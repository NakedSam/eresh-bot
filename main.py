import discord
import os
import json
import asyncio
import aiomysql
import functions

from classes import prompt
from functions import database

from discord.ext import commands, tasks

CREDENTIALS_PATH = "./credentials.json"

credentials = None

with open(CREDENTIALS_PATH) as f:
    credentials = json.load(f)

dbCredentials = {
    "user": credentials["dbUser"],
    "password": credentials["dbPass"]
}

if __name__ == "__main__":
    description="```Un bot multifonction```"
    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix="$", description=description, intents=intents)


    with open("./prompts.json") as f:
        bot.prompts = json.load(f)

    with open("./databaseStructure.json") as f:
        bot.databaseStructure = json.load(f)

    @bot.event
    async def on_ready():
        print("Eresh est prête Master !")
        bot.blindtests = {}
        bot.ongoingBlindtestPrompts = {}
        bot.blindtestPromptsDict = {}
        bot.blindtestPromptMessagesDict = {}
        bot.blindtestChannelChoicePromptsDict = {}

    @bot.command(name="hi", aliases=["hello", "salut"])
    async def _hi(ctx):
        """
        Salut l'utilisateur
        """

        await ctx.send("o/")

    @bot.command(name="blindtest", aliases=["bt"])
    async def _blindtest(ctx):
        """
        Prépare un blind test
        """
            
        #Starts a new connection to the database
        blindtestLoop = asyncio.get_event_loop()

        blindtestRequest = f"SELECT server_btChannel FROM {bot.databaseStructure['serversTable']} WHERE server_id='{ctx.guild.id}'"
        #We check if there's already the server in the list by making a request to the database
        selectResponse = await database.select(
            loop=blindtestLoop, 
            request=blindtestRequest, 
            database=bot.databaseStructure["serversDatabase"],
            credentials=dbCredentials
        )

        #If there's no server returned or the server doesn't have an channel id for the blindtest, 
        #it means they haven't picked a blind test channel yet so we ask them to
        if selectResponse == None or selectResponse[0][0] :
            channelChoicePrompt = prompt.Prompt(
                bot=bot,
                guildId=ctx.guild.id,
                descriptions=[bot.prompts["blindtestChoicePrompt"]],
                emojisLists=["1️⃣", "2️⃣", "🚫"],
                promptType="blindtestChannelChoice",
                channel=ctx.channel,
                functions=(None)
            )

            #channelChoiceMessage = await channelChoicePrompt.showPrompt()

        #If we have an ongoing blindtest, we mention that a blind test is already ongoing
        if ctx.guild.id in bot.blindtests and bot.blindtests["ongoingBlindtest"]:
            await ctx.channel.send("Un blind test est déjà en cours !")           
        #Else we start the prompts chain and we set the blindtest as ongoing as well as putting the prompt
        else:
            btPrompt = prompt.Prompt(
                bot=bot, 
                guildId=ctx.guild.id, 
                descriptions=[bot.prompts["blindtestModePrompt"]],
                emojisLists=[["1️⃣", "2️⃣", "3️⃣", "🚫"]], 
                promptType="blindtest",
                channel=ctx.channel,
                functions=(None)
            )

            bot.blindtests[ctx.guild.id] = {"ongoingBlindtest" : True}

            promptMessage = await btPrompt.showPrompt()
            #We create the prompt and add it to the prompts dictionnary stored on the bot
            blindtestPromptToAdd = {
                "prompt": btPrompt   
            }

            bot.blindtestPromptsDict[promptMessage.guild.id] = blindtestPromptToAdd
            bot.blindtestPromptMessagesDict[promptMessage.id] = promptMessage.id

    #When a reaction is added, we perform some checks
    @bot.event
    async def on_raw_reaction_add(self, payload=discord.RawReactionActionEvent):
        #If it's the bot reaction, we do nothing
        if(self.member == bot.user):
            return
        #If the message is not in the 
        if not self.message.id in bot.blindtestPromptsDict:
            return

    bot.run(credentials["token"])