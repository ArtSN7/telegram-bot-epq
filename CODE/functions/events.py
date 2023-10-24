# function that shows events near the place

import requests
import aiohttp
import asyncio
import os
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
                                     params={'engine': 'google_events', 'api_key': serp_key, 'hl': 'en', 'q': f'Events in {town}', 'htichips': htichips})
        else:
            req = await get_response("https://serpapi.com/search.json?", 
                                     params={'engine': 'google_events', 'api_key': serp_key, 'hl': 'en', 'q': f'Events in {town}'})
            
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