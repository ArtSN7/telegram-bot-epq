# function which get a quote


import requests
from .wikipedia_get_photo import get_wiki_image
import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def quote():
    req = await get_response('https://favqs.com/api/qotd', {})
    data = req

    author = data["quote"]["author"]
    txt = data['quote']['body']
    img_url = await get_wiki_image(author)

    text = f"{author} - \n\n"
    text += txt

    if img_url == '0':
        return text, 'Image was not found :('

    return text, img_url


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())