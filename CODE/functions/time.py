# function which provides information about time

import os
import asyncio
import requests
import aiohttp


async def get_response(url, params): # function which send a request to the server; url - http request, params - parameters of http request
    # https://docs.aiohttp.org/en/stable/client_quickstart.html
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp: # creating aysnc requset to the server
            return await resp.json() # getting and returning json file which is a response from the server


async def time(name):
    if os.name == 'nt': # code which forces asyncio work properly on the windows machines
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    req = await get_response("https://timeapi.io/api/Time/current/zone?", params={'timeZone': name})

    data = req

    time = data["time"]

    return time


#def main():
#return asyncio.run(time())