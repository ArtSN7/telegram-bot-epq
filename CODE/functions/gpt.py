# key: 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

# chat-gpt function with open-ai API

import openai
import os
import pandas as pd
import time

openai.api_key = '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'

#main func

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0,)

    return response.choices[0].message["content"]



# how to use 

prompt = "Name a capital of England" 
response = get_completion(prompt)
print(response)