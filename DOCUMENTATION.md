# DOCUMENTATION

---

# Content map:

---

**[Before Reading](https://github.com/ArtSN7/telegram-bot/blob/main/DOCUMENTATION.md#before-reading)**

[Before Reading](https://www.notion.so/Before-Reading-9d5991c6102e4f3796632d4b2cd6d2e0?pvs=21) 

[Introduction](https://www.notion.so/Introduction-eacfeaed09c54a8b9f00fdd79e74b5cc?pvs=21) 

     [Telegram](https://www.notion.so/Telegram-d25ee15b51a2410398786dd9bcf53119?pvs=21) 

[What is a telegram-bot](https://www.notion.so/What-is-a-telegram-bot-9be1c2e77702404aa2daaefa9049ba82?pvs=21) 

[What problems can be solved by telegram-bot](https://www.notion.so/What-problems-can-be-solved-by-telegram-bot-5251199a809e451a9d7b4fee83dcec57?pvs=21) 

[Database And Related Files](https://www.notion.so/Database-And-Related-Files-7721097b92eb4f78a32dc9bf563f6fc0?pvs=21) 

[ORM-models](https://www.notion.so/ORM-models-837921ebee644af1894c5a2d5bd67ab3?pvs=21) 

[user.py](https://www.notion.so/user-py-c8ed060d4b9a47afb6b157a32f15b8ad?pvs=21) 

[all_models.py](https://www.notion.so/all_models-py-f8786e2e91ff4ab08b966cb0d1dd136a?pvs=21) 

[db_session.py](https://www.notion.so/db_session-py-39b3fbdd962e4e43a0004b6f69dc724d?pvs=21) 

[config.py](https://www.notion.so/config-py-ded297f98a3c403480e18d2ed93d0b5f?pvs=21) 

---

# Before Reading

---

**GIT-HUB link - [https://github.com/ArtSN7/telegram-bot](https://github.com/ArtSN7/telegram-bot)**

**Documentation of how to write telegram-bots with theory and examples you might find in the repository in the file GUIDE.md. It will be useful for you to check it first before reading documentation, as it will help you deeply understand how does it all work.**

---

# Introduction

---

## Telegram

Telegram is a messenger (messaging program) implemented using a client-server architecture. Using the server to create a dialogue between two clients, Telegram sends text messages through it or directly, as well as images, videos, or documents in other formats.

## What is a telegram-bot

A Telegram bot is a special user whose behaviour is controlled by some program. Technically, it makes no difference to the server whether a given user is a human or a bot: to the server, both clients look the same.

## What problems can be solved by telegram-bot

Everything, it is limited only by imagination. Here are some examples:

- Autoresponders - all situations where an unambiguous answer to a request is required. For example, the bot can provide telephone numbers and other contacts of the organization, its working hours, or provide other background information upon request

- Interface for accessing web services - the bot can make requests to various [APIs](https://www.ibm.com/topics/api) *(application programming interface, which is a set of definitions and protocols for building and integrating application software)* and send responses in the form of telegram messages.

- Action scenarios - the bot can go through any scenario, ask the user certain questions and collect answers to them. For example, when registering in any service or when applying for a service

- Games - the bot can send pictures, so you can create any games that do not require an instant response, such as chess or different card games ( example - @anicardplaybot )

---

# Database And Related Files

---

<img width="287" alt="Untitled" src="https://github.com/ArtSN7/telegram-bot/assets/102421671/040ec921-e407-494f-92b7-de58fd6b8092">


db — to store a single database file
data — to store the classes and functions needed to interact with the database

## ORM-models

Imagine that you have an object at your disposal that is linked to a database. This object takes over all the work of organizing communication with data. All you must do is give it commands: get data, filter them according to a given condition, write data, etc., and converting commands into SQL queries is already the object's concern.

In large applications, ORM (Object-Relational Mapping) technology is often used — a layer that allows working with a database through language objects. In addition, most ORMs allow you to generate database migration scripts to maintain versioning (remotely comparable to git, but for databases), and provide the developer with a lot of other useful functionality. We will use the [sqlalchemy library](https://www.sqlalchemy.org). It can be used not only when creating web applications, but also when developing any programs that interact with databases.

## user.py

```python
import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=True, default=0)

    language = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="en")
```

It describes User class in which there are columns with information from database. For example, field below means that there is a column in the database with names which consists of String values.

```python
name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
```

## all_models.py

```python
from . import user
```

There I am creating a connection “factory” to my database that will work with the engine I need.

## db_session.py

This file will be responsible for connecting to the database and creating a session to work with the database.

```python
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Please, make sure that the path to the database is correct")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqla.create_engine(conn_str, echo=False, pool_pre_ping=True)

    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()
```

First, we import the necessary extensions — the sqlalchemy library itself, then the part of the library that is responsible for the ORM functionality, then the Session object responsible for connecting to the database, and the declarative module — it will help to declare database.

```python
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
```

Then, let’s create two variables: SqlAlchemyBase — some abstract declarative database into which we will later inherit all our models, and __factory, which I will use to get connection sessions to our database.

```python
SqlAlchemyBase = dec.declarative_base()

__factory = None
```

Also, in the db_session file.py I will need to make two more functions global_init and create_session.

- *global_init* takes the database address as input, then checks if I have already created a connection factory (that is, if I am not calling the function for the first time).
I check that I have been given a non-empty database address, and then create a conn_str connection string (it consists of the database type, the address to the database and connection parameters), which I pass to Sqlalchemy. Them I chose the right database engine (engine variable). In my case, it will be an engine for working with SQLite databases.

```python
def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Please, make sure that the path to the database is correct")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqla.create_engine(conn_str, echo=False, pool_pre_ping=True)

    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)
```

- Moving further, the create_session function is needed to get a connection session to our database.

```python
def create_session() -> Session:
    global __factory
    return __factory()
```

Then I need to add import of the contents of the db_session file to the main code:

```python
from data import db_session
```

And before launching the app.run() application, we will add a call to the global initialization of everything related to the database:

```python
db_session.global_init("db/database.db") // you can have anothe path to your database
```

## config.py

```python
from data import keys

config = keys.dict

tg_key = config["tg_key"]

gpt_key = config["gpt_key"]

weather_key = config["weather_key"]

yandex_key = config["yandex_key"]

news_key = config["news_key"]

recipe_key = config["recipe_key"]

serp_key = config["serp_key"]

flight_key = config["flight_key"]
```

This file is needed to get secret values from the file which is only stored localy, as there are keys to the different API’s.

Example of the local file:

```python
dict = {
    "tg_key": "your key",

    "gpt_key": "your key",

    "weather_key": "6f24844bb0dd708bcdbc1bc7fa94bc08",

    "yandex_key":"your key",

    "news_key": "your key",

    "flight_key": "your key",

    "recipe_key": ["your key", "your key", "your key"],

    "serp_key": ["your key", "your key",
                 "your key"]
}
```

---
