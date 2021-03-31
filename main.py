import discord
import os
import feedparser

from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv(".env")
bot = commands.Bot(command_prefix='$$')

@bot.event
async def on_ready():
  print('Eresh est prête Master ! Connectée en tant que {0.user}'.format(bot))

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  msg = message.content
  
  if msg.startswith("$actu"):
    return

@tasks.loop(seconds=10.0)
async def  get_news_anime_news():
  animenews_feed = feedparser.parse("https://www.animenewsnetwork.com/news/rss.xml?ann-edition=fr")
  for news in animenews_feed.entries:
    #print(news["tags"][0].term)
    print(news.link)

  return

get_news_anime_news.start()

bot.run(os.getenv("TOKEN"))