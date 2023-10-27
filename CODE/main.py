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

from functions import gpt, quote, weather, news, recipes, events, flight

#------------------------------------------------------------------
# weather buttond
btn_loc = KeyboardButton('SEND A LOCATION', request_location=True) # button which will ask user to send a location
markup_weather_loc = ReplyKeyboardMarkup([[btn_loc]], one_time_keyboard=True, resize_keyboard=True) # function which will show this button

coords_button = KeyboardButton('/coordinates')
address_button = KeyboardButton('/address')
markup_weather_options = ReplyKeyboardMarkup([[address_button],[coords_button]], one_time_keyboard=True, resize_keyboard=True) # showing weather option buttons

#------------------------------------------------------------------
# news buttons 
reply_keyboard_news = [['/specific_news'], ['/general_news']]
markup_news = ReplyKeyboardMarkup(reply_keyboard_news, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard_news_topic = [['/general'], ['/business'], ['/entertainment'], ['/health'], ['/science'], ['/sports'],['/technology']]
markup_news_topic = ReplyKeyboardMarkup(reply_keyboard_news_topic, one_time_keyboard=True, resize_keyboard=True)

#------------------------------------------------------------------
# recipes buttons 

# types of request
reply_keyboard_recipe_type = [['/cuisines'], ['/ingredients'], ['/dish_name']]
markup_recipe_type = ReplyKeyboardMarkup(reply_keyboard_recipe_type, one_time_keyboard=True, resize_keyboard=True)

# cuisines 
reply_keyboard_cuisine_type = [['/Italian'], ['/British'], ['/Chinese'], ['/European'], ['/French'], ['/German'],['/Greek'], ['/Indian'],['/Japanese'], ['/Korean'],
                               ['/Mexican'], ['/Thai']]
markup_cuisine_type = ReplyKeyboardMarkup(reply_keyboard_cuisine_type, one_time_keyboard=True, resize_keyboard=True)

#------------------------------------------------------------------
# evetns buttond
markup_event_loc = ReplyKeyboardMarkup([[btn_loc]], one_time_keyboard=True, resize_keyboard=True) # function which will show this button

reply_keyboard_events_type = [['/Real'], ['/Virtual']]
markup_events_type = ReplyKeyboardMarkup(reply_keyboard_events_type, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard_events_date = [['/Today'], ['/Tomorrow'], ['/This_week'], ['/Next_week'], ['/All_dates']]
markup_events_date = ReplyKeyboardMarkup(reply_keyboard_events_date, one_time_keyboard=True, resize_keyboard=True)
#------------------------------------------------------------------

#------------------------------------------------------------------
# profile change buttons 
reply_keyboard_profile_change = [['/change_language']]
markup_profile_change = ReplyKeyboardMarkup(reply_keyboard_profile_change, one_time_keyboard=True, resize_keyboard=True)

# ar de en es fr he it nl no pt ru sv ud zh - languages
reply_keyboard_profile_language = [['/en'],['/fr'], ['/de'], ['/es'],['/it'],['/ru']]
markup_profile_language = ReplyKeyboardMarkup(reply_keyboard_profile_language, one_time_keyboard=True, resize_keyboard=True)


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
# flight function

async def flight_command_0(update, context):
    await update.message.reply_text("Please, send us airport code from your ticket. Just to remind, EK104 ( on the photo ) is a airport code (EK) and flight number(104)")
    await update.message.reply_text("https://www.flightright.co.uk/wp-content/uploads/sites/2/2023/02/where-can-i-find-my-flight-number.jpg")
    return 1

async def flight_command_1(update, context):
    context.user_data['airport'] = update.message.text.upper() # upper is needed if user inputed in a wrong format
    await update.message.reply_text("Thank you, now send us you flight code, which is also on your ticket.")
    return 2

async def flight_command_2(update, context):
    context.user_data['flight'] = update.message.text

    answer = await flight.get_flight_info(context.user_data["flight"], context.user_data["airport"])
    await update.message.reply_text(answer)

    context.user_data.clear()
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# events function

async def events_command(update, context):
    await update.message.reply_html(rf"To find events near you, please, send us your location!", reply_markup=markup_event_loc)
    return 1


async def events_response(update, context):

    long, lat = update.message.location.longitude, update.message.location.latitude # getting user coordinates 

    context.user_data['long'] = long
    context.user_data['lat'] = lat
    await update.message.reply_html(rf"Please, choose the type of event!",
                                    reply_markup=markup_events_type)

    return ConversationHandler.END

async def real_event_type(update, context): # if event type is real
    context.user_data['type'] = "Real"
    await update.message.reply_html(rf"Please, now choose the date of event!",
                                    reply_markup=markup_events_date)
    
async def virtual_event_type(update, context): # if event type is virtual
    context.user_data['type'] = "Virtual"
    await update.message.reply_html(rf"Please, now choose the date of event!",
                                    reply_markup=markup_events_date)


async def today_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "today")
    await update.message.reply_text(f"{answer}") 

async def tomorrow_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "tomorrow")
    await update.message.reply_text(f"{answer}") 

