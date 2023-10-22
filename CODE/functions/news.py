# function which 

import requests
import os
import asyncio
import aiohttp
from data import config

key = config.news_key

categories_list = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
# ar de en es fr he it nl no pt ru sv ud zh - languages


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
            return 'Oops, smth went wrong... :(\n\nPlease, try again later!'
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
            return 'Oops, smth went wrong... :( \n\nPlease, try again later!'

        return text # returning response 