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