async def this_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "week")
    await update.message.reply_text(f"{answer}") 

async def next_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "next_week")
    await update.message.reply_text(f"{answer}") 

async def all_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "all")
    await update.message.reply_text(f"{answer}")  


#------------------------------------------------------------------
# chat-gpt function
async def gpt_command(update, context):
    await update.message.reply_text('Please, send a message with your question.') # asking to send a messagew with question 
    return 1 # showing that the next function must be message_answer(update, context)

async def message_answer(update, context):
    txt = update.message.text # gettin text which was sent by user
    await update.message.reply_text("Wait for a little bit... We are looking for the best answer!")
    answer = gpt.question_gpt(txt) # asking gpt function to give an answer - if something is wrong, it will return error
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
# weather function

async def weather_command(update, context):
    await update.message.reply_html(rf"Please, choose how you will send us your location ( by sending text address or by sharing your location using button )",
                                    reply_markup=markup_weather_options)

async def weather_command_coords(update, context):
    await update.message.reply_html(rf"To analyse data, you need to send your current location.",
                                    reply_markup=markup_weather_loc)
    return 1

async def weather_command_address(update, context):
    await update.message.reply_html(rf"To analyse data, you need to send address")
    return 1

async def weather_command_response_coords(update, context): # function which works with longitude and latitude 
    long, lang = update.message.location.longitude, update.message.location.latitude # getting user coordinates 
    func = weather.weather_coords((long, lang)) # calling function
    answer = await func # getting response 
    await update.message.reply_text(f"{answer}") # sending response to the user
    return ConversationHandler.END # ending conversation

async def weather_command_response_address(update, context): # function which works with address
    func = weather.weather_address(update.message.text) # calling function
    answer = await func # getting answer
    await update.message.reply_text(f"{answer}") # sending response to the user
    return ConversationHandler.END # ending conversation 

#------------------------------------------------------------------
# news function 
async def news_command(update, context):
    await update.message.reply_html(rf"Please, choose the type of news you want to see.", reply_markup=markup_news) # chose between general and specific


async def general_news(update, context):
    await update.message.reply_html(rf"Please, choose interesting topic.", reply_markup=markup_news_topic) # if user had chosen general news, he would need to choose topic

