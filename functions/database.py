import os
import asyncio
import aiomysql

from dotenv import load_dotenv

load_dotenv("../.env")
#loop     : An asyncio loop
#request  : A string representing the SQL request
#database : A string representing the database
#args     : A tuple representing the values in order of appearance for the sql request

@asyncio.coroutine
async def executeRequest(loop, request, database, args=None):
    try:
        connection = await aiomysql.connect(
            host="localhost",
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            db=database,
            loop=loop
        )

        #Execute the sql request
        async with connection.cursor() as cur:
            if args is not None:
                await cur.execute(request, args)
            else:
                await cur.execute(request)

            print(cur.description)
            r = await cur.fetchall()
            print(r)

        connection.close()
    except Exception as e:
        print(e)
        print("Une erreur est arrivée avec la bdd!")