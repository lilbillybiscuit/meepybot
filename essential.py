import sqlite3 as sl
import discord
from discord.ext import commands
import pickle

intents = discord.Intents.default()
intents.members=True
client = commands.Bot(command_prefix='?meep ', intents=intents)

cache=dict()

con = sl.connect('meepybot.db')

async def refresh_pin_cache(message):
  pins = list(await message.channel.pins())
  cache[f"cache/pincache_{message.channel.id}"]=pins

async def keyexists(key, db="USER", key_name="id"):
    sql=f"SELECT * FROM {db} where {key_name}=:key"
    data = {"key": key}
    res = con.execute(sql, data)
    works=False
    for row in res:
        works=True
        if works: break
    return works
async def removerow(key, db="USER", key_name="id"):
    sql=f"DELETE FROM {db} WHERE {key_name}=:key"
    data= {"key":key}
    con.execute(sql, data)
    con.commit()

def setdata(key, val, db="USER"):
  sql = f"SELECT * FROM {db} WHERE id=:key"
  data={"key": str(key)}
  cur = con.execute(sql, data)
  works=False
  for row in cur:
    works=True
  if not works:
    con.execute(f"INSERT INTO {db} (id, value) values (?,?)", [str(key),"0"])
  sql = f"UPDATE {db} SET value = ? WHERE id = ?"
  data = (str(val), str(key))
  con.execute(sql, data)
  con.commit()

async def getdata(key, db="USER", msg=None):
    sql = f"SELECT * FROM {db} WHERE id=:key"
    data = {"key": str(key)}
    cur = con.execute(sql, data)
    res = None
    for row in cur:
        res = row
        break
    if res == None: return None
    return res[1]