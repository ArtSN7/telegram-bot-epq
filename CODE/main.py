import datetime

import asyncio
import os
import aiohttp
from data import db_session
from data.user import User

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton


reply_keyboard = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)



async def help_command(update, context):
    await update.message.reply_text('1')


# start
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



def main():
    # create an Application object
    # inserting bot's token which was given in the BotFather as a string 
    application = Application.builder().token("6534440693:AAEBK22bypwmKrjI8SGczQG85fmkLjjb4no").build()


    # registrating command handler in order to check what buttons were pressed
    application.add_handler(CommandHandler("start", start_command)) # /start command
    application.add_handler(CommandHandler("help", help_command)) # /help command

    # starting application
    application.run_polling()





if __name__ == '__main__': # part of the code that set up the environmet 
    
    db_session.global_init("code/db/data.db") # connecting database in the main code code/db/data.db - path to reach the file


    if os.name == 'nt': # if os is windows
        # essential part which will set up "asyncio" library for the specific system
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        

    main() # starting main code 