import asyncio
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv(".env")

class Playlist:
  def __init__(self, bot, playlist={}):
    self.bot = bot
    self.playlist = playlist

  async def getBlindtestPlaylist(self, ctx):
    conn = await aiomysql.connect(
      host="localhost",
      port=3306,
      user=os.getenv("USER"),
      password=os.getenv("PASS"),
      db="er_bt_songs"
    )

    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM er_bt_songs")
        r = await cur.fetchall()
        print(r)
    conn.close()

    await ctx.send("Test")