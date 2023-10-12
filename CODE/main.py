import asyncio
import os
import aiohttp
from data import db_session





def main():
    pass





# part of the code that set up the environmet 
if __name__ == '__main__':
    
    db_session.global_init("db/database.db") # connecting database in the main code


    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        # essential part which will set up "asyncio" library for the specific system

    main() # starting main code 