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