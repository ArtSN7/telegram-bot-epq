# function which get a random quote

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
    text = f"'{txt}',- {author}" 

    if img_url == '0': # if there is a mistake on the server or there is no image in the wikipedia, there will be no link returned
        return text, ''

    return text, img_url # returing response and url of image 


if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())