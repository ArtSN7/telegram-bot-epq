## Library installation

```python
pip install python-telegram-bot[ext] --upgrade

```

This library has really decent documentation ( **https://python-telegram-bot.readthedocs.io/en/stable )** . 

In addition, there are a number of example in their GIT-HUB ( https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/README.md ), by studying which you can understand how to use it correctly and what typical operations look like.

The **python-telegram-bot library version 20** is written using Asyncio , so it might be beneficial to understand how all of this works. ( https://docs.python.org/3/library/asyncio.html )


## Echo-bot

Let's look at the simplest example.

**Echo-bot** is a bot that simply sends the received text message back. Usually such bots are used by the system to check the connection.

The entrance to the bot program is Application. This is an object that receives incoming messages from the telegram server. The task of this object is to organize network interaction between the client and the server.

The received messages are passed by the Application to the Dispatcher, which is automatically created inside the Application. The dispatcher is responsible for calling message handlers.

The dispatcher stores message handlers — handlers. These are functions, or rather, coroutines that have a certain signature, receiving messages of already certain types with information about which users these messages came from.

A message receiving and transmitting cycle is implemented inside the Application.

Thus, the bot program should:

1. Create an object by passing it the token received from @BotFather.  
2. Get coroutines-handlers for messages and commands and register them.
3. Start the cycle of receiving and processing messages.
4. Wait for the end / interruption of the program.

The example of code, that shows theory above:

```python
# importing classes 
import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN

# Defining a message handler function.
# It has two parameters, the updater that received the message and the context - additional information about the message.
async def echo(update, context):
    # The Updater class object has a message field,
    # being the object of the message.
    # Message has a text field containing the text of the received message,
    # as well as the reply_text(str) method,
    # sending a response to the user from whom the message was received.
    await update.message.reply_text(update.message.text)

def main():
		# Creating an Application object.
    # Instead of the word "TOKEN", you need to place the token received from
    # @BotFather

    application = Application.builder().token(BOT_TOKEN).build()

    # Creating a message handler of the filters.TEXT type
    # from the asynchronous echo() function described above
    # After registering the handler in the application
    # this asynchronous function will be called when a message is received
    # with the "text" type, i.e. text messages.
    text_handler = MessageHandler(filters.TEXT, echo)

    # registering the handler in the application.
    application.add_handler(text_handler)

    # run the application
    application.run_polling()

# Run the main() function if the script is running.
if __name__ == '__main__':
    main()

```

## Processing commands

```python
text_handler = MessageHandler(filters.TEXT, echo)

```

In addition to messages, the bot can receive commands, inline requests and some other objects. All possible options are listed in the documentation ( https://docs.python-telegram-bot.org/en/stable/telegram.ext.handlers-tree.html )

**Command**

A command is a special message starting with the "/" character. The command assumes some specific action of the bot.

There are several standard commands. For example:

- **/start** (the command started communicating with the bot, usually it sends a message about the capabilities of the bot and how to communicate with it)
- **/help** (in response to the command, the bot sends instructions for working with itself)

The commands that the bot responds to can be any, depending on the purpose of the bot.

Let's add handlers for the **/start** and **/help** commands.

By analogy with message processing, a command handler must be created from a function and registered in the application.

```python
# adding new object from library
from telegram.ext import CommandHandler

# Let's write the appropriate functions.
# Their signature and behavior are similar to text message handlers.
async def start(update, context):
    """it sends the message when /start was called"""
    user = update.effective_user
    await update.message.reply_html(rf"Hello {user.mention_html()}!",)

async def help_command(update, context):
    """it sends the message when /help was called"""
    await update.message.reply_text("I can do nothing")

# Register them in the app before
# by registering a text message handler.
# The first parameter of the Command Handler constructor I
# is the name of the team.
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

```

Also, let’s change line: 

`text_handler = MessageHandler(filters.TEXT, echo)` 

to the line:

 `text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)`

, in this way, we will indicate that the echo handler will be used only for processing text messages, but not for processing commands.

## Creating a keyboard in the user's dialog

One of the possible tasks of the bot is to provide various background information. We already know that special commands can be created to implement this behavior. However, for a user to enter commands is a relatively long matter. And if he came to the bot from a mobile phone, then it's just inconvenient.

In order to cope with this difficulty, the API has a mechanism for pre-marked responses. If it is assumed that the interlocutor will use any commands of the bot, you can output a set of buttons, each of which sends a specific command to the bot. This makes interaction with the bot faster, more convenient and clearer.

Let's look at an example. We will develop a bot directory that will provide some background information about the company. To begin with: address, phone number, website and opening hours.

We will create four commands: /address, /phone, /site, / work_time, each of which will simply send the user a text message with the necessary information.

```python
# writing functions, nothing special
async def help(update, context):
    await update.message.reply_text(
        "I am ur assistant")

async def address(update, context):
    await update.message.reply_text(
        "Address: King's School Canterbury")

async def phone(update, context):
    await update.message.reply_text("Phone: +44 (0)1223 337733")

async def site(update, context):
    await update.message.reply_text(
        "Web: https://www.youtube.com")

async def work_time(update, context):
    await update.message.reply_text(
        "Work time: from 8 am to 6pm every day")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("help", help))
    application.run_polling()

```

Now let's create a keyboard with four buttons for these commands. To do this, use the class ReplyKeyboardMarkup. To use it, you need to import it from the telegram module:

```python
from telegram import ReplyKeyboardMarkup

```

The first parameter of the ReplyKeyboardMarkup constructor is a list of buttons. Note: in the example, the list consists of two sublists, each of which defines a row of buttons.

```python
reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

```

If you pass all four lines in the form of a single list, you will get a keyboard with four buttons in one line.

The one_time_keyboard parameter specifies whether to hide the keyboard after pressing one of the buttons.

In order for the keyboard to appear in the user's dialog, you need to add it as the reply_markup parameter to the reply_text function. Then, in addition to the text, the API will forward the marked-up keyboard.

```python
async def start(update, context):
    await update.message.reply_text(
          "What do you want to see?", reply_markup=markup)

```

A keyboard that has been transferred once will remain in the dialog in a collapsed or expanded form until a new one is sent to the client or it is explicitly indicated that the transferred keyboard should be deleted.

To delete it, you need to pass an object of a special class as the value of the reply_markup parameter: ReplyKeyboardRemove.

```python
from telegram import ReplyKeyboardRemove

async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

application.add_handler(CommandHandler("close", close_keyboard))

```

## Creating dialog scripts

Discussing the scope of bots, I talked about different scenarios in which the user is consistently asked questions, and the bot collects answers and does something further with them. How is this different from what I did before? Mainly because in the previous example I did not store the context of the "conversation". That is, the bot "answered" one question and immediately "forgot" who asked him what.

A scenario is a series of questions or replicas in which the bot "remembers" what questions it has already asked the user, what answers it has received and what to ask next.

There is a special dialog handler for creating scripts in telegram-bot-python: ConversationHandler.

Let's look at an example of its use.

```python
    conv_handler = ConversationHandler(
        # The entry point to the dialog.
        # In this case, the /start command. It asks the first question.
        entry_points=[CommandHandler('start', start)],

        # Option with two handlers filtering text messages.
        states={
            # The function reads the answer to the first question and asks the 
            # second one.
            1:[MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            # The function reads the answer to the second question and ends the        
            # dialog.
            2:[MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },
        # Dialog breakpoint. In this case, the /stop command.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

```

In normal handlers there is only one function. The dispatcher calls it if the filter condition in the handler is met. The function itself returns None, or, in other words, does not return any value.

Here I register a handler consisting of other handlers. How does such a mechanism work?

At the very beginning of the program, only the start handler described in the entry_points parameter is active. Exactly the same as if I was without creation ConversationHandler would just register it in the Dispatcher, as I did earlier.

However, unlike the previous cases, the start handler will have to return a value. And this value will tell the Dispatcher which handler to choose for **subsequent** messages.

In my case, it will return 1, and this will indicate to the Dispatcher that the handler from the states parameter with index 1 — `states[1]` should be applied to the next message. That is, the one that is associated with the `first_response()` function. It turns out that, in addition to processing the /start command itself, it also tells the Dispatcher how to work further.

In turn, `first_response()` will return the value 2. After that, the Dispatcher will apply a handler from `states[2]` to the following messages.

To end the dialog, you need to return the special value `ConversationHandler.END'. After that, the Dispatcher will, as at the very beginning, try to apply the entry_points handler.

The handler from the fallbacks parameter is active all the time the dialog is running and is deactivated after exiting it. It is used to interrupt the dialog.

Let's write the functions mentioned above.

```python
async def start(update, context):
    await update.message.reply_text("Please, could you answer some questions?"
                                    "Where do you live?")

    # Number is the key in the states dictionary —
    # the second parameter of the conversationhandler.
    # It indicates what's next for messages from this user
    # the handler states[1] must respond.
    return 1

async def first_response(update, context):
    locality = update.message.text
    await update.message.reply_text(
        f"What's the weather look like at {locality}?")

    # The following text message will be processed
    # by the states handler[2]
    return 2

async def second_response(update, context):
    weather = update.message.text # user's response 
    await update.message.reply_text("Thank you!")
    return ConversationHandler.END  # The end of conversation

# this function will stop conversation, if it's called
async def stop(update, context): 
    await update.message.reply_text("Bye")
    return ConversationHandler.END

```

## Transmitting user data in a script

It is often necessary to store not only the user's previous response, but also a larger amount of data received during the dialogue.

For storing and transmitting such data, telegram supports a special context.user_data dictionary.

Let’s modify our bot so that at the end of the dialog it can *send greetings* to the city that the user specified in the first response.

```python
# Added the user_data dictionary to the parameters.
async def first_response(update, context):
    # store response in the dictionary
    context.user_data['locality'] = update.message.text
    await update.message.reply_text(
        f"What's the weather look like {context.user_data['locality']}?")
    return 2

async def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    await update.message.reply_text(
        f"Thank for sharing info about {context.user_data['locality']}!")
    context.user_data.clear()  # clear user's data (deleting all info from dict)
    return ConversationHandler.END

```

## Using the HTTP API in telegram bots

As you understand, chatbots can work not only with the data that is in their immediate availability, but also request information from the API of third-party services. The idea is simple: let's teach a telegram bot to "walk" into the HTTP API, turning user requests into http requests to the API, and broadcast API responses in a user-friendly and understandable form.

Let's create a bot that sends him information about the object at the request of the user.

Since my telegram bot works in asynchronous mode, then use the standard requests library ( https://pypi.org/project/requests ) to access third-party APIs incorrectly. I will use the asynchronous aiohttp library ( [https://docs.aiohttp.org](https://docs.aiohttp.org/) )

So, my functions will look like this:

```python
async def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"

    # I use get_response to send a request to the server
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text})
    
    await.update.message.reply_text(response) 

# function which allow user to send request to APIs
async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()
```
