import os
import asyncio
import aiomysql

#loop        : An asyncio loop
#request     : A string representing the SQL request
#database    : A string representing the database
#args        : A tuple representing the values in order of appearance for the sql request
#credentials : A dictionnary representing the redentials to access the database

@asyncio.coroutine
async def select(loop, request, database, credentials, args=None):
    try:
        #Connect to the database
        connection = await aiomysql.connect(
            host="localhost",
            port=3306,
            user=credentials["user"],
            password=credentials["password"],
            db=database,
            loop=loop
        )

        #Execute the sql request
        async with connection.cursor() as cur:
            if args is not None:
                await cur.execute(request, args)
            else:
                await cur.execute(request)

            r = await cur.fetchall()

        connection.close()

        #If there's no row that correspond
        if len(r) == 0:
            return None
            
        return r

    except Exception as e:
        print(e)
        print("Une erreur est arrivée avec la bdd lors d'un SELECT !")

async def executeRequest(loop, request, database, credentials, args=None):
    if request.startswith("SELECT"):
        await select(loop, request, database, credentials, args)
    else:
        raise RequestTypeError("Type de requête non supporté")

class RequestTypeError(TypeError):
    '''The SQL Request is of an unknown type'''