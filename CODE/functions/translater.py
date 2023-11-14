# function which translates text 

from deep_translator import GoogleTranslator # importing library

# en it de fr ru es - list of languages
# https://pypi.org/project/deep-translator/ - link to the library documentation

async def translating(lang, text): # lang - user's language to which I need to translate; text - text which need to be translated
    try: # trying to catch an error
        translated = GoogleTranslator(source='english', target=lang).translate(text) # creating an object where source is a language of given text and
        # target is a language to which library needs to translate; text - it is just a text that need to be translated 
        return translated # returning translated text 
    except Exception as e: # catching an error
        return "Sorry, error in translation :(" # returning message if there is any errors




