# chat-gpt function with open-ai API

import openai
import os
import pandas as pd
import time

#open-ai key
openai.api_key = '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'


#function which provide answer from Open Ai machine
def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}] # creating a request to the server 

    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0,) # send a request 

    return response.choices[0].message["content"] # get a response and return it


#main function which will be used in the bot ( we send a request to it from the main.py (promt - question which we request) )
def question_gpt(promt):

    try:
        response = get_completion(promt) # get response from chat-gpt
        return response # return it to user
    
    except Exception: # if there is a mistake, we return text about it 
        return "Error on the server - developers will try to fix it as fast as possible. Sorry for discomfort"


#print(question_gpt("How can I train a dog")) - test