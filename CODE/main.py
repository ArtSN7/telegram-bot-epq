import datetime

import asyncio
import os
import aiohttp
from data import db_session
from data.user import User

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram import ReplyKeyboardRemove

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
reply_keyboard_news = [['/general_news'], ['/specific_news']]
markup_news = ReplyKeyboardMarkup(reply_keyboard_news, one_time_keyboard=True, resize_keyboard=True)


#------------------------------------------------------------------
# recipes buttons 

# types of request
reply_keyboard_recipe_type = [['/by_cuisine'], ['/by_name']]
markup_recipe_type = ReplyKeyboardMarkup(reply_keyboard_recipe_type, one_time_keyboard=True, resize_keyboard=True)

#------------------------------------------------------------------
# evetns buttons
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


#------------------------------------------------------------------


#------------------------------------------------------------------
# function which work with all inline keyboard buttons
async def inline_buttons(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    # languages

    if query.data == 'es': # if inline button with this callback had been used, then : ( the same idea with other if part in this function )

        await es(id) # changing language
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'") # sending message about this
    
    if query.data == 'en':

        await en(id)
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'")
    
    if query.data == 'fr':

        await fr(id)
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'")

    if query.data == 'de':

        await de(id)
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'")

    if query.data == 'ru':

        await ru(id)
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'")

    if query.data == 'it':

        await it(id)
        await query.edit_message_text(text=f"Language has been successfully updated to the '{query.data}'")


    # news

    if query.data == "general":
        answer = await general(id) # getting response 
        await query.edit_message_text(text=f"{answer}") # sending response to the user

    if query.data == "business":
        answer = await business(id)
        await query.edit_message_text(text=f"{answer}")


    if query.data == "health":
        answer = await health(id)
        await query.edit_message_text(text=f"{answer}")
        

    if query.data == "science":
        answer = await science(id)
        await query.edit_message_text(text=f"{answer}")

    if query.data == "sports":
        answer = await sports(id)
        await query.edit_message_text(text=f"{answer}")

    if query.data == "entertainment":
        answer = await entertainment(id)
        await query.edit_message_text(text=f"{answer}")
    
    if query.data == "technology":
        answer = await technology(id)
        await query.edit_message_text(text=f"{answer}")

    # cuisine types
        
    if query.data == 'italian':
        answer = await italian_cuisine() # getting response 
        await query.edit_message_text(text=f"{answer}") # sending response to the user

    if query.data == 'british':
        answer = await british_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'chinese':
        answer = await chinese_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'european':
        answer = await european_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'french':
        answer = await french_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'german':
        answer = await german_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'greek':
        answer = await greek_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'indian':
        answer = await indian_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'japanese':
        answer = await japanese_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'korean':
        answer = await korean_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'mexican':
        answer = await mexican_cuisine()
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'thai':
        answer = await thai_cuisine()
        await query.edit_message_text(text=f"{answer}")


#------------------------------------------------------------------


#------------------------------------------------------------------
# help function wich explains abilities of all functions in the bot 
async def help_command(update, context):
    await update.message.reply_text('Please, share your thoughts with us:\n\nhttps://forms.gle/mHidQLY62DiZVeHz8', reply_markup=ReplyKeyboardRemove())


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
    await update.message.reply_html(f"Hello, {user.mention_html()}!\n\nI am AUXXIbot, but friends call me AUX, so you can call me like this ;D\n\nI am your personal assistant that can simplify your life, moreover, you can ask me whatever you want and recieve an answer!\n\nTo see more of my power try buttons in MENU :)")



#------------------------------------------------------------------
# flight function

async def flight_command_0(update, context):
    await update.message.reply_text("Please, send us airport code from your ticket. Just to remind, EK104 ( on the photo ) is a airport code (EK) and flight number(104)", reply_markup=ReplyKeyboardRemove())

    url = "https://www.flightright.co.uk/wp-content/uploads/sites/2/2023/02/where-can-i-find-my-flight-number.jpg"
    await context.bot.send_photo(update.message.chat_id, url, caption="") # seding example of ticket
    return 1 # showing what function must be called next

async def flight_command_1(update, context):
    context.user_data['airport'] = update.message.text.upper() # storing airport name , upper is needed if user inputed in a wrong format
    await update.message.reply_text("Thank you, now send us you flight code, which is also on your ticket.", reply_markup=ReplyKeyboardRemove()) # asking for the flight code
    return 2 # showing what function must be called next

async def flight_command_2(update, context):
    context.user_data['flight'] = update.message.text # storing flight code

    answer = await flight.get_flight_info(context.user_data["flight"], context.user_data["airport"]) # calling function which will provide info about this flight 

    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove()) # sending response to the user

    context.user_data.clear() # deleting all information about this user

    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# events function

