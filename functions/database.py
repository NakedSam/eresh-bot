import os
import asyncio
import aiomysql

from dotenv import load_dotenv

load_dotenv("../.env")
#loop     : An asyncio loop
#request  : A string representing the SQL request
#database : A string representing the database
async def executeRequest(loop, request, database, channel):
    connection = await aiomysql.connect(
        host="localhost",
        port=3306,
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        db=database,
        loop=loop
    )

    async with conn.cursor() as cur:
        await cur.execute(request)
        print(cur.description)
        r = await cur.fetchall()
        print(r)

    conn.close()