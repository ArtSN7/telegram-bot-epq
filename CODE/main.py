import datetime

import asyncio
import os
import aiohttp
from data import db_session
from data.user import User

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from data import config

from functions import gpt, quote

#------------------------------------------------------------------

# options which will be shown after using time command
#reply_keyboard_time = [[''], [''], [''], ['']]
#markup_time = ReplyKeyboardMarkup(reply_keyboard_time, one_time_keyboard=True)


#------------------------------------------------------------------


#------------------------------------------------------------------
# help function wich explains abilities of all functions in the bot
async def help_command(update, context):
    await update.message.reply_text('1')


#------------------------------------------------------------------
# start function which is called after user use bot for the first time
async def start_command(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    if not person: # if person is not in the database, so we add him

        usera = User() # creating user object ( name usera as user is already chosen )
        usera.tg_id = id # adding to the field id in database his tg id
        usera.name = user.mention_html() # getting his name using user.mention_html() and add this name to the name field in the database
        usera.date = datetime.date.today() # adding date of user registration to the date field

        db_sess.add(usera) # adding user with data put to the fields to the database
        db_sess.commit() # commiting and updating our database, from this moment there is an information about this specific user in the database

    # sending message as an asnwer to the start button
    await update.message.reply_html(f"Hello, {user.mention_html()}!\n\nI am AUXXIbot, but friends call me AUX, so you can call me like this ;D\n\nI am your personal assistant that can simplify your life, moreover, you can ask me whatever you want and recieve an answer!\n\nTo see more of my power try /help button :)")



#------------------------------------------------------------------
# chat-gpt function
async def gpt_command(update, context):
    await update.message.reply_text('Please, send a message with your question.') # asking to send a messagew with question 
    return 1 # showing that the next function must be message_answer(update, context)

async def message_answer(update, context):
    txt = update.message.text # gettin text which was sent by user
    answer = gpt.question_gpt(txt) # asking gpt function to give an answer - if something is wrong, it will return error
    await update.message.reply_text("Wait for a little bit... We are looking for the best answer!")
    await update.message.reply_text(f"{answer}") # sending an answer to user
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function



#------------------------------------------------------------------
# quote function
async def quote_command(update, context):
    func = quote.quote() # declaring function call ( procedure that is needed to work with async requests )
    answer = await func # getting response from function
    await update.message.reply_text(f'{answer[0]}') # sending random quote to user

    if answer[1] != "": # if there is a link with author's photo, then we send it
        await context.bot.send_message(update.message.chat_id, text=answer[1]) # sending link to the photo ( tg will represent it )

#------------------------------------------------------------------


    


#------------------------------------------------------------------
# function that stops dialogue with user
async def stop(update, context):
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# functions that controls all the activity in the bot
def main():
    # create an Application object with specific telegram key which I recieved from BotFather
    application = Application.builder().token(config.tg_key).build()
    #------------------------------------------------------------------


    # registrating command handler in order to check what buttons were pressed

    application.add_handler(CommandHandler("start", start_command)) # adding /start command
    application.add_handler(CommandHandler("help", help_command)) # adding /help command
    application.add_handler(CommandHandler("quote", quote_command)) # adding /quote command

    #------------------------------------------------------------------
    conv_handler_gpt = ConversationHandler( # /gpt command
        entry_points=[CommandHandler("gpt", gpt_command)], # declaring the function which will start the conversation if gpt command will be called
        states={
            1: [MessageHandler(filters.TEXT, message_answer)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_gpt) # adding /gpt command
    #------------------------------------------------------------------


    #------------------------------------------------------------------
    # starting application
    application.run_polling()





#------------------------------------------------------------------
if __name__ == '__main__': # part of the code that set up the environmet 
    
    db_session.global_init("code/db/data.db") # connecting database in the main code code/db/data.db - path to reach the file


    if os.name == 'nt': # if os is windows
        # essential part which will set up "asyncio" library for the specific system
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        

    main() # starting main code 