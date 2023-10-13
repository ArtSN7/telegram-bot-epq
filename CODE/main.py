import asyncio
import os
import aiohttp
from data import db_session

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton


reply_keyboard = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)



async def help_command(update, context):
    await update.message.reply_text('1')


# start
async def start_command(update, context):
    user = update.effective_user

    await update.message.reply_html(f"Hello, {user.mention_html()}!\n\nI am AUXXIbot, but friends call me AUX, so you can call me like this ;D\n\nI am your personal assistant that can simplify your life, moreover, you can ask me whatever you want and recieve an answer!\n\nTo see more of my power try /help button :)")



def main():
    # create an Application object
    # inserting bot's token which was given in the BotFather as a string 
    application = Application.builder().token("6534440693:AAEBK22bypwmKrjI8SGczQG85fmkLjjb4no").build()




    # Регистрируем обработчик в приложении.
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Запускаем приложение.
    application.run_polling()





# part of the code that set up the environmet 
if __name__ == '__main__':
    
    #db_session.global_init("db/blogs.db") # connecting database in the main code


    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        # essential part which will set up "asyncio" library for the specific system

    main() # starting main code 