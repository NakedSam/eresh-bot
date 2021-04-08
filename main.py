import discord
import os
import sys
import json
import asyncio
import aiomysql
import functions

from classes import playlist, prompt
from functions import database

from dotenv import load_dotenv
from discord.ext import commands, tasks

description="```Un bot multifonction```"
intents = discord.Intents.default()
intents.members = True

load_dotenv(".env")
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
  bot.promptsList = []


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
  print(bot.databaseStructure["serversTable"])
  blindtestRequest = "SELECT * FROM" + bot.databaseStructure["serversTable"] + "WHERE server_id = " + str(ctx.guild.id) + ""
  #database.executeRequest(loop=blindtestLoop, request=blindtestRequest, database=bot.databaseStructure["serversDatabase"])
  #Starts a new connection to the database
  blindtestLoop = asyncio.get_event_loop()
  serverRow = blindtestLoop.run_until_complete(await database.executeRequest(
    loop=blindtestLoop, 
    request=blindtestRequest, 
    database=bot.databaseStructure["serversDatabase"],
    channel=ctx.channel))
  #We check if there's already the server in the list

  #If it's the case, we check if there's already a blind test channel, if not, we ask someone to choose it

  #If we have an ongoing blindtest, we mention that a blind test is already ongoing
  if(
    ctx.guild.id in bot.blindtests and 
    "ongoingBlindtest" in bot.blindtests[ctx.guild.id] and 
    bot.blindtests[ctx.guild.id]["ongoingBlindtest"] == True
  ):
    await ctx.channel.send("Un blind test est déjà en cours !")
  #Else we start the prompts chain and we set the blindtest as ongoing as well as putting the prompt
  else:
    bt_prompt = prompt.Prompt(
      bot=bot, 
      guildId=ctx.guild.id, 
      descriptions=[bot.prompts["blindtestModePrompt"]], 
      functions=[None],
      emojisLists=[["1️⃣", "2️⃣", "3️⃣", "🚫"]], 
      promptType="blindtest",
      channel=ctx.channel
    )

    bot.blindtests[ctx.guild.id] = {"ongoingBlindtest" : True}
    bot.ongoingBlindtestPrompts[ctx.guild.id] = {"prompt" : bt_prompt}
    bot.promptsList.append(bt_prompt)

    await bt_prompt.showPrompt()

#When a reaction is added, we perform some checks
@bot.event
async def on_raw_reaction_add(self, payload=discord.RawReactionActionEvent):
  #If it's the bot reaction, we do nothing
  if(self.member == bot.user):
    return
  #If the message is the same as the blindTestPrompt, we check if it's a valid reaction
  if(self.message_id == bot.ongoingBlindtestPrompts[self.guild_id]["prompt"].message.id and self.guild_id in bot.ongoingBlindtestPrompts.keys() ):
    if await bot.ongoingBlindtestPrompts[self.guild_id]["prompt"].checkReactionValidity(self.emoji.name):
      await bot.get_channel(self.channel_id).send("Valide !")
      await bot.ongoingBlindtestPrompts[self.guild_id]["prompt"].useFunction()

#@bot.event
#async def on_message(message):
#  if (message.author != bot.user) and (not message.content.startswith(bot.command_prefix)):
#    print("FOO")
 # else:
  #  await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))