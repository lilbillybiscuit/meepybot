import sqlite3 as sl
import discord
from discord.ext import commands
import pickle
import re
import string
import random
intents = discord.Intents.default()
intents.members=True
client = commands.Bot(command_prefix=('?meep ', '?mbot ', '?mmod '), intents=intents)

cache=dict()

def randomstring(N=50):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

async def message_date_comparator(message1, message2):
    if message1.created_at<message2.created_at: return -1
    elif message1.created_at>message2.created_at: return 1
    else: return 0
async def delete_message(guild, channel, message):
    guild=client.get_guild(guild)
    if guild is None: return False
    channel = discord.utils.get(guild.channels, name=int(channel), type="ChannelType.text")
    if channel is None: return False
    message=channel.fetch_message(message)
    if message is None: return False
    await message.delete()
    return True

async def get_channel(guild, channel):
    guild=client.get_guild(guild)
    if guild is None: return False
    channel = guild.get_channel(int(channel))
    return channel

async def get_member(guild, member_id):
    try:
        return client.get_guild(guild).get_member(member_id)
    except: return False

async def get_role(guild, role_id):
    try:
        guild = client.get_guild(guild)
        role = discord.utils.get(guild.roles, name=role_id)
        return role
    except: return False

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

async def getdata(key, db="USER", msg=None, retrow=False):
    sql = f"SELECT * FROM {db} WHERE id=:key"
    data = {"key": str(key)}
    cur = con.execute(sql, data)
    res = None
    for row in cur:
        res = row
        break
    if res == None: return None
    elif retrow: return res
    return res[1]

async def extractnumbers(str1):
    return [int(s) for s in re.findall(r'\b\d+\b', str(str1))]
