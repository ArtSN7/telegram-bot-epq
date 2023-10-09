import asyncio
import os
import aiohttp
from data import db_session





def main():
    pass





# part of the code that starts the programm
if __name__ == '__main__':
    db_session.global_init("db/database.db")
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()