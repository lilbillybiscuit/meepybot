import discord
import os
import sqlite3 as sl
import random
import string
import respond
import actions
import time
from discord.ext import commands
con = sl.connect('meepybot.db')
intents = discord.Intents.default()
intents.members=True
client = commands.Bot(command_prefix='?', intents=intents)
respond.client=client
actions.client=client

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


def randomstring(N=40):
    ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                         string.digits) for _ in range(N))


async def sendmessage(message, msg):
    await message.channel.send(msg)


async def configure(str1, msg=None):
    print(str1)
    # Change meepybot settings here
    key = str1.split()[0]
    val = str1.split()[1]
    print(key, val)
    try:
        val = int(val)
    except:
        hi = 4
    if key == "threshold":
        res = 0
        with con:
            print("communicated to database")
            #sql = "INSERT INTO USER (id, value) values (?,?)"
            sql = "UPDATE USER SET value = ? WHERE id = ?"
            data = (str(int(val)), 'vote_threshold')
            con.execute(sql, data)
            con.commit()
            if not msg == None:
                await msg.channel.send(f"Vote threshold set to {val}")
            
    elif key == "timeout":
      if (int(val)) > 300:
        if not msg == None:
          await msg.channel.send(f"Timeout too long (max is 300 seconds)")
          return
      with con:
          sql = "UPDATE USER SET value = ? WHERE id = ?"
          data = (str(int(val)), 'vote_timeout')
          con.execute(sql, data)
          con.commit()
          if msg is not None:
              await msg.channel.send(f"Vote timeout set to {val} seconds")


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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    tokenized = message.content.split()
    if len(tokenized) == 0:
        return
    
    if tokenized[0] == '?mmod' or tokenized[0] == '?mbot':
        command = str(message.content)[6:]
        if len(command.split())==0:
          await message.channel.send(open('assets/help.txt', 'r').read())
          return
        
        firstword = command.split()[0]
        if firstword=='help':
          await message.channel.send(open('assets/help.txt', 'r').read())
          return
        
        if firstword == 'log':
          print(str(message))
          await message.channel.send(f"Debug info logged ({randomstring(N=20)})", delete_after=2)
          return
        if firstword == 'random' or firstword == 'motd': await respond.getrandompin(message); return
        
        #check for empty first character
        if command[0] == ' ':
            print("Incorrect command string: \"" + command + "\"")
            await message.channel.send(
                ":question: **Incorrect command string**", delete_after=3)
            return
        if firstword == 'set':
            try:
                await configure(command[4:], msg=message)
                return
            except:
                await message.channel.send(
                    ":question: **Something went wrong**", delete_after=3)
                return
        

        if firstword == 'listroles':
            print(message.guild.roles)
            await message.channel.send(str(message.guild.roles), delete_after=15)
            return

        
        # Initiate unmute
        if firstword == 'unmute':
            user = command.split()[-1]
            if (user[2]=="&"):
              # This message was suggested by a friend
              await message.channel.send("Are you dumb? Why are you trying to mute a role!?")
              return
            print("USER =", user)
            seconds = await getdata("vote_timeout", msg=message)
            if seconds == None:
                await message.channel.send("Database exception occured")
                return
            else:
                seconds = int(seconds)
            numvotes = await getdata('vote_threshold', msg=message)
            if numvotes == None:
                await message.channel.send("Database exception occured")
                return
            else:
                numvotes = int(numvotes)
            
            userid = user[3:-1]
            with con:
              sql = "INSERT INTO reqs (id, action, datetime) values (?,?,?)"
              data = (message.id, f'u {userid} {seconds}', time.time())
              con.execute(sql, data)
              con.commit()
            
            sent = await message.channel.send(
                f"**Unmute {user}?**\nReact to the two options to vote ({numvotes} votes to unmute or cancel)\n*Will go away after {seconds} seconds*",
                delete_after=seconds)
            await sent.add_reaction("✅")
            await sent.add_reaction("❌")
            print(user)

        #Initiate mute
        elif firstword == 'mute':
            user = command.split()[-1]
            print("USER =", user)
            seconds = await getdata("vote_timeout", msg=message)
            if seconds == None:
                await message.channel.send("Database exception occured")
                return
            else:
                seconds == int(seconds)
            numvotes = await getdata('vote_threshold', msg=message)
            if numvotes == None:
                await message.channel.send("Database exception occured")
                return
            else:
                numvotes = int(numvotes)

            sent = await message.channel.send(
                f"**Mute {user}?**\nReact to the two options to vote ({numvotes} votes to mute or cancel)\n*Will go away after {seconds} seconds*",
                delete_after=seconds)
            await sent.add_reaction("✅")
            await sent.add_reaction("❌")
            print(user)

        #No other command matches
        else:
            await message.channel.send(
                ":grey_question: **Command doesn't exist**", delete_after=3)

        print("reached end")

@client.event
async def on_raw_reaction_add(reaction):
    if reaction.member == client.user:
        return
    
    print(str(reaction))
    print(str(reaction.emoji))
    print(str(reaction.message_id))


client.run(os.getenv('TOKEN'))
