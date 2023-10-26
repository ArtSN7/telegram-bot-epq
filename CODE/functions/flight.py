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
        return "Sorry, your flight was not found. Please, check accuracy of data."


if os.name == 'nt': # code which forces asyncio work properly on the windows machines
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# asyncio.run(get_flight_info("207", 'AZ')) - just testing function
