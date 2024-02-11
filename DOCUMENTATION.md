# DOCUMENTATION

---

# Before Reading

---

**GIT-HUB link - [https://github.com/ArtSN7/telegram-bot](https://github.com/ArtSN7/telegram-bot)**

**Presentation - [click](https://docs.google.com/presentation/d/1zW4qY62hreSH9HOeFIs154F6oV6w4LMu5XsAehd-jx4/edit?usp=sharing)**

**Documentation of how to write telegram-bots with theory and examples you might find in the repository in the file GUIDE.md. It will be useful for you to check it first before reading documentation, as it will help you deeply understand how does it all work.**

---

# Introduction

---

## Telegram

Telegram is a messenger (messaging program) implemented using a client-server architecture. Using the server to create a dialogue between two clients, Telegram sends text messages through it or directly, as well as images, videos, or documents in other formats.

## What is a telegram-bot

A Telegram bot is a special user whose behaviour is controlled by some program. Technically, it makes no difference to the server whether a given user is a human or a bot: to the server, both clients look the same.

## What problems can be solved by telegram-bot

Everything, it is limited only by imagination. Here are some examples:

- Autoresponders - all situations where an unambiguous answer to a request is required. For example, the bot can provide telephone numbers and other contacts of the organization, its working hours, or provide other background information upon request

- Interface for accessing web services - the bot can make requests to various [APIs](https://www.ibm.com/topics/api) *(application programming interface, which is a set of definitions and protocols for building and integrating application software)* and send responses in the form of telegram messages.

- Action scenarios - the bot can go through any scenario, ask the user certain questions and collect answers to them. For example, when registering in any service or when applying for a service

- Games - the bot can send pictures, so you can create any games that do not require an instant response, such as chess or different card games ( example - @anicardplaybot )

---

# Database And Related Files

---

<img width="287" alt="Untitled" src="https://github.com/ArtSN7/telegram-bot/assets/102421671/2c0f131f-b677-4ed1-8249-9289b7d79fe2">


db — to store a single database file
data — to store the classes and functions needed to interact with the database

## ORM-models

Imagine that you have an object at your disposal that is linked to a database. This object takes over all the work of organizing communication with data. All you must do is give it commands: get data, filter them according to a given condition, write data, etc., and converting commands into SQL queries is already the object's concern.

In large applications, ORM (Object-Relational Mapping) technology is often used — a layer that allows working with a database through language objects. In addition, most ORMs allow you to generate database migration scripts to maintain versioning (remotely comparable to git, but for databases), and provide the developer with a lot of other useful functionality. We will use the [sqlalchemy library](https://www.sqlalchemy.org). It can be used not only when creating web applications, but also when developing any programs that interact with databases.

## user.py

```python
import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=True, default=0)

    language = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="en")
```

It describes User class in which there are columns with information from database. For example, field below means that there is a column in the database with names which consists of String values.

```python
name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
```

## all_models.py

```python
from . import user
```

There I am creating a connection “factory” to my database that will work with the engine I need.

## db_session.py

This file will be responsible for connecting to the database and creating a session to work with the database.

```python
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Please, make sure that the path to the database is correct")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqla.create_engine(conn_str, echo=False, pool_pre_ping=True)

    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()
```

First, we import the necessary extensions — the sqlalchemy library itself, then the part of the library that is responsible for the ORM functionality, then the Session object responsible for connecting to the database, and the declarative module — it will help to declare database.

```python
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
```

Then, let’s create two variables: SqlAlchemyBase — some abstract declarative database into which we will later inherit all our models, and __factory, which I will use to get connection sessions to our database.

```python
SqlAlchemyBase = dec.declarative_base()

__factory = None
```

Also, in the db_session file.py I will need to make two more functions global_init and create_session.

- *global_init* takes the database address as input, then checks if I have already created a connection factory (that is, if I am not calling the function for the first time).
I check that I have been given a non-empty database address, and then create a conn_str connection string (it consists of the database type, the address to the database and connection parameters), which I pass to Sqlalchemy. Them I chose the right database engine (engine variable). In my case, it will be an engine for working with SQLite databases.

```python
def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Please, make sure that the path to the database is correct")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqla.create_engine(conn_str, echo=False, pool_pre_ping=True)

    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)
```

- Moving further, the create_session function is needed to get a connection session to our database.

```python
def create_session() -> Session:
    global __factory
    return __factory()
```

Then I need to add import of the contents of the db_session file to the main code:

```python
from data import db_session
```

And before launching the app.run() application, we will add a call to the global initialization of everything related to the database:

```python
db_session.global_init("db/database.db") // you can have anothe path to your database
```

## config.py

```python
from data import keys

config = keys.dict

tg_key = config["tg_key"]

gpt_key = config["gpt_key"]

weather_key = config["weather_key"]

yandex_key = config["yandex_key"]

news_key = config["news_key"]

recipe_key = config["recipe_key"]

serp_key = config["serp_key"]

flight_key = config["flight_key"]
```

This file is needed to get secret values from the file which is only stored localy, as there are keys to the different API’s.

Example of the local file:

```python
dict = {
    "tg_key": "your key",

    "gpt_key": "your key",

    "weather_key": "6f24844bb0dd708bcdbc1bc7fa94bc08",

    "yandex_key":"your key",

    "news_key": "your key",

    "flight_key": "your key",

    "recipe_key": ["your key", "your key", "your key"],

    "serp_key": ["your key", "your key",
                 "your key"]
}
```

---

# Functions

---

## Chat-GPT

```python
# chat-gpt function with open-ai API
from data import config
import openai
import os
import pandas as pd
import time

#open-ai key
openai.api_key = config.gpt_key

#function which provide answer from Open Ai machine
def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}] # creating a request to the server 

    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0,) # send a request 

    return response.choices[0].message["content"] # get a response and return it

#main function which will be used in the bot ( we send a request to it from the main.py (promt - question which we request) )
def question_gpt(promt):

    try:
        response = get_completion(promt) # get response from chat-gpt
        return response # return it to user
    
    except Exception as e: # if there is a mistake, we return text about it 
        print(e)
        return "Error on the server - developers will try to fix it as fast as possible. Sorry for discomfort"

#print(question_gpt("How can I train a dog")) - test
```

Gpt function provides to user an opportunity to ask questions to the Open-AI creation called “Chat-GPT” ( which is currently 3.5 ) . In this function, I use their API, which give me an access to their machine which can analyse data. Therefore, user send a request (question), it goes to question-gpt function, then the question is being sent to the server using get_completion, and in the end being returned to the user.

“Question-gpt" connects message sent by user to bot with Open-AI machine, it gets question and send it to the “get_completion”.  It is also catches possible errors, so there is little chance for program to be terminated.

“get_completion” send a request and then get a response using open-ai library

Lines of code are explained in the code by comments.

<img width="360" alt="Untitled 1" src="https://github.com/ArtSN7/telegram-bot/assets/102421671/4e724af9-6f32-4b0e-8f4c-107e17ba8f0c">


### Links

- [https://platform.openai.com/docs/api-reference/chat/object](https://platform.openai.com/docs/api-reference/chat/object)
- [https://platform.openai.com/docs/guides/gpt/chat-completions-api](https://platform.openai.com/docs/guides/gpt/chat-completions-api)
- [https://blog.enterprisedna.co/how-to-use-chatgpt-for-python/](https://blog.enterprisedna.co/how-to-use-chatgpt-for-python/)
- [https://platform.openai.com/docs/plugins/examples](https://platform.openai.com/docs/plugins/examples)

## Quote

```python
# function which gets a random quote

import requests
from .wikipedia_get_photo import get_wiki_image
import aiohttp
import asyncio
import os

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 

async def quote():
    req = await get_response('https://favqs.com/api/qotd', {}) # getting json file from the api
    data = req # declaring data which is the same as req just to feel comfortable

    author = data["quote"]["author"] # getting the value ( the name of the author )
    txt = data['quote']['body'] # getting text of the quote 
    img_url = await get_wiki_image(author) # getting url of image of author of quote by sending his name to the function 

    # just creating response text for the user which will be send by bot
    text = f'"{txt}" - {author}'

    if img_url == '0': # if there is a mistake on the server or there is no image in the wikipedia, there will be no link returned
        return text, ''

    return text, img_url # returing response and url of image 

if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

```python
import requests
from .wikipedia_get_photo import get_wiki_image
import aiohttp
import asyncio
import os
```

First, I import the function “get_wiki_image” from “wikipedia_get_photo”. This function returns the URL of the photo of the author of the quote. Then I import libraries which are necessary for proper working of my bot.

```python
async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
```

Function “get_response” ( which is always the same in every code ) takes “url,” which is link of the API request, and “params” which will be empty as there are no specific parameters of the request. Then this function, using specific async library, send a request to the server and get a response with JSON file, which will be returned to the main function.

```python
async def quote():
    req = await get_response('https://favqs.com/api/qotd', {}) # getting json file from the api
    data = req # declaring data which is the same as req just to feel comfortable

    author = data["quote"]["author"] # getting the value ( the name of the author )
    txt = data['quote']['body'] # getting text of the quote 
    img_url = await get_wiki_image(author) # getting url of image of author of quote by sending his name to the function 

    # just creating response text for the user which will be send by bot
    text = f'"{txt}" - {author}'

    if img_url == '0': # if there is a mistake on the server or there is no image in the wikipedia, there will be no link returned
        return text, ''

    return text, img_url # returing response and url of image 

```

Function “quote” is the main one in the file. It calls “get_response” function to get json file with all needed data, then duplicate it to the “data” value. Then we get author and text of the photo from the json file.

```python
if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

This part of the code is needed to set up asyncio library.

```python
// This is just an example of the possible json file which is returned after request.

{
  "qotd_date": "2024-02-11T00:00:00.000+00:00",
  "quote": {
    "id": 389,
    "dialogue": false,
    "private": false,
    "tags": [
      "funny"
    ],
    "url": "https://favqs.com/quotes/oscar-wilde/389-some-cause-happ-",
    "favorites_count": 4,
    "upvotes_count": 1,
    "downvotes_count": 0,
    "author": "Oscar Wilde",
    "author_permalink": "oscar-wilde",
    "body": "Some cause happiness wherever they go; others whenever they go."
  }
}
```

After this I call another function (“get_wiki_image”  ) which will find the url of image of author.
Then I create the text which will be used as a response to the user in TG.

### Links

- [https://favqs.com/api](https://favqs.com/api)

## Wikipedia

```python
# getting a photo from wikipedia ( made for quote )

import wikipedia
import requests
import json
import aiohttp
import os
import asyncio

# https://en.wikipedia.org/w/api.php?action=help&modules=query

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 

# returning link of the photo of person whos name is search_term
async def get_wiki_image(search_term):
    try: # using try-except for catching different errors from the server ( as there might be no photo in wikipedia )
        result = wikipedia.search(search_term, results=1) # creating request to the wikipedia servers

        wikipedia.set_lang('en') # setting english as the main language in wikipedia ( so response fro, server will be in english )
        wkpage = wikipedia.WikipediaPage(title=result[0]) # getting first result of this topic from wikipedia
        title = wkpage.title # getting title of this page

        # https://en.wikipedia.org/w/api.php?action=help&modules=query
        # using wikipedia api, I send a response to the server and get a json file of the page
        req = await get_response("http://en.wikipedia.org/w/api.php?",
                                 params={'action': 'query', 'prop': 'pageimages', 'format': 'json',
                                         'piprop': 'original', 'titles': title})

        data = req # declaring data which is the same as req just to feel comfortable

        img_link = list(data['query']['pages'].values())[0]['original']['source'] # getting image link from json file

        return img_link # returning link of the image

    except Exception as e: # if there is a mistake, we will do this:
        return '0' # returning '0' which means that there was no photo found

if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

```python
import wikipedia
import requests
import json
import aiohttp
import os
import asyncio
```

Firstly, I import necessary libraries. “wikipedia” library is used to work with wikipedia pages and last three are used to make program work with async style of programming.

```python
async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
```

There is “get_response” function which has been already described above.

```python
# returning link of the photo of person whos name is search_term
async def get_wiki_image(search_term):
    try: # using try-except for catching different errors from the server ( as there might be no photo in wikipedia )
        result = wikipedia.search(search_term, results=1) # creating request to the wikipedia servers

        wikipedia.set_lang('en') # setting english as the main language in wikipedia ( so response fro, server will be in english )
        wkpage = wikipedia.WikipediaPage(title=result[0]) # getting first result of this topic from wikipedia
        title = wkpage.title # getting title of this page

        # https://en.wikipedia.org/w/api.php?action=help&modules=query
        # using wikipedia api, I send a response to the server and get a json file of the page
        req = await get_response("http://en.wikipedia.org/w/api.php?",
                                 params={'action': 'query', 'prop': 'pageimages', 'format': 'json',
                                         'piprop': 'original', 'titles': title})

        data = req # declaring data which is the same as req just to feel comfortable

        img_link = list(data['query']['pages'].values())[0]['original']['source'] # getting image link from json file

        return img_link # returning link of the image

    except Exception as e: # if there is a mistake, we will do this:
        return '0' # returning '0' which means that there was no photo found
```

In function “get_wiki_image,” “search_term” is the name of the author.

I use TRY-EXCEPT to make sure that there are no mistakes while trying to find page (if there is no page, or there is server error), if there is a mistake, the return will be 0, which in this case ,means nothing.

The idea of the function is to use wikipedia library to find specific page and get a title of it. Then, I need to use API which will collect all the data from this page and return to me a json file. After this, I take URL of the photo from the file and return it.

### Links

- [https://en.wikipedia.org/w/api.php?action=help&modules=query](https://en.wikipedia.org/w/api.php?action=help&modules=query)
- [https://www.educative.io/answers/how-to-get-all-the-image-urls-from-a-wikipedia-page-using-python](https://www.educative.io/answers/how-to-get-all-the-image-urls-from-a-wikipedia-page-using-python)
- [https://www.geeksforgeeks.org/how-to-extract-wikipedia-data-in-python/](https://www.geeksforgeeks.org/how-to-extract-wikipedia-data-in-python/)
- [https://pypi.org/project/Wikipedia-API/](https://pypi.org/project/Wikipedia-API/)
- [https://stackoverflow.com/questions/8363531/accessing-main-picture-of-wikipedia-page-by-api](https://stackoverflow.com/questions/8363531/accessing-main-picture-of-wikipedia-page-by-api)
- [https://docs.aiohttp.org/en/stable/client_quickstart.html](https://docs.aiohttp.org/en/stable/client_quickstart.html)

## Weather

```python
# function which provides informstion about weather in specific location

from data import config
import requests
import asyncio
import aiohttp

app_id = config.weather_key # getting special key for the api
yandex_key = config.yandex_key # getting special key for api

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server

async def moji(txt): # function which retranslate weather description into moji
    dict_m = { # creating data with mojis and their description
        'Thunderstorm': '🌩',
        'Drizzle': '🌦',
        'Rain': '🌧',
        'Snow': '🌨',
        'snow': '🌨',
        'Clear': '☀️',
        'Clouds': '🌥'
    }

    try: # if there is proper moji, we return it
        return dict_m[txt]

    except Exception: # if not, we return basic one
        return '🌫'

async def getting_address(coords): # function gets coordinates ( long and lat )
    try: # trying to catch server mistakes
        req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                                 params={'apikey': yandex_key, 'geocode': f'{coords[0]},{coords[1]}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
        data = req # declaring json file into data variable
        
        # getting address from json file
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]

        return address # returning that address
    
    except Exception as e: # if there are any mistakes
        print(e) # I print mistakes for debugging 
        return "<address was not found>" # returning text
    

async def getting_coords(address): # function which will return long and lat ( needed to use weather function if user input address instead of lat/long )
    req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                             params={'apikey': yandex_key, 'geocode': f'{address}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
    data = req # declaring json file into data variable
        
    # getting lang and lat from json file

    address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
    

    return address # returning that address
    

async def weather_coords(coords): # function which gets information about weather
    # getting weather description at specific place
    req = await get_response("https://api.openweathermap.org/data/2.5/weather?",
                             params={'lat': coords[1], 'lon': coords[0], 'units': 'metric', 'lang': 'en',
                                     'APPID': app_id})

    data = req # declaring json file into data variable

    dictt = {} # creating dictionary which will store reponse data

    # adding to the dictionary weather description from json file
    dictt['weather'] = data['weather'][0]['description'] 
    dictt['temperature'] = data['main']['feels_like'] 

    sp = data['wind']['speed']
    d = data['wind']['deg']

    dictt['wind'] = f"{sp} m/sec ; {d} deg"
    dictt['visibility'] = str(int(data['visibility']) / 1000)
    dictt['humidity'] = data['main']['humidity']

    dictt['png'] = await moji(data['weather'][0]['main']) # getting emoji for the weather description

    address = await getting_address(coords) # getting user address

    # creating response to the user which will be sent by bot 
    txt = f"Weather at {address} :\n\n {dictt['weather'].capitalize()} {dictt['png']} \n\n Feels like: {dictt['temperature']} C \n\n Wind: {dictt['wind']} \n\n Visibility: {dictt['visibility']} km \n\n Humidity: {dictt['humidity']}%\n"

    return txt # returning response

async def weather_address(coords): # function which gets information about weather
    try: # trying to find weather at input address 

        lon, lat = await getting_coords(coords) # getting lat and lon for weather api request

        # getting weather description at specific place
        req = await get_response("https://api.openweathermap.org/data/2.5/weather?",
                                 params={'lat': lat, 'lon': lon, 'units': 'metric', 'lang': 'en',
                                         'APPID': app_id})

        data = req # declaring json file into data variable

        dictt = {} # creating dictionary which will store reponse data

        # adding to the dictionary weather description from json file
        dictt['weather'] = data['weather'][0]['description'] 
        dictt['temperature'] = data['main']['feels_like'] 

        sp = data['wind']['speed']
        d = data['wind']['deg']

        dictt['wind'] = f"{sp} m/sec ; {d} deg"
        dictt['visibility'] = str(int(data['visibility']) / 1000)
        dictt['humidity'] = data['main']['humidity']

        dictt['png'] = await moji(data['weather'][0]['main']) # getting emoji for the weather description

        address = await getting_address((lon, lat)) # getting user address

        # creating response to the user which will be sent by bot 
        txt = f"Weather at {address} :\n\n {dictt['weather'].capitalize()} {dictt['png']} \n\n Feels like: {dictt['temperature']} C \n\n Wind: {dictt['wind']} \n\n Visibility: {dictt['visibility']} km \n\n Humidity: {dictt['humidity']}%\n"

        return txt # returning response
    
    except Exception as e: # if there is a mistake and response was not created
        print(e) # debugging 
        return "Sorry, but the weather at your address was not found. Please, check accuracy of the address!"
```

```python
# function which provides informstion about weather in specific location

from data import config
import requests
import asyncio
import aiohttp

app_id = config.weather_key # getting special key for the api
yandex_key = config.yandex_key # getting special key for api

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server
```

In the beggining, as it has been already done before in other functions, I import extensions which will allow my program works properly and then write “get_response” function.

```python
app_id = config.weather_key # getting special key for the api
yandex_key = config.yandex_key # getting special key for api
```

There are also two keys which allow me to work with APIs

```python
async def getting_address(coords): # function gets coordinates ( long and lat )
    try: # trying to catch server mistakes
        req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                                 params={'apikey': yandex_key, 'geocode': f'{coords[0]},{coords[1]}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
        data = req # declaring json file into data variable
        
        # getting address from json file
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]

        return address # returning that address
    
    except Exception as e: # if there are any mistakes
        print(e) # I print mistakes for debugging 
        return "<address was not found>" # returning text
    

async def getting_coords(address): # function which will return long and lat ( needed to use weather function if user input address instead of lat/long )
    req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                             params={'apikey': yandex_key, 'geocode': f'{address}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
    data = req # declaring json file into data variable
        
    # getting lang and lat from json file

    address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
    

    return address # returning that address
```

There are two functions which are connected to the Yandex API ( [https://yandex.com/dev/](https://yandex.com/dev/) ). They are needed to work with user location.

****Yandex*** is a technology ***company*** that builds intelligent products and services powered by machine learning.

*“getting_coords”* is needed to get longitude and latitude from user’s input. Function gets address and then, using Yandex API, finds longitude and latitude.

*“getting_address”* is remarkably like the function above, but it reflects it – it gets longitude and latitude and then finds the address.

```python
async def moji(txt): # function which retranslate weather description into moji
    dict_m = { # creating data with mojis and their description
        'Thunderstorm': '🌩',
        'Drizzle': '🌦',
        'Rain': '🌧',
        'Snow': '🌨',
        'snow': '🌨',
        'Clear': '☀️',
        'Clouds': '🌥'
    }

    try: # if there is proper moji, we return it
        return dict_m[txt]

    except Exception: # if not, we return basic one
        return '🌫'
```

There is also “moji” function which was made to make output less formal by adding proper mojis to the output according to the returned data.

```python
async def weather_coords(coords): # function which gets information about weather
    # getting weather description at specific place
    req = await get_response("https://api.openweathermap.org/data/2.5/weather?",
                             params={'lat': coords[1], 'lon': coords[0], 'units': 'metric', 'lang': 'en',
                                     'APPID': app_id})

    data = req # declaring json file into data variable

    dictt = {} # creating dictionary which will store reponse data

    # adding to the dictionary weather description from json file
    dictt['weather'] = data['weather'][0]['description'] 
    dictt['temperature'] = data['main']['feels_like'] 

    sp = data['wind']['speed']
    d = data['wind']['deg']

    dictt['wind'] = f"{sp} m/sec ; {d} deg"
    dictt['visibility'] = str(int(data['visibility']) / 1000)
    dictt['humidity'] = data['main']['humidity']

    dictt['png'] = await moji(data['weather'][0]['main']) # getting emoji for the weather description

    address = await getting_address(coords) # getting user address

    # creating response to the user which will be sent by bot 
    txt = f"Weather at {address} :\n\n {dictt['weather'].capitalize()} {dictt['png']} \n\n Feels like: {dictt['temperature']} C \n\n Wind: {dictt['wind']} \n\n Visibility: {dictt['visibility']} km \n\n Humidity: {dictt['humidity']}%\n"

    return txt # returning response

async def weather_address(coords): # function which gets information about weather
    try: # trying to find weather at input address 

        lon, lat = await getting_coords(coords) # getting lat and lon for weather api request

        # getting weather description at specific place
        req = await get_response("https://api.openweathermap.org/data/2.5/weather?",
                                 params={'lat': lat, 'lon': lon, 'units': 'metric', 'lang': 'en',
                                         'APPID': app_id})

        data = req # declaring json file into data variable

        dictt = {} # creating dictionary which will store reponse data

        # adding to the dictionary weather description from json file
        dictt['weather'] = data['weather'][0]['description'] 
        dictt['temperature'] = data['main']['feels_like'] 

        sp = data['wind']['speed']
        d = data['wind']['deg']

        dictt['wind'] = f"{sp} m/sec ; {d} deg"
        dictt['visibility'] = str(int(data['visibility']) / 1000)
        dictt['humidity'] = data['main']['humidity']

        dictt['png'] = await moji(data['weather'][0]['main']) # getting emoji for the weather description

        address = await getting_address((lon, lat)) # getting user address

        # creating response to the user which will be sent by bot 
        txt = f"Weather at {address} :\n\n {dictt['weather'].capitalize()} {dictt['png']} \n\n Feels like: {dictt['temperature']} C \n\n Wind: {dictt['wind']} \n\n Visibility: {dictt['visibility']} km \n\n Humidity: {dictt['humidity']}%\n"

        return txt # returning response
    
    except Exception as e: # if there is a mistake and response was not created
        print(e) # debugging 
        return "Sorry, but the weather at your address was not found. Please, check accuracy of the address!"
```

There are two main functions in the code which provide weather information.

“weather_coords” gets longitude and latitude and then goes to the OpenWeatherMap server with a request. Then, after getting response, program analyses json file with the response and takes needed data. Then it creates a response to the user and in the end sends it.

“weather_address” works in the same way, but instead of getting longitude and latitude, it gets address and then, using “getting_coords” function, it gets longitude and latitude.

```python
#------------------------------------------------------------------
# weather buttond
btn_loc = KeyboardButton('SEND A LOCATION', request_location=True) # button which will ask user to send a location
markup_weather_loc = ReplyKeyboardMarkup([[btn_loc]], one_time_keyboard=True, resize_keyboard=True) # function which will show this button

coords_button = KeyboardButton('/coordinates')
address_button = KeyboardButton('/address')
markup_weather_options = ReplyKeyboardMarkup([[address_button],[coords_button]], one_time_keyboard=True, resize_keyboard=True) # showing weather o
```

In the [main.py](http://main.py/) I create buttons which will help user to work with this function. One will be connected to the location sending by using innate GPS tracker. And another two buttons will be just choices of how to send location.

```python
#------------------------------------------------------------------
# weather function

async def weather_command(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose how you will send us your location ( by sending text address or by sharing your location using button )")

    await update.message.reply_html(answer, reply_markup=markup_weather_options) # asking how user will send location

async def weather_command_coords(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "To analyse data, you need to send your current location (use button below)")

    

    await update.message.reply_html(answer, reply_markup=markup_weather_loc) # asking user to send coordinates by innate telegram function
    return 1

async def weather_command_address(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "To analyse data, you need to send address")

    await update.message.reply_html(answer, reply_markup=ReplyKeyboardRemove()) # asking user to send coordinates by text ( King' school canterbury , for example )
    return 1

async def weather_command_response_coords(update, context): # function which works with longitude and latitude 
    long, lang = update.message.location.longitude, update.message.location.latitude # getting user coordinates 
    func = weather.weather_coords((long, lang)) # calling function
    answer = await func # getting response 

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)

    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to the user
    return ConversationHandler.END # ending conversation

async def weather_command_response_address(update, context): # function which works with address
    func = weather.weather_address(update.message.text) # calling function
    answer = await func # getting answer

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)

    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to the user
    return ConversationHandler.END # ending conversation 

#------------------------------------------------------------------
```

There are 5 functions above which are all used in conversation.

```python
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
```

Conversation starts with “weather” command, it asks user how he wants to send location. If user chooses coordinates, the program will ask him a permission to send his location which is recorded by phone. If user chooses address, he will need to input address in a message and send it to bot. By the end of this manipulations, bot sends information about weather in chosen location.

### Links

- [https://yandex.ru/dev/weather/doc/dg/concepts/about.html](https://yandex.ru/dev/weather/doc/dg/concepts/about.html)
- [https://openweathermap.org/](https://openweathermap.org/)
- [https://openweathermap.org/current](https://openweathermap.org/current)
- [https://yandex.com/dev/maps/geocoder/](https://yandex.com/dev/maps/geocoder/)
- [https://yandex.com/dev/geocode/doc/en/request](https://yandex.com/dev/geocode/doc/en/request)

## News

```python
# function which show news

import requests
import os
import asyncio
import aiohttp
from data import config

key = config.news_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 

async def get_news(category, lang): # function which gets news by category

    req = await get_response('https://newsapi.org/v2/top-headlines?',
                             params={'language': lang, 'category': category, 'pageSize': 21, 'apiKey': key}) # making a request where county is a country of news
    
    data = req # copying json file to the data variable 

    text = 'We have found something for you: \n\n'

    try:
        for i in range(0, 5): # searching for the first 5 news 
            title = data['articles'][i]['title'] # getting title of the article
            s_url = data['articles'][i]['url'] # getting link to the article

 
            text += f'----------------\n\nTITLE: {title}\n\nURL: {s_url} \n\n----------------'

        return text

    except Exception as e: # if there is a mistake

        if text == 'We have found something for you: \n\n':
            return 'Nothing was found :(\n\nTry to change language to see more news'
        return text

async def get_spec_news(about): # function which get news by specific topic 

    try: # trying to catch any server error
        text = 'We have found something for you: \n\n'

        req = await get_response('https://newsapi.org/v2/top-headlines?', params={'q': about, 'apiKey': key}) # making a request

        data = req # copying json file to the data variable 

        if not data: # if there is nothing found , I raise an error
            raise Exception
        
        

        for i in range(0, 5): # searching for the first 5 news 

            title = data['articles'][i]['title'] # getting title of the article
            s_url = data['articles'][i]['url'] # getting link to the article

            text += f'----------------\n\nTITLE: {title}\n\nURL: {s_url} \n\n----------------'

        return text # returning response 

    except Exception: # if there is an error, I send a message that there are no news or I output all news which I was able to find before error appeared

        if text == 'We have found something for you: \n\n': # if there was no news found, I would return text below
            return 'No news around this field was found :('

        return text # returning response
```

```python
# function which show news

import requests
import os
import asyncio
import aiohttp
from data import config

key = config.news_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server
```

Same procedure of importing libraries as in the previous functions

```python
async def get_news(category, lang): # function which gets news by category

    req = await get_response('https://newsapi.org/v2/top-headlines?',
                             params={'language': lang, 'category': category, 'pageSize': 21, 'apiKey': key}) # making a request where county is a country of news
    
    data = req # copying json file to the data variable 

    text = 'We have found something for you: \n\n'

    try:
        for i in range(0, 5): # searching for the first 5 news 
            title = data['articles'][i]['title'] # getting title of the article
            s_url = data['articles'][i]['url'] # getting link to the article

 
            text += f'----------------\n\nTITLE: {title}\n\nURL: {s_url} \n\n----------------'

        return text

    except Exception as e: # if there is a mistake

        if text == 'We have found something for you: \n\n':
            return 'Nothing was found :(\n\nTry to change language to see more news'
        return text
```

Function “get_news” gets category, which is one of the topics of news, and language, which is language set up by user (default – English). It sends a request to the server, and then gets a response with 21 news. Then it sends a text with title and link to this news to the user.

```python
async def get_spec_news(about): # function which get news by specific topic 

    try: # trying to catch any server error
        text = 'We have found something for you: \n\n'

        req = await get_response('https://newsapi.org/v2/top-headlines?', params={'q': about, 'apiKey': key}) # making a request

        data = req # copying json file to the data variable 

        if not data: # if there is nothing found , I raise an error
            raise Exception
        
        

        for i in range(0, 5): # searching for the first 5 news 

            title = data['articles'][i]['title'] # getting title of the article
            s_url = data['articles'][i]['url'] # getting link to the article

            text += f'----------------\n\nTITLE: {title}\n\nURL: {s_url} \n\n----------------'

        return text # returning response 

    except Exception: # if there is an error, I send a message that there are no news or I output all news which I was able to find before error appeared

        if text == 'We have found something for you: \n\n': # if there was no news found, I would return text below
            return 'No news around this field was found :('

        return text # returning response
```

The same idea is in the “get_spec_news” which gets only topic by user. Then it tries to find related to this topic news and in the end sends text with titles and URLs of the news.

```python
#------------------------------------------------------------------
# news buttons 
reply_keyboard_news = [['/general_news'], ['/specific_news']]
markup_news = ReplyKeyboardMarkup(reply_keyboard_news, one_time_keyboard=True, resize_keyboard=True)
```

Declaing buttons which are going to be connected to the function.

```python
#------------------------------------------------------------------
# news function 
async def news_command(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose the type of news you want to see.")

    await update.message.reply_html(answer, reply_markup=markup_news) # chose between general and specific

async def general_news(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose topic you are intersted in.")

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
    await update.message.reply_html(answer, reply_markup=markup_news_topic) # if user had chosen general news, he would need to choose topic
    
    await update.message.reply_text('', reply_markup=ReplyKeyboardRemove()) # removing keyboard eventhough there will be error
```

This part of the functions shows the topics and user must pick one. Then it shows news.

```python
#------------------------------------------------------------------
# function which work with all inline keyboard buttons
async def inline_buttons(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language
```

```python
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
```

As they are made as inlinebuttons, then this function will call general news functions depends on the pressed button

```python
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
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Enter the topic you are interested in (for example, Microsoft)")
    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return 1

async def specific_news_response(update, context):

    func = news.get_spec_news(update.message.text)
    answer = await func
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
```

All general news is built in the same way – they get language from database, then call the function, and send a response from this function to user.

```python
async def specific_news(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Enter the topic you are interested in (for example, Microsoft)")
    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return 1

async def specific_news_response(update, context):

    func = news.get_spec_news(update.message.text)
    answer = await func
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
```

Specific news (where user must write what he wants to find) are built as a conversation function (the same as it was with gpt function).

### Links

- [https://newsapi.org](https://newsapi.org/)
- [https://newsapi.org/docs/endpoints/](https://newsapi.org/docs/endpoints/)

## Recipes

```python

#------------------------------------------------------------------
# function which work with all inline keyboard buttons
async def inline_buttons(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    # cuisine types
        
    if query.data == 'italian':
        answer = await italian_cuisine() # getting response

        answer = await translater.translating(lang, answer)

        await query.edit_message_text(text=f"{answer}") # sending response to the user

    if query.data == 'british':
        answer = await british_cuisine()

        answer = await translater.translating(lang, answer)

        await query.edit_message_text(text=f"{answer}")

    if query.data == 'chinese':
        answer = await chinese_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'european':
        answer = await european_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'french':
        answer = await french_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'german':
        answer = await german_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'greek':
        answer = await greek_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'indian':
        answer = await indian_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'japanese':
        answer = await japanese_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'korean':
        answer = await korean_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'mexican':
        answer = await mexican_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'thai':
        answer = await thai_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")
```

As they are made as inlinebuttons, then this function will call general news functions depends on the pressed button

```python
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
```

In the main file I declare all the functions as usual, there are 2 conversation handlers which help me to work with “dish_name” function and “ingredients” function.

```python
#------------------------------------------------------------------
# recipes function
async def recipes_command(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose by which parameter you want to choose recipe")

    await update.message.reply_text(answer, reply_markup=markup_recipe_type) # chose between different types of request

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

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose the type of cuisine you are interested in.")

    await update.message.reply_text(answer, reply_markup=markup_cuisine_type) # chose between different cuisines
```

We need to add next functions in the main file, they show Inline Buttons.

```python
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
```

This commands start functions

Now let’s have a look on the code of the function 

```python
# function which shows recipes

import requests
import os
import asyncio
import aiohttp
import random

from data import config

key = config.recipe_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 

async def get_plan(id): # function which gets plan how to 
    req = await get_response(f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions', params={"apiKey": key[random.randint(0, 2)]})
    data = req

    text = "" # our response
    
    for i in data[0]["steps"]: # i means information about each step of cooking
        text += f"\n-- {i['step']}\n" # i['step'] - description of the step , we just add them to our response

    return text

async def get_ingredient(id): # function which gets infor abour required ingredienrs
    req = await get_response(f'https://api.spoonacular.com/recipes/{id}/ingredientWidget.json', params={"apiKey": key[random.randint(0, 2)]})
    data = req

    text = "" # our response
    
    for i in data["ingredients"]: # i means information about each ingredient of cooking
        name = i["name"] # getting name of ingredient
        value = f"{i['amount']['metric']['value']} ({i['amount']['metric']['unit']})" # getting how many of this is needed
        text += f"{name} - {value}\n"

    return text

async def get_cuisine(category): # function which gets recipe by cuisine

    req = await get_response('https://api.spoonacular.com/recipes/complexSearch?',
                             params={"cuisine": category, "apiKey": key[random.randint(0, 2)], "number": 10}) # making a request 
    
    data = req # copying json file to the data variable 
    
    data = data["results"][random.randint(0, 9)] # getting random recipe from file

    id = data["id"] # getting id of the dish in database
    title = data["title"] # getting title of the dish
    img = data["image"] # getting url of the image of the dish

    return id, title, img # returning id of the dish, title of the dish and url of the image of the dish

async def get_rec_by_cuisine(cuisine): # function which calls other function to create a full response
    try:
        id, title, img = await get_cuisine(cuisine) # getting id, title and link to the image
        plan = await get_plan(id) # getting plan how to cook it
        ing = await get_ingredient(id) # getting needed ingredients

        response = f"{title}\n\n---------\n\nIngredients:\n\n{ing}\n---------\n\nHow to cook:\n\n{plan}" # creating response

        return response, img # returning response and url of image 
    
    except Exception as e:
        return "Sorry, nothing was found", "..."

async def get_name(name):
    req = await get_response('https://api.spoonacular.com/recipes/complexSearch?',
                             params={"query": name, "apiKey": key[random.randint(0, 2)], "number": 10}) # making a request 
    
    data = req # copying json file to the data variable 
    
    data = data["results"][random.randint(0, 9)] # getting random recipe from file

    id = data["id"] # getting id of the dish in database
    title = data["title"] # getting title of the dish
    img = data["image"] # getting url of the image of the dish

    return id, title, img # returning id of the dish, title of the dish and url of the image of the dish

async def get_rec_by_name(cuisine): # function which calls other function to create a full response
    try:
        id, title, img = await get_name(cuisine) # getting id, title and link to the image
        plan = await get_plan(id) # getting plan how to cook it
        ing = await get_ingredient(id) # getting needed ingredients

        response = f"{title}\n\n---------\n\nIngredients:\n\n{ing}\n---------\n\nHow to cook:\n\n{plan}" # creating response

        return response, img # returning response and url of image 
    except Exception as e:
        return "Sorry, nothing was found", "..."

async def get_by_ingredient(ingredients):
    try: # trying to catch any errors

        par = '' # making ingredients in a proper format
        if len(ingredients.split(",")) == 1: # if there is only one ingredient
            par = ingredients.split(",")[0]
        else: # if there any many of them
            par += ingredients.split(",")[0]
            for i in ingredients.split(",")[1:-1]:
                par += f",+{i}"

        req = await get_response('https://api.spoonacular.com/recipes/findByIngredients?',
                                 params={"ingredients": par, "apiKey": key[random.randint(0, 2)], "number": 10}) # making a request 
    
        data = req # copying json file to the data variable 

    
        data = data[random.randint(0, len(data) - 1)] # getting first recipe from file

        id = data["id"] # getting id of the dish in database
        title = data["title"] # getting title of the dish
        img = data["image"] # getting url of the image of the dish

        return id, title, img # returning id of the dish, title of the dish and url of the image of the dish
    
    except Exception as e: # if there are any mistakes, or nothing will be found
        return "Sorry, nothing was found", "..."

async def get_rec_by_ingredients(ing): # function which calls other function to create a full response
    try:
        id, title, img = await get_by_ingredient(ing) # getting id, title and link to the image
        plan = await get_plan(id) # getting plan how to cook it
        ing = await get_ingredient(id) # getting needed ingredients

        response = f"{title}\n\n---------\n\nIngredients:\n\n{ing}\n---------\n\nHow to cook:\n\n{plan}" # creating response

        return response, img # returning response and url of image 
    except Exception as e:
        return "Sorry, nothing was found", "..."
```

```python
# function which shows recipes

import requests
import os
import asyncio
import aiohttp
import random

from data import config

key = config.recipe_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server
```

Well-known process there.

```python
async def get_plan(id): # function which gets plan how to 
    req = await get_response(f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions', params={"apiKey": key[random.randint(0, 2)]})
    data = req

    text = "" # our response
    
    for i in data[0]["steps"]: # i means information about each step of cooking
        text += f"\n-- {i['step']}\n" # i['step'] - description of the step , we just add them to our response

    return text

async def get_ingredient(id): # function which gets infor abour required ingredienrs
    req = await get_response(f'https://api.spoonacular.com/recipes/{id}/ingredientWidget.json', params={"apiKey": key[random.randint(0, 2)]})
    data = req

    text = "" # our response
    
    for i in data["ingredients"]: # i means information about each ingredient of cooking
        name = i["name"] # getting name of ingredient
        value = f"{i['amount']['metric']['value']} ({i['amount']['metric']['unit']})" # getting how many of this is needed
        text += f"{name} - {value}\n"

    return text
```

These two functions are needed to get plan how to cook dish and what ingredients are needed to do this. They both get ID and using it find this information using API.

```python
async def get_cuisine(category): # function which gets recipe by cuisine

    req = await get_response('https://api.spoonacular.com/recipes/complexSearch?',
                             params={"cuisine": category, "apiKey": key[random.randint(0, 2)], "number": 10}) # making a request 
    
    data = req # copying json file to the data variable 
    
    data = data["results"][random.randint(0, 9)] # getting random recipe from file

    id = data["id"] # getting id of the dish in database
    title = data["title"] # getting title of the dish
    img = data["image"] # getting url of the image of the dish

    return id, title, img # returning id of the dish, title of the dish and url of the image of the dish

async def get_rec_by_cuisine(cuisine): # function which calls other function to create a full response
    try:
        id, title, img = await get_cuisine(cuisine) # getting id, title and link to the image
        plan = await get_plan(id) # getting plan how to cook it
        ing = await get_ingredient(id) # getting needed ingredients

        response = f"{title}\n\n---------\n\nIngredients:\n\n{ing}\n---------\n\nHow to cook:\n\n{plan}" # creating response

        return response, img # returning response and url of image 
    
    except Exception as e:
        return "Sorry, nothing was found", "..."
```

“get_cuisine” function is needed to find recipe by the cuisine type, for example, if user wants to eat something from Italian menu, he chooses this type of cuisine and then script tries to find any dish from the required cuisine.

“get_rec_by_cuisine” function makes a response for the user, it gets id of the dish and then goes to another two functions and gets information from them, then it summarizes it and sends to user.

### Link

- [https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions](https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions)
- [https://spoonacular.com/food-api/docs#Cuisines](https://spoonacular.com/food-api/docs#Cuisines)
- [https://spoonacular.com/food-api/docs#Ingredients-by-ID](https://spoonacular.com/food-api/docs#Ingredients-by-ID)
- [https://spoonacular.com/food-api/docs#Search-Recipes-Complex](https://spoonacular.com/food-api/docs#Search-Recipes-Complex)
- [https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients](https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients)

## Events

```python
#------------------------------------------------------------------
# evetns buttons
markup_event_loc = ReplyKeyboardMarkup([[btn_loc]], one_time_keyboard=True, resize_keyboard=True) # function which will show this button

reply_keyboard_events_type = [['/Real'], ['/Virtual']]
markup_events_type = ReplyKeyboardMarkup(reply_keyboard_events_type, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard_events_date = [['/Today'], ['/Tomorrow'], ['/This_week'], ['/Next_week'], ['/All_dates']]
markup_events_date = ReplyKeyboardMarkup(reply_keyboard_events_date, one_time_keyboard=True, resize_keyboard=True)
#------------------------------------------------------------------
```

```python
#------------------------------------------------------------------
# events function

async def events_command(update, context):
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "To find events near you, please, send us your location!")

    await update.message.reply_html(answer, reply_markup=markup_event_loc) # sending button with location
    return 1

async def events_response(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose the type of event!")

    long, lat = update.message.location.longitude, update.message.location.latitude # getting user coordinates 

    context.user_data['long'] = long # storing longitude
    context.user_data['lat'] = lat # storing latitude 

    
    await update.message.reply_html(answer, reply_markup=markup_events_type) # asking user to choose type of event ( Real or Virtual )

    return ConversationHandler.END # finishing conversation

async def real_event_type(update, context): # if event type is real
    context.user_data['type'] = "Real" # storing information about event type

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, now choose the date of event!")

    await update.message.reply_html(answer, reply_markup=markup_events_date) # asking to choose date of event
    

async def virtual_event_type(update, context): # if event type is virtual
    context.user_data['type'] = "Virtual" # storing information about event type

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, now choose the date of event!")

    await update.message.reply_html(answer, reply_markup=markup_events_date) # asking to choose date of event

 # dates of event
async def today_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "today") # calling main function from events.py

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)

    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def tomorrow_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "tomorrow") # calling main function from events.py

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def this_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "week") # calling main function from events.py
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def next_week_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "next_week") # calling main function from events.py
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove()) # sending response to user

async def all_event(update, context): 
    answer = await events.main_events((context.user_data['long'], context.user_data['lat']), context.user_data['type'], "all") # calling main function from events.py
    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, answer)
    await update.message.reply_text(f"{answer}", reply_markup=ReplyKeyboardRemove())  # sending response to user
```

```python
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
```

In the main code this function is declared with buttons and conversation handlers. So, in the main code I declare buttons which will be helpful for the taking user’s answers. After, in the main file I write functions which asks questions to the user, and then in the conversation form they summarise all the answers in the dictionary and then call the function which will return the response.

Code of the whole functions is showed below:

```python
# function that shows events near the place

import requests
import aiohttp
import asyncio
import os
import random
from data import config

yandex_key = config.yandex_key # getting special key for api
serp_key = config.serp_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
        

async def getting_address(coords): # function gets coordinates ( long and lat )
    try: # trying to catch server mistakes
        req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                                 params={'apikey': yandex_key, 'geocode': f'{coords[0]},{coords[1]}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
        data = req # declaring json file into data variable
        
        # getting address from json file
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"]["Locality"]["LocalityName"] # getting town

        return address # returning that address
    
    except Exception as e: # if there are any mistakes
        print(e)
        return "<address was not found>" # returning text

async def searching_events(type_of_req, town, htichips): # if type_of_req == 1, then there is no htichips, else, there is htichips
    try:
        if type_of_req == 2:
            req = await get_response("https://serpapi.com/search.json?", 
                                     params={'engine': 'google_events', 'api_key': serp_key[random.randint(0, 2)], 'hl': 'en', 'q': f'Events in {town}', 'htichips': htichips})
        else:
            req = await get_response("https://serpapi.com/search.json?", 
                                     params={'engine': 'google_events', 'api_key': serp_key[random.randint(0, 2)], 'hl': 'en', 'q': f'Events in {town}'})
            
        data = req 

        response = ""

        for num, i in enumerate(data["events_results"]): # num - count of events, i - data of event
            if num >= 5: # if there is enought info about event, I return response
                return response
            
            # adding info about new event to response
            response += f'{i["title"].upper()}\n\n"{i["description"]}"\n\nWHEN: {i["date"]["when"]}\n\nAddress: {i["address"][0]}\n\n{i["link"]}\n------------------------\n\n'
        
        return response # returning response
        
    except Exception as e: # if there are any mistakes
        print(e)
        return "Nothing was found"

async def main_events(coords, type, date):
    town = await getting_address(coords) # finding town 

    if type == 'Virtual': # if user had set up specific type of event
        htichips = f"event_type:{type},date:{date}" # creating second part of future request
    else:
        htichips = f"date:{date}" # creating second part of future request ( without event_type )

    if date == 'all':
        return await searching_events(1, town, htichips) # returning answer to the user
    
    return await searching_events(2, town, htichips) # returning answer to the user

if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

```python
# function that shows events near the place

import requests
import aiohttp
import asyncio
import os
import random
from data import config

yandex_key = config.yandex_key # getting special key for api
serp_key = config.serp_key

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
```

In the [events.py](http://events.py/) there is as always “get_respones” function and import of libraries.

```python
async def getting_address(coords): # function gets coordinates ( long and lat )
    try: # trying to catch server mistakes
        req = await get_response("https://geocode-maps.yandex.ru/1.x/?",
                                 params={'apikey': yandex_key, 'geocode': f'{coords[0]},{coords[1]}', 'lang': 'en_US', 'format': 'json'}) # sending request to the server
    
        data = req # declaring json file into data variable
        
        # getting address from json file
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"]["Locality"]["LocalityName"] # getting town

        return address # returning that address
    
    except Exception as e: # if there are any mistakes
        print(e)
        return "<address was not found>" # returning text
```

“getting_address” function returns town by analysing coordinates of the user. It is important function as the main request includes name of the town. ( functions was used in the weather command )

```python
async def searching_events(type_of_req, town, htichips): # if type_of_req == 1, then there is no htichips, else, there is htichips
    try:
        if type_of_req == 2:
            req = await get_response("https://serpapi.com/search.json?", 
                                     params={'engine': 'google_events', 'api_key': serp_key[random.randint(0, 2)], 'hl': 'en', 'q': f'Events in {town}', 'htichips': htichips})
        else:
            req = await get_response("https://serpapi.com/search.json?", 
                                     params={'engine': 'google_events', 'api_key': serp_key[random.randint(0, 2)], 'hl': 'en', 'q': f'Events in {town}'})
            
        data = req 

        response = ""

        for num, i in enumerate(data["events_results"]): # num - count of events, i - data of event
            if num >= 5: # if there is enought info about event, I return response
                return response
            
            # adding info about new event to response
            response += f'{i["title"].upper()}\n\n"{i["description"]}"\n\nWHEN: {i["date"]["when"]}\n\nAddress: {i["address"][0]}\n\n{i["link"]}\n------------------------\n\n'
        
        return response # returning response
        
    except Exception as e: # if there are any mistakes
        print(e)
        return "Nothing was found"
```

“searching_events” makes a request to the server and creates a response.

```python
async def main_events(coords, type, date):
    town = await getting_address(coords) # finding town 

    if type == 'Virtual': # if user had set up specific type of event
        htichips = f"event_type:{type},date:{date}" # creating second part of future request
    else:
        htichips = f"date:{date}" # creating second part of future request ( without event_type )

    if date == 'all':
        return await searching_events(1, town, htichips) # returning answer to the user
    
    return await searching_events(2, town, htichips) # returning answer to the user
```

“main_event” is needed only to connect all these two functions and then return final response t

### Links

- [https://serpapi.com/google-events-api](https://serpapi.com/google-events-api)

## Flight

```python
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
```

In the main code function was declared in a straightforward way – it is 3 step conversation with the user.

```python
#------------------------------------------------------------------
# flight function

async def flight_command_0(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, send us airport code from your ticket. Just to remind, EK104 ( on the photo ) is a airport code (EK) and flight number(104)")

    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    url = "https://www.flightright.co.uk/wp-content/uploads/sites/2/2023/02/where-can-i-find-my-flight-number.jpg"
    await context.bot.send_photo(update.message.chat_id, url, caption="") # seding example of ticket
    return 1 # showing what function must be called next

async def flight_command_1(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Thank you, now send us you flight code, which is also on your ticket.")
    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    context.user_data['airport'] = update.message.text.upper() # storing airport name , upper is needed if user inputed in a wrong format
    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove()) # asking for the flight code
    return 2 # showing what function must be called next

async def flight_command_2(update, context):
    context.user_data['flight'] = update.message.text # storing flight code

    answer = await flight.get_flight_info(context.user_data["flight"], context.user_data["airport"]) # calling function which will provide info about this flight 

    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove()) # sending response to the user

    context.user_data.clear() # deleting all information about this user

    return ConversationHandler.END # finishing conversation, so the user next message won't be connected to this function
```

In the first function I ask user for the airport code and show program that it need to move to the second function. In the second function I store user’s answer in the database and ask question about flight number and show program that it need to call third function. And finally, in the third function I get user’s response and call function from the “fligh” file which will find information about user’s flight.

Main code is a bit more complicated

```python
# function which provides information about your flight

import requests
import aiohttp
import asyncio
import os
import datetime
from data import config

flight_key = config.flight_key # getting special key for api

# link_ticket = "https://www.flightright.co.uk/wp-content/uploads/sites/2/2023/02/where-can-i-find-my-flight-number.jpg" - just link of the ticket's photo

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
        
async def get_flight_info(num, name):

    try: # trying to catch any errors 

        date = datetime.date.today().strftime('%Y%m%d') # getting today's date as there is date requirement in the request

        req = await get_response(f"https://api.flightapi.io/airline/{flight_key}?",
                                 params={"num": num, "name" : name, "date": date}) # sending request to the server

        # getting information about departure

        time_sch_of_departure = req[0]['departure'][0]['Scheduled Time:']
        time_est_of_departure = req[0]['departure'][0]['Estimated Time:']
        airport_of_departure = req[0]['departure'][0]['Airport:']
        terminal_of_departure = ""
        gate = req[0]['departure'][0]['Terminal - Gate:'].split(" - ")[1]
        terminal = req[0]['departure'][0]['Terminal - Gate:'].split(" - ")[0].split(" ")[1]
        terminal_of_departure = f'{terminal} | {gate}'

        # getting information about arrival
        time_sch_of_arrival = req[1]['arrival'][0]['Scheduled Time:']
        time_est_of_arrival = req[1]['arrival'][0]['Estimated Time:']
        airport_of_arrival = req[1]['arrival'][0]['Airport:']
        terminal_of_arrival = req[1]['arrival'][0]['Terminal - Gate:'].split(" ")[1] # choosing only number of terminal

        # creating response to user

        response_dep = f'Departure information:\n\n  -Airport: {airport_of_departure}\n\n  -Terminal | Gate: {terminal_of_departure}\n\n  -Scheduled time: {time_sch_of_departure}\n\n  -Estimated time: {time_est_of_departure}\n\n'
        response_ar = f'------\n\nArrival information:\n\n  -Airport: {airport_of_arrival}\n\n  -Terminal: {terminal_of_arrival}\n\n  -Scheduled time: {time_sch_of_arrival}\n\n  -Estimated time: {time_est_of_arrival}\n\n'
    
        return response_dep + response_ar # returning response to the user
    
    except Exception as e: # if there are any mistakes
        print(e)
        return "Sorry, your flight was not found or it's already flew away. Please, check accuracy of data."

if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# asyncio.run(get_flight_info("207", 'AZ')) - just testing function
```

```python
# function which provides information about your flight

import requests
import aiohttp
import asyncio
import os
import datetime
from data import config

flight_key = config.flight_key # getting special key for api

# link_ticket = "https://www.flightright.co.uk/wp-content/uploads/sites/2/2023/02/where-can-i-find-my-flight-number.jpg" - just link of the ticket's photo

async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server 
```

Well-known procedure

```python
async def get_flight_info(num, name):

    try: # trying to catch any errors 

        date = datetime.date.today().strftime('%Y%m%d') # getting today's date as there is date requirement in the request

        req = await get_response(f"https://api.flightapi.io/airline/{flight_key}?",
                                 params={"num": num, "name" : name, "date": date}) # sending request to the server

        # getting information about departure

        time_sch_of_departure = req[0]['departure'][0]['Scheduled Time:']
        time_est_of_departure = req[0]['departure'][0]['Estimated Time:']
        airport_of_departure = req[0]['departure'][0]['Airport:']
        terminal_of_departure = ""
        gate = req[0]['departure'][0]['Terminal - Gate:'].split(" - ")[1]
        terminal = req[0]['departure'][0]['Terminal - Gate:'].split(" - ")[0].split(" ")[1]
        terminal_of_departure = f'{terminal} | {gate}'

        # getting information about arrival
        time_sch_of_arrival = req[1]['arrival'][0]['Scheduled Time:']
        time_est_of_arrival = req[1]['arrival'][0]['Estimated Time:']
        airport_of_arrival = req[1]['arrival'][0]['Airport:']
        terminal_of_arrival = req[1]['arrival'][0]['Terminal - Gate:'].split(" ")[1] # choosing only number of terminal

        # creating response to user

        response_dep = f'Departure information:\n\n  -Airport: {airport_of_departure}\n\n  -Terminal | Gate: {terminal_of_departure}\n\n  -Scheduled time: {time_sch_of_departure}\n\n  -Estimated time: {time_est_of_departure}\n\n'
        response_ar = f'------\n\nArrival information:\n\n  -Airport: {airport_of_arrival}\n\n  -Terminal: {terminal_of_arrival}\n\n  -Scheduled time: {time_sch_of_arrival}\n\n  -Estimated time: {time_est_of_arrival}\n\n'
    
        return response_dep + response_ar # returning response to the user
    
    except Exception as e: # if there are any mistakes
        print(e)
        return "Sorry, your flight was not found or it's already flew away. Please, check accuracy of data."
```

This is the main function of the file which returns information about the flight. It gets as parameters num (flight number) and name (airport code). Then it goes to the server with these parameters (date of the flight is always today’s date) and after this I analyse json file from the response to get needed information. Then I summarise all the data and return response to the user.

### Links

- [https://docs.flightapi.io](https://docs.flightapi.io/)

## User’s profile

This function is needed to change different settings in the bot. It gets current language of the user from database and ask him if he want to change it. After pushing buttons language will be updated

```python
#------------------------------------------------------------------
# profile change buttons 
reply_keyboard_profile_change = [['/change_language']]
markup_profile_change = ReplyKeyboardMarkup(reply_keyboard_profile_change, one_time_keyboard=True, resize_keyboard=True)
```

There is only one button which allows user to change a language of output

```python
#------------------------------------------------------------------
# Profile connected function 

async def user_profile(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

    answer = await translater.translating(lang, "Please, choose what you want to change")

    await update.message.reply_html(answer, reply_markup=markup_profile_change)

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

    answer = await translater.translating(lang, f"Please, choose language to which you want to switch. Your current language is '{lang}'")

    await update.message.reply_html(answer, reply_markup=markup_profile_language)
```

It asks user to choose between few inline buttons, when user makes a choice, specific functions is being called and then language connected to the user in the database is being changed.

```python
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
```

This functions are responsible for such change. 

## Translator

```python
# function which translates text 

from deep_translator import GoogleTranslator # importing library

# en it de fr ru es - list of languages
# https://pypi.org/project/deep-translator/ - link to the library documentation

async def translating(lang, text): # lang - user's language to which I need to translate; text - text which need to be translated
    try: # trying to catch an error
        translated = GoogleTranslator(source='english', target=lang).translate(text) # creating an object where source is a language of given text and
        # target is a language to which library needs to translate; text - it is just a text that need to be translated 
        return translated # returning translated text 
    except Exception as e: # catching an error
        return "Sorry, error in translation :(" # returning message if there is any errors
```

This function is used to translate text before sending it to the user.

It takes language of the user to which text must be translated and text itself as arguments, then translates it and returns the translated text.

### Links

- https://pypi.org/project/deep-translator/

---

# Main Code

---

```python
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

from functions import gpt, quote, weather, news, recipes, events, flight, translater
```

First of all, in the main code I import all the libraries and files storing other functions.

```python
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
```

Then I declare buttons for the functions.

```python
#------------------------------------------------------------------
# function which work with all inline keyboard buttons
async def inline_buttons(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

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

        answer = await translater.translating(lang, answer)

        await query.edit_message_text(text=f"{answer}") # sending response to the user

    if query.data == 'british':
        answer = await british_cuisine()

        answer = await translater.translating(lang, answer)

        await query.edit_message_text(text=f"{answer}")

    if query.data == 'chinese':
        answer = await chinese_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'european':
        answer = await european_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'french':
        answer = await french_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'german':
        answer = await german_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'greek':
        answer = await greek_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'indian':
        answer = await indian_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'japanese':
        answer = await japanese_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'korean':
        answer = await korean_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'mexican':
        answer = await mexican_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

    if query.data == 'thai':
        answer = await thai_cuisine()
        answer = await translater.translating(lang, answer)
        await query.edit_message_text(text=f"{answer}")

#------------------------------------------------------------------
```

There is a special “inline” function which works only with inline buttons ( check [GUIDE.md](http://GUIDE.md) to understand what I am talking about ). It checks the name of the inline button and call specific functions after.

```python
#------------------------------------------------------------------
# help function wich explains abilities of all functions in the bot 
async def help_command(update, context):

    user = update.effective_user # getting user info from telegram
    id = user.id #getting user id

    db_sess = db_session.create_session() # creating connection with database
    person = db_sess.query(User).filter(User.tg_id == id).first() # searching for the data in the database which has the same id as the tg user
    
    lang = person.language # getting language

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

.......
//MORE FUNCTIONS THERE
.......

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
```

Then there is a huge block of different functions which make the program work.

```python
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
```

Function called “main” is the most important there, it stored all the conversation handlers, in other words, it commands what to do after different user interactions.

```python
#------------------------------------------------------------------
if __name__ == '__main__': # part of the code that set up the environmet 
    
    db_session.global_init("code/db/data.db") # connecting database in the main code code/db/data.db - path to reach the file

    if os.name == 'nt': # if os is windows
        # essential part which will set up "asyncio" library for the specific system
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        

    main() # starting main code
```

This part just sets up a database and calls function “main” to start my bot.
