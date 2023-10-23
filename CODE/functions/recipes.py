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
        return "Sorry, there is an error on the server. Try again later :(", "..."


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
        return "Sorry, there is an error on the server. Try again later :(", "..."


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
        return "Sorry, there is an error on the server. Try again later :(", "..."


async def get_rec_by_ingredients(ing): # function which calls other function to create a full response
    try:
        id, title, img = await get_by_ingredient(ing) # getting id, title and link to the image
        plan = await get_plan(id) # getting plan how to cook it
        ing = await get_ingredient(id) # getting needed ingredients

        response = f"{title}\n\n---------\n\nIngredients:\n\n{ing}\n---------\n\nHow to cook:\n\n{plan}" # creating response

        return response, img # returning response and url of image 
    except Exception as e:
        return "Sorry, there is an error on the server. Try again later :(", "..."