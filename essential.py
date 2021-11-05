import sqlite3 as sl
import discord
from discord.ext import commands
import pickle

intents = discord.Intents.default()
intents.members=True
client = commands.Bot(command_prefix='?', intents=intents)

con = sl.connect('meepybot.db')

async def refresh_pin_cache(message):
  pins = list(await message.channel.pins())
  with open(f"cache/pincache_{message.channel.id}", 'wb') as f:
    pickle.dump(pins, f)

def setdata(key, val):
  sql = "SELECT * FROM USER WHERE id=:key"
  data={"key": str(key)}
  cur = con.execute(sql, data)
  works=False
  for row in cur:
    works=True
  if not works:
    con.executemany("INSERT INTO USER (id, value) values (?,?)", (str(key),"0"))
  sql = "UPDATE USER SET value = ? WHERE id = ?"
  data = (str(val), str(key))
  con.execute(sql, data)
  con.commit()

async def getdata(key, msg=None):
    sql = "SELECT * FROM USER WHERE id=:key"
    data = {"key": str(key)}
    cur = con.execute(sql, data)
    res = None
    for row in cur:
        res = row
        break
    if res == None: return None
    return res[1]