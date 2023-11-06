# function which translates text 

from translate import Translator

# en it de fr ru es
# https://pypi.org/project/translate/

async def translating(lang, text): # lang - user's language to which I need to translate; text - text which need to be translated
    try: # trying to catch an error
        translator= Translator(to_lang=lang) # creating an object and declare language to which I need to translate 
        translation = translator.translate(text) # translating text 
        return translation # returning what I have translated 
    except Exception as e: # catching an error
        return "Sorry, error in translation :(" # returning message if there is any errors


# asyncio.run(translating('ru', "How to cook some bread"))