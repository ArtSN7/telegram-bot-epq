# getting a photo from wikipedia ( made for quote )


import wikipedia
import requests
import json
import aiohttp
import os
import asyncio


# https://en.wikipedia.org/w/api.php?action=help&modules=query

async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


# возвращает ссылку на изображение из википедии
async def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results=1)

        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title

        req = await get_response("http://en.wikipedia.org/w/api.php?",
                                 params={'action': 'query', 'prop': 'pageimages', 'format': 'json',
                                         'piprop': 'original', 'titles': title})

        data = req

        img_link = list(data['query']['pages'].values())[0]['original']['source']

        return img_link

    except Exception as e:
        return '0'


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())