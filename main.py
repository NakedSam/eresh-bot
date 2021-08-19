import discord
import os
import json
import asyncio
import aiomysql
import functions

from classes import prompt
from functions import database, blindtest

from discord.ext import commands, tasks

CREDENTIALS_PATH = "./credentials.json"
EMOJIS_PATH = "./emojis.json"

credentials = None

with open(CREDENTIALS_PATH) as f:
    credentials = json.load(f)

dbCredentials = {
    "user": credentials["dbUser"],
    "password": credentials["dbPass"]
}

with open(EMOJIS_PATH) as f:
    emojisDict = json.load(f)

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
        bot.blindtests = {}
        bot.ongoingBlindtestPrompts = {}
        bot.blindtestPromptsDict = {}
        bot.blindtestPromptMessagesDict = {}
        bot.blindtestChannelChoicePromptsDict = {}
        bot.blindtestChannelChoicePromptMessagesDict = {}
        bot.emojisDict = emojisDict

        print("Eresh est prête Master !")

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
        #Initialize the blindtest as not ongoing if it doesn't exist already
        if not ctx.guild.id in bot.blindtests.keys():
            bot.blindtests[ctx.guild.id] = {"ongoingBlindtest": False}

        #Starts a new connection to the database
        blindtestLoop = asyncio.get_event_loop()

        blindtestRequest = f"SELECT server_btChannel FROM {bot.databaseStructure['serversTable']} WHERE server_id='{ctx.guild.id}'"
        #We check if there's already the server in the list by making a request to the database
        try:
            selectResponse = await database.executeRequest(
                loop=blindtestLoop, 
                request=blindtestRequest, 
                database=bot.databaseStructure["serversDatabase"],
                credentials=dbCredentials
            )
        except Exception as e:
            print(e)
            return


        #If there's no server returned or the server doesn't have an channel id for the blindtest, 
        #it means they haven't picked a blind test channel yet so we ask them to
        try:
            print(bot.blindtests[ctx.guild.id]["ongoingBlindtest"])
        except KeyError as e:
            print(e)
            pass
        print(f" selectResponse == None : {selectResponse == None}")
        print(f"selectResponse[0][0] == ctx.guild.id : {selectResponse[0][0] == ctx.guild.id}")
        if ctx.guild.id in bot.blindtests.keys():
            print(f"bot.blindtests[ctx.guild.id]['ongoingBlindtest'] : {bot.blindtests[ctx.guild.id]['ongoingBlindtest']}")
        if selectResponse == None or not selectResponse[0][0] == ctx.guild.id and not bot.blindtests[ctx.guild.id]["ongoingBlindtest"]:
            #We activate the blindtest
            bot.blindtests[ctx.guild.id] = {"ongoingBlindtest" : True}  

            channelChoicePrompt = prompt.Prompt(
                bot=bot,
                guildId=ctx.guild.id,
                descriptions=[bot.prompts["blindtestChoicePrompt"]],
                emojisLists=[[bot.emojisDict["whiteCheckMark"], bot.emojisDict["crossMark"]]],
                promptType="blindtestChannelChoice",
                channel=ctx.channel,
                functions=(None, blindtest.blindtestChannelChoiceFunc)
            )
            
            blindtestChannelChoiceMessage = await channelChoicePrompt.showPrompt()
            blindtestChannelChoicePromptToAdd = {
                "prompt": channelChoicePrompt
            }
            #We store the prompt and the message id in bot stored variables
            bot.blindtestChannelChoicePromptMessagesDict[ctx.guild.id] = blindtestChannelChoicePromptToAdd
            bot.blindtestChannelChoicePromptsDict[blindtestChannelChoiceMessage.id] = blindtestChannelChoiceMessage.id    
        else:
            #If we have an ongoing blindtest, we mention that a blind test is already ongoing
            if ctx.guild.id in bot.blindtests and bot.blindtests["ongoingBlindtest"]:
                await ctx.channel.send("Un blind test est déjà en cours !")           
            #Else we start the prompts chain and we set the blindtest as ongoing as well as putting the prompt
            else:
                btPrompt = prompt.Prompt(
                    bot=bot, 
                    guildId=ctx.guild.id, 
                    descriptions=[bot.prompts["blindtestModePrompt"]],
                    emojisLists=[[bot.emojisDict["whiteCheckMark"], bot.emojisDict["crossMark"]]], 
                    promptType="blindtest",
                    channel=ctx.channel,
                    functions=(None)
                )
                #We activate the blindtest
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
    async def on_raw_reaction_add(payload):   
        #If it's the bot reaction, we do nothing
        if(payload.member.bot):
            return
        
        #If the message is in the blindtestPrompts, we launch the next section of the blindtest
        if payload.message_id in bot.blindtestPromptMessagesDict:
            #If the emoji is not in the prompt emoji list for this prompt stage, we do nothing
            if not bot.blindtestPromptsDict[payload.guild_id]["prompt"].checkReactionValidity(payload.emoji):
                return
            #Else we pass to the next step
            bot.blindtestPromptsDict[payload.guild_id]["prompt"].promptStage += 1
            bot.blindtestPromptsDict[payload.guild_id]["prompt"].runFunction(payload.emoji)
        #If the if of the prompt is in the dictionnary of prompts
        elif payload.message_id in bot.blindtestChannelChoicePromptsDict.values():
            #We check the validity of the emoji or if we're currently processing a prompt
            if not await bot.blindtestChannelChoicePromptMessagesDict[payload.guild_id]["prompt"].checkReactionValidity(payload.emoji) or \
                bot.blindtestChannelChoicePromptMessagesDict[payload.guild_id]["prompt"].isOngoing:
                return
            #Else we pass to the next step
            bot.blindtestChannelChoicePromptMessagesDict[payload.guild_id]["prompt"].promptStage += 1
            bot.blindtestChannelChoicePromptMessagesDict[payload.guild_id]["prompt"].isOngoing = True
            await bot.blindtestChannelChoicePromptMessagesDict[payload.guild_id]["prompt"].runFunction(payload.emoji)
            return

    bot.run(credentials["token"])