async def events_command(update, context):
    await update.message.reply_html(rf"To find events near you, please, send us your location!", reply_markup=markup_event_loc) # sending button with location
    return 1


async def events_response(update, context):

    long, lat = update.message.location.longitude, update.message.location.latitude # getting user coordinates 

    context.user_data['long'] = long # storing longitude
    context.user_data['lat'] = lat # storing latitude 

    await update.message.reply_html(rf"Please, choose the type of event!", reply_markup=markup_events_type) # asking user to choose type of event ( Real or Virtual )

    return ConversationHandler.END # finishing conversation


async def real_event_type(update, context): # if event type is real
    context.user_data['type'] = "Real" # storing information about event type
    await update.message.reply_html(rf"Please, now choose the date of event!", reply_markup=markup_events_date) # asking to choose date of event
    

async def virtual_event_type(update, context): # if event type is virtual
    context.user_data['type'] = "Virtual" # storing information about event type
    await update.message.reply_html(rf"Please, now choose the date of event!", reply_markup=markup_events_date) # asking to choose date of event

 # dates of event
async def today_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "today") # calling main function from events.py
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def tomorrow_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "tomorrow") # calling main function from events.py
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def this_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "week") # calling main function from events.py
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def next_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "next_week") # calling main function from events.py
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def all_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "all") # calling main function from events.py
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove())  # sending response to user


#------------------------------------------------------------------
# chat-gpt function
async def gpt_command(update, context):
    await update.message.reply_text('Please, send a message with your question.', reply_markup=ReplyKeyboardRemove()) # asking to send a messagew with question 
    return 1 # showing that the next function must be message_answer(update, context)

async def message_answer(update, context):
    txt = update.message.text # gettin text which was sent by user
    await update.message.reply_text("Please, wait. Your request might take 2-15 seconds.")
    answer = gpt.question_gpt(txt) # asking gpt function to give an answer - if something is wrong, it will return error
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending an answer to user
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function



#------------------------------------------------------------------
# quote function
async def quote_command(update, context):
    func = quote.quote() # declaring function call ( procedure that is needed to work with async requests )
    answer = await func # getting response from function
    await update.message.reply_text(f'{answer[0]}', reply_markup=ReplyKeyboardRemove()) # sending random quote to user

    if answer[1] != "": # if there is a link with author's photo, then we send it
        await context.bot.send_photo(update.message.chat_id, answer[1], caption="") # sending link to the photo ( tg will represent it )



#------------------------------------------------------------------
# weather function

async def weather_command(update, context):
    await update.message.reply_html(rf"Please, choose how you will send us your location ( by sending text address or by sharing your location using button )",
                                    reply_markup=markup_weather_options) # asking how user will send location

async def weather_command_coords(update, context):
    await update.message.reply_html(rf"To analyse data, you need to send your current location (use button below)",
                                    reply_markup=markup_weather_loc) # asking user to send coordinates by innate telegram function
    return 1

async def weather_command_address(update, context):
    await update.message.reply_html(rf"To analyse data, you need to send address", reply_markup=ReplyKeyboardRemove()) # asking user to send coordinates by text ( King' school canterbury , for example )
    return 1

async def weather_command_response_coords(update, context): # function which works with longitude and latitude 
    long, lang = update.message.location.longitude, update.message.location.latitude # getting user coordinates 
    func = weather.weather_coords((long, lang)) # calling function
    answer = await func # getting response 
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to the user
    return ConversationHandler.END # ending conversation

async def weather_command_response_address(update, context): # function which works with address
    func = weather.weather_address(update.message.text) # calling function
    answer = await func # getting answer
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to the user
    return ConversationHandler.END # ending conversation 

#------------------------------------------------------------------
# news function 
async def news_command(update, context):
    await update.message.reply_html(rf"Please, choose the type of news you want to see.", reply_markup=markup_news) # chose between general and specific


