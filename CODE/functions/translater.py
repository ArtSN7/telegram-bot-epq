# function which translates text 

from deep_translator import GoogleTranslator

# en it de fr ru es
# https://pypi.org/project/deep-translator/

async def translating(lang, text): # lang - user's language to which I need to translate; text - text which need to be translated
    try: # trying to catch an error
        translated = GoogleTranslator(source='english', target=lang).translate(text)
        return translated
    except Exception as e: # catching an error
        return "Sorry, error in translation :(" # returning message if there is any errors