# functions connected to the different topics
async def business(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('business', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def entertainment(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('entertainment', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def general(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('general', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def health(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('health', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def science(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('science', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def sports(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('sports', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def technology(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('technology', language)
    answer = await func
    await update.message.reply_text(f"{answer}")


async def specific_news(update, context):
    await update.message.reply_text("Enter the topic you are interested in (for example, Microsoft)")
    return 1


async def specific_news_response(update, context):

    func = news.get_spec_news(update.message.text)
    answer = await func
    await update.message.reply_text(f"{answer}")
    return ConversationHandler.END


#------------------------------------------------------------------
# recipes function
async def recipes_command(update, context):
    await update.message.reply_html(rf"Please, choose by which parameter you want to choose recipe", reply_markup=markup_recipe_type) # chose between different types of request



async def cuisine_command(update, context):
    await update.message.reply_html(rf"Please, choose the type of cuisine you are interested in.", reply_markup=markup_cuisine_type) # chose between different cuisines

# adding different cuisines
async def italian_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Italian")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def british_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("British")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def chinese_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Chinese")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def european_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("European")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def french_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("French")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def german_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("German")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def greek_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Greek")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def indian_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Idian")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def japanese_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Japanese")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def korean_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Korean")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def mexican_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Mexican")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

async def thai_cuisine(update, context):
    func = recipes.get_rec_by_cuisine("Thai")
    answer, url = await func
    await update.message.reply_text(f"{answer}")
    await update.message.reply_text(f"{url}")

# dish name 
async def dish_name(update, context):
    await update.message.reply_text(f"Please, send me a name of the dish you want to cook, for example, pasta.")
    return 1 # showing bot that next message must be read by dish_name_response function

async def dish_name_response(update, context):
    txt = update.message.text # gettin text which was sent by user
    answer, url = await recipes.get_rec_by_name(txt) # sending a request

    await update.message.reply_text(f"{answer}") # sending an answer to user
    await update.message.reply_text(f"{url}") # sending picture
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function

# ingredients 
# dish name 
async def ingredients(update, context):
    await update.message.reply_text(f"Please, send me name of ingredients in format name1,name2,name3... , where name1 is a name of ingredient.")
    return 1 # showing bot that next message must be read by dish_name_response function

async def ingredient_response(update, context):
    txt = update.message.text # gettin text which was sent by user
    answer, url = await recipes.get_rec_by_ingredients(txt) # sending a request

    await update.message.reply_text(f"{answer}") # sending an answer to user
    await update.message.reply_text(f"{url}") # sending picture
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# Changing language function

async def user_profile(update, context):
    await update.message.reply_html(rf"Please, choose what you want to change", reply_markup=markup_profile_change)


async def change_user_lang(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    lang = person.language # getting user's language

    await update.message.reply_html(rf"Please, choose language to which you want to switch. Your current language is '{lang}'", reply_markup=markup_profile_language)


async def en(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'en' # changing user's language

    db_sess.commit()

    await update.message.reply_text("Your language has been succefully updated!")

async def it(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'it' # changing user's language

    db_sess.commit()


    await update.message.reply_text("Your language has been succefully updated!")

async def de(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'de' # changing user's language

    db_sess.commit()



    await update.message.reply_text("Your language has been succefully updated!")

async def fr(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'fr' # changing user's language

    db_sess.commit()


    await update.message.reply_text("Your language has been succefully updated!")

async def es(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'es' # changing user's language

    db_sess.commit()


    await update.message.reply_text("Your language has been succefully updated!")

async def ru(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'ru' # changing user's language

    db_sess.commit()


    await update.message.reply_text("Your language has been succefully updated!")



#------------------------------------------------------------------


#------------------------------------------------------------------
# function that stops dialogue with user
async def stop(update, context):
    update.message.reply_text("Function was stopped.")
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# functions that controls all the activity in the bot
def main():


    # create an Application object with specific telegram key which I recieved from BotFather
    application = Application.builder().token(config.tg_key).build()
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # registrating command handler in order to check what buttons were pressed

    application.add_handler(CommandHandler("start", start_command)) # adding /start command
    application.add_handler(CommandHandler("help", help_command)) # adding /help command
    application.add_handler(CommandHandler("quote", quote_command)) # adding /quote command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # FLIGHT COMMAND
    conv_handler_flight = ConversationHandler( # /gpt command
        entry_points=[CommandHandler("flight", flight_command_0)], # declaring the function which will start the conversation if gpt command is called
        states={
            1: [MessageHandler(filters.TEXT, flight_command_1)], # after next message this function will be called ( user must send text message )
            2: [MessageHandler(filters.TEXT, flight_command_2)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_flight) # adding /flight command
    #------------------------------------------------------------------


    #------------------------------------------------------------------
    # WEATHER COMMAND
    application.add_handler(CommandHandler("weather", weather_command)) # adding /weather command which will start all weather process

    conv_handler_weather = ConversationHandler( # /weather command with coordinates
        entry_points=[CommandHandler("coordinates", weather_command_coords)], # declaring the function which will start the conversation if weather command is called
        states={
            1: [MessageHandler(filters.LOCATION & ~filters.COMMAND, weather_command_response_coords)], # after next message this function will be called ( user must send location message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_weather) # adding /weather command with address

    conv_handler_weather_address = ConversationHandler( # /weather command with coordinates
        entry_points=[CommandHandler("address", weather_command_address)], # declaring the function which will start the conversation if weather command is called
        states={
            1: [MessageHandler(filters.TEXT, weather_command_response_address)], # after next message this function will be called ( user must send location message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_weather_address) # adding /weather command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # GPT COMMAND
    conv_handler_gpt = ConversationHandler( # /gpt command
        entry_points=[CommandHandler("gpt", gpt_command)], # declaring the function which will start the conversation if gpt command is called
        states={
            1: [MessageHandler(filters.TEXT, message_answer)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_gpt) # adding /gpt command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # NEWS COMMAND
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("general_news", general_news))
    application.add_handler(CommandHandler("business", business))
    application.add_handler(CommandHandler("entertainment", entertainment))
    application.add_handler(CommandHandler("general", general))
    application.add_handler(CommandHandler("health", health))
    application.add_handler(CommandHandler("science", science))
    application.add_handler(CommandHandler("sports", sports))
    application.add_handler(CommandHandler("technology", technology))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('specific_news', specific_news)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, specific_news_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # RECIPES COMMAND

    application.add_handler(CommandHandler("recipes", recipes_command))

    # cuisines 
    application.add_handler(CommandHandler("cuisines", cuisine_command))
    application.add_handler(CommandHandler("Italian", italian_cuisine))
    application.add_handler(CommandHandler("British", british_cuisine))
    application.add_handler(CommandHandler("Chinese", chinese_cuisine))
    application.add_handler(CommandHandler("European", european_cuisine))
    application.add_handler(CommandHandler("French", french_cuisine))
    application.add_handler(CommandHandler("German", german_cuisine))
    application.add_handler(CommandHandler("Greek", greek_cuisine))
    application.add_handler(CommandHandler("Indian", indian_cuisine))
    application.add_handler(CommandHandler("Japanese", japanese_cuisine))
    application.add_handler(CommandHandler("Korean", korean_cuisine))
    application.add_handler(CommandHandler("Mexican", mexican_cuisine))
    application.add_handler(CommandHandler("Thai", thai_cuisine))

    # dish_name
    conv_handler_dish_name = ConversationHandler( # /dish_name command
        entry_points=[CommandHandler("dish_name", dish_name)], # declaring the function which will start the conversation if dish_name had been called
        states={
            1: [MessageHandler(filters.TEXT, dish_name_response)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_dish_name) # adding /dish_name command

    # ingredients
    conv_handler_ingredients = ConversationHandler( # /dish_name command
        entry_points=[CommandHandler("ingredients", ingredients)], # declaring the function which will start the conversation if ingredients had been called
        states={
            1: [MessageHandler(filters.TEXT, ingredient_response)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_ingredients) # adding /ingredients command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # EVENTS COMMAND

    conv_handler_events = ConversationHandler( # /events command 
        entry_points=[CommandHandler("events", events_command)], # declaring the function which will start the conversation if events command is called
        states={
            1: [MessageHandler(filters.LOCATION & ~filters.COMMAND, events_response)], # after next message this function will be called ( user must send location message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_events) # adding /events command with address


    # types of event
    application.add_handler(CommandHandler("Real", real_event_type))
    application.add_handler(CommandHandler("Virtual", virtual_event_type))

    # dates of event
    application.add_handler(CommandHandler("Today", today_event))
    application.add_handler(CommandHandler("Tomorrow", tomorrow_event))
    application.add_handler(CommandHandler("This_week", this_week_event))
    application.add_handler(CommandHandler("Next_week", next_week_event))
    application.add_handler(CommandHandler("All_dates", all_event))
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # USER'S PROFILE COMMAND

    application.add_handler(CommandHandler("profile", user_profile))
    application.add_handler(CommandHandler("change_language", change_user_lang))


    # languages 
    application.add_handler(CommandHandler("en", en))
    application.add_handler(CommandHandler("de", de))
    application.add_handler(CommandHandler("fr", fr))
    application.add_handler(CommandHandler("it", it))
    application.add_handler(CommandHandler("es", es))
    application.add_handler(CommandHandler("ru", ru))
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