async def general_news(update, context):

    keyboard_news = [
        [InlineKeyboardButton("general󠁧", callback_data="general")],
        [InlineKeyboardButton("business", callback_data="business")],
        [InlineKeyboardButton("entertainment", callback_data="entertainment")],
        [InlineKeyboardButton("health", callback_data="health")],
        [InlineKeyboardButton("science", callback_data="science")],
        [InlineKeyboardButton("sports", callback_data="sports")],
        [InlineKeyboardButton("technology", callback_data="technology")]
    ] # buttons which can be used 

    markup_news_topic = InlineKeyboardMarkup(keyboard_news) # adding this buttons to the text
    await update.message.reply_html(rf"Please, choose topic you are intersted in.", reply_markup=markup_news_topic) # if user had chosen general news, he would need to choose topic
    
    await update.message.reply_text('', reply_markup=ReplyKeyboardRemove()) # removing keyboard eventhough there will be error 


# functions connected to the different topics
async def business(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('business', language)
    answer = await func

    return answer


async def entertainment(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('entertainment', language)
    answer = await func
    return answer


async def general(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('general', language)
    answer = await func
    return answer


async def health(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('health', language)
    answer = await func
    return answer


async def science(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('science', language)
    answer = await func
    return answer


async def sports(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('sports', language)
    answer = await func
    return answer


async def technology(id):

    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    language = person.language # getting user's language

    func = news.get_news('technology', language)
    answer = await func
    return answer


async def specific_news(update, context):
    await update.message.reply_text("Enter the topic you are interested in (for example, Microsoft)", reply_markup=ReplyKeyboardRemove())
    return 1


async def specific_news_response(update, context):

    func = news.get_spec_news(update.message.text)
    answer = await func
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


#------------------------------------------------------------------
# recipes function
async def recipes_command(update, context):
    await update.message.reply_text(rf"Please, choose by which parameter you want to choose recipe", reply_markup=markup_recipe_type) # chose between different types of request



async def cuisine_command(update, context):

    keyboard_cuisine_type = [
        [InlineKeyboardButton("Italian🇮🇹", callback_data="italian")],
        [InlineKeyboardButton("Thai🇹🇭", callback_data="thai")],
        [InlineKeyboardButton("Mexican🇲🇽", callback_data="mexican")],
        [InlineKeyboardButton("Korean🇰🇷", callback_data="korean")],
        [InlineKeyboardButton("Japanese🇯🇵", callback_data="japanese")],
        [InlineKeyboardButton("Indian🇮🇳", callback_data="indian")],
        [InlineKeyboardButton("Greek🇬🇷", callback_data="greek")],
        [InlineKeyboardButton("German🇩🇪", callback_data="german")],
        [InlineKeyboardButton("French🇫🇷", callback_data="french")],
        [InlineKeyboardButton("European🇪🇺", callback_data="european")],
        [InlineKeyboardButton("Chinese🇨🇳", callback_data="chinese")],
        [InlineKeyboardButton("British🇬🇧", callback_data="british")],
 
    ]

    markup_cuisine_type = InlineKeyboardMarkup(keyboard_cuisine_type)


    await update.message.reply_text(rf"Please, choose the type of cuisine you are interested in.", reply_markup=markup_cuisine_type) # chose between different cuisines


# adding different cuisines

async def italian_cuisine():
    func = recipes.get_rec_by_cuisine("Italian") # getting response 
    answer, url = await func # declaring data

    if url != "...": # if there is a photo ( no errors )
        return f"{answer}\n\n{url}" # send text with photo
    else:
        return f"{answer}" # send text without photo


async def british_cuisine():
    func = recipes.get_rec_by_cuisine("British")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def chinese_cuisine():
    func = recipes.get_rec_by_cuisine("Chinese")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def european_cuisine():
    func = recipes.get_rec_by_cuisine("European")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def french_cuisine():
    func = recipes.get_rec_by_cuisine("French")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def german_cuisine():
    func = recipes.get_rec_by_cuisine("German")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def greek_cuisine():
    func = recipes.get_rec_by_cuisine("Greek")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def indian_cuisine():
    func = recipes.get_rec_by_cuisine("Indian")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def japanese_cuisine():
    func = recipes.get_rec_by_cuisine("Japanese")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


async def korean_cuisine():
    func = recipes.get_rec_by_cuisine("Korean")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"

async def mexican_cuisine():
    func = recipes.get_rec_by_cuisine("Mexican")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"

async def thai_cuisine():
    func = recipes.get_rec_by_cuisine("Thai")
    answer, url = await func

    if url != "...":
        return f"{answer}\n\n{url}"
    else:
        return f"{answer}"


# dish name 
async def dish_name(update, context):
    await update.message.reply_text(f"Please, send a name of the dish you want to cook, for example, pasta. ( in english )", reply_markup=ReplyKeyboardRemove())
    return 1 # showing bot that next message must be read by dish_name_response function

async def dish_name_response(update, context):
    txt = update.message.text # gettin text which was sent by user
    answer, url = await recipes.get_rec_by_name(txt) # sending a request

    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending an answer to user
    if url != '...':
        await context.bot.send_photo(update.message.chat_id, url, caption="") # sending picture
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function
#------------------------------------------------------------------


#------------------------------------------------------------------
# Profile connected function 

async def user_profile(update, context):
    await update.message.reply_html(rf"Please, choose what you want to change", reply_markup=markup_profile_change)


# changing user's language
async def change_user_lang(update, context):
    user = update.effective_user # getting user info from telegram

    id = user.id #getting user id
    db_sess = db_session.create_session() # creating connection with database

    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user

    lang = person.language # getting user's language

    keyboard_language = [
        [InlineKeyboardButton("En🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="en")],
        [InlineKeyboardButton("Fr🇫🇷", callback_data="fr")],
        [InlineKeyboardButton("De🇩🇪", callback_data="de")],
        [InlineKeyboardButton("Es🇪🇸", callback_data="es")],
        [InlineKeyboardButton("It🇮🇹", callback_data="it")],
        [InlineKeyboardButton("Ru🇷🇺", callback_data="ru")],
    ]

    markup_profile_language = InlineKeyboardMarkup(keyboard_language)


    await update.message.reply_html(rf"Please, choose language to which you want to switch. Your current language is '{lang}'", reply_markup=markup_profile_language)


# language functions
async def en(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'en' # changing user's language

    db_sess.commit()


async def it(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'it' # changing user's language

    db_sess.commit()


async def de(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'de' # changing user's language

    db_sess.commit()


async def fr(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'fr' # changing user's language

    db_sess.commit()


async def es(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'es' # changing user's language

    db_sess.commit()

    
async def ru(id):
    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    person.language  = 'ru' # changing user's language

    db_sess.commit()

#------------------------------------------------------------------


#------------------------------------------------------------------
# function that stops dialogue with user
async def stop(update, context):
    await update.message.reply_text("Function was stopped.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function


#------------------------------------------------------------------
# functions that controls all the activity in the bot
def main():


    # create an Application object with specific telegram key which I recieved from BotFather
    application = Application.builder().token(config.tg_key).build()
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # registrating command handler in order to check what buttons were pressed

    application.add_handler(CallbackQueryHandler(inline_buttons)) # handler which will work with all inline functions 

    application.add_handler(CommandHandler("start", start_command)) # adding /start command
    application.add_handler(CommandHandler("help", help_command)) # adding /help command
    application.add_handler(CommandHandler("quote", quote_command)) # adding /quote command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # FLIGHT COMMAND

    conv_handler_flight = ConversationHandler( # /gpt command
        entry_points=[CommandHandler("flight", flight_command_0)], # declaring the function which will start the conversation if gpt command is called
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_command_1)], # after next message this function will be called ( user must send text message )
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_command_2)], # after next message this function will be called ( user must send text message )
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
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_answer)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_gpt) # adding /gpt command
    #------------------------------------------------------------------

    #------------------------------------------------------------------
    # NEWS COMMAND

    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("general_news", general_news))

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
    application.add_handler(CommandHandler("by_cuisine", cuisine_command))


    # dish_name
    conv_handler_dish_name = ConversationHandler( # /dish_name command
        entry_points=[CommandHandler("by_name", dish_name)], # declaring the function which will start the conversation if dish_name had been called
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, dish_name_response)], # after next message this function will be called ( user must send text message )
        },
        fallbacks=[CommandHandler('stop', stop)] # function which will end conversation
    )
    application.add_handler(conv_handler_dish_name) # adding /dish_name command

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