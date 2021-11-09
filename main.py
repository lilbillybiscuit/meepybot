import discord
import os
import sqlite3 as sl
import random
import string
import respond
import actions
import time
import asyncio
import essential
import threading
#from persist_pq import Persist_PQ
from discord.ext import commands, tasks
con = essential.con
client = essential.client

#pq = Persist_PQ("meepy.pq")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    actions.start_background()

def randomstring(N=40):
    ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                         string.digits) for _ in range(N))


async def sendmessage(message, msg):
    await message.channel.send(msg)


async def configure(str1, msg=None):
    # Change meepybot settings here
    key = str1.split()[0]
    val = str1.split()[1]
    try:
        val = int(val)
    except:
        hi = 4
    if key == "threshold":
        res = 0
        with con:
            print("communicated to database")
            essential.setdata('vote_threshold', str(int(val)))
            if not msg == None:
                await msg.channel.send(f"Vote threshold set to {val}")
            
    elif key == "timeout":
      if (int(val)) > 300:
        if not msg == None:
          await msg.channel.send(f"Timeout too long (max is 300 seconds)")
          return
      with con:
          essential.setdata('vote_timeout', str(int(val)))
          if msg is not None:
              await msg.channel.send(f"Vote timeout set to {val} seconds")
    elif key == "slowmoderole":
        if essential.keyexists("slowmoderole"):
            if not msg == None:
                await msg.channel.send(f"")
            return
        with con:
            essential.setdata('vote_timeout', str(int(val)))
            if msg is not None:
                await msg.channel.send(f"Vote timeout set to {val} seconds")


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

@client.command(name="set", pass_context=True, brief="Set Options (Requires \"Manage Roles\"")
@commands.has_permissions(manage_roles=True)
async def setoption(ctx, *args):
    ctx = ctx.message
    try:
        # Change meepybot settings here
        key = args[0]
        val = args[1]

        if key == "threshold":
            if int(val)<=1:
                await ctx.channel.send(f"Threshold too low")
                return
            res = 0
            essential.setdata('vote_threshold', str(int(val)))
            await ctx.channel.send(f"Vote threshold set to {val}")
                
        elif key == "timeout":
            if (int(val)) > 300:
                await ctx.channel.send(f"Timeout too long (max is 300 seconds)")
                return
            essential.setdata('vote_timeout', str(int(val)))
            await ctx.channel.send(f"Vote timeout set to {val} seconds")

        elif key == "slowmoderole":
            role=discord.utils.get(ctx.guild.roles,name=val)
            if role is None:
                await ctx.channel.send(f"Role doesn't exist")
                return
            essential.setdata('slowmoderole', str(int(role.id)))
            await ctx.channel.send(f"Slowmode Role ID set to {val} (Role ID: {role.id})")

        elif key == "slowmodetime":
            essential.setdata('slowmodetime', str(int(val)))
            await ctx.channel.send(f"Slowmode timeout set to {val}")
        elif key == "mute_duration":
            essential.setdata("mute_duration", str(int(val)))
            await ctx.channel.send(f"Mute duration set to {val}")
        elif key == "bot_mute" or key=="bot_muting":
            if val.lower()=="true":
                val=1
            elif val.lower()=='false':
                val=0
            else:
                await ctx.channel.send("Must be 'true' or 'false'")
                return
            essential.setdata('bot_muting', str(val))
            if val==0:  await ctx.channel.send("Bot muting disabled")
            elif val==1:await ctx.channel.send("Bot muting enabled")
    except Exception as e:
        print(e)
        await ctx.channel.send(":question: **Something went wrong**", delete_after=3)
        return
@setoption.error
async def setoption_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingAnyRole):
        message = "You don't have the required role..."
    elif isinstance(error, commands.MissingPermission):
        message = "\"Manage Roles\" permission required"
    else:
        message = "Something went wrong..."

    await ctx.send(message, delete_after=3)
    await ctx.message.delete(delay=3)

@client.command(pass_context=True)
async def version(ctx):
    await ctx.channel.send("Version v0.2.6 (implemented force muting and updated commands)")

@client.command(pass_context=True, brief="Pin a message with its ID")
@commands.has_permissions(manage_channels=True)
async def pin(ctx, arg):
    message=ctx.message
    try:
        await respond.addpin(message, int(arg))
    except Exception as e:
        print(e)
        await message.channel.send("Something went wrong...")
    return
@pin.error
async def pin_error(ctx: commands.Context, error: commands.CommandError):
    print(error)
    if isinstance(error, commands.MissingAnyRole):
        message = "Pinning requires 'mod' or 'Admin'"
    elif isinstance(error, commands.MissingPermissions):
        message = "\"Manage Channels\" required"
    else:
        message = "Something went wrong..."

    await ctx.send(message, delete_after=3)
    await ctx.message.delete(delay=3)


@client.command(pass_context=True, brief="View bot settings")
async def options(ctx):
    mes=""
    mes += f"**Slowmode Inteval** (slowmodetime): {await essential.getdata('slowmodetime')}\n"
    mes += f"**Vote Timeout** (timeout): {await essential.getdata('vote_timeout')}\n"
    mes += f"**Vote Threshold** (threshold): {await essential.getdata('vote_threshold')}\n"
    mes += f"**Slowmode/Mute Duration** (mute_duration): {await essential.getdata('mute_duration')}"
    await ctx.channel.send(mes)

@client.command(name="random", pass_context=True, brief="Displays a random pinned message from this channel", aliases=["motd"])
async def random1(ctx, arg=None):
    message=ctx.message
    #print("Through client.command")
    if  arg is not None: await respond.getrandompin(message, num=int(arg)); return
    else: await respond.getrandompin(message); return

@client.command(name="random2", pass_context=True, brief="Displays a random pinned message from this channel(v2)")
async def random2(ctx, arg=None):
    message=ctx.message
    print("Through client.command")
    if  arg is not None: await respond.getrandompin2(message, num=int(arg)); return
    else: await respond.getrandompin2(message); return

@client.command(pass_context=True, aliases = ["funmute"])
@commands.has_permissions(manage_roles=True)
async def forceunmute(ctx, arg):
    message=ctx.message
    mentions=message.mentions
    role = discord.utils.get(ctx.guild.roles, name = "text-muted")
    retstr = "Unmuted "
    for member in mentions:
        await member.remove_roles(role)
        retstr += f"{member.name}#{member.discriminator}, "
    await ctx.channel.send(retstr[:-2])
    return

@client.command(pass_context=True, brief="Vote to unmute someone")
@commands.cooldown(1,10)
async def unmute(ctx, arg):
    message=ctx.message
    mentions = message.mentions
    user = arg
    userid = mentions[0].id
    if (user[2]=="&") or (user[0]=='@'):
        # This message was suggested by a friend
        await message.channel.send("Are you dumb? Why are you trying to unmute a role!?")
        return
    if await essential.keyexists(f"u {userid}", db="reqs", key_name="action"):
        await message.channel.send(f"Request to unmute {user} already exists")
        return
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

    sent = await message.channel.send(
        f"**Unmute {user}?**\nReact to the two options to vote ({numvotes} votes to unmute or cancel)\n*Will go away after {seconds} seconds*",
        delete_after=seconds)
    await sent.add_reaction("✅")
    await sent.add_reaction("❌")
    try:
        with con:
            sql = "INSERT INTO reqs (id, channel, action, datetime, guild) values (?,?,?,?,?)"
            data = (int(sent.id), int(message.channel.id), f'u {userid} {numvotes}', int(time.time()+seconds), int(message.guild.id))
            con.execute(sql, data)
            con.commit()
    except:
        await message.channel.send("Something went wrong")
        await sent.delete()

    print(user)

@client.command(pass_context=True,aliases = ["fmute"], brief="Mutes someone without voting (Mods only)")
@commands.has_permissions(manage_roles=True)
async def forcemute(ctx, arg):
    message=ctx.message
    mentions=message.mentions
    role = discord.utils.get(ctx.guild.roles, name = "text-muted")
    retstr = "Muted "
    for member in mentions:
        await member.add_roles(role)
        retstr += f"{member.name}#{member.discriminator}, "
    await ctx.channel.send(retstr[:-2])
    return

@client.command(name="slowmode", aliases=["sm"], pass_context=True, brief="Vote to slowmode someone")
@commands.cooldown(1,10)
async def slowmode(ctx, arg):
    message=ctx.message
    mentions = message.mentions
    user = arg
    userid = mentions[0].id
    if (user[2]=="&") or (user[0]=='@'):
        # This message was suggested by a friend
        await message.channel.send("Are you dumb? Why are you trying to slowmode a role!?")
        return
    if await essential.keyexists(f"sm {userid}", db="reqs", key_name="action"):
        await message.channel.send(f"Request to slowmode {user} already exists")
        return
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

    sent = await message.channel.send(
        f"**Slowmode {user}?**\nReact to the two options to vote ({numvotes} votes to slowmode or cancel)\n*Will go away after {seconds} seconds*",
        delete_after=seconds)
    await sent.add_reaction("✅")
    await sent.add_reaction("❌")
    try:
        with con:
            sql = "INSERT INTO reqs (id, channel, action, datetime, guild) values (?,?,?,?,?)"
            data = (int(sent.id), int(message.channel.id), f'sm {userid} {numvotes}', int(time.time()+seconds), int(message.guild.id))
            con.execute(sql, data)
            con.commit()
    except:
        await message.channel.send("Something went wrong")
        await sent.delete()

    print(user)


@client.command(pass_context=True, brief="Vote to mute someone")
@commands.cooldown(1, 10)
async def mute(ctx, arg):
    message=ctx.message
    mentions = message.mentions
    user = arg
    userid = mentions[0].id
    if (user[2]=="&") or (user[0]=='@'):
        # This message was suggested by a friend
        await message.channel.send("Are you dumb? Why are you trying to mute a role!?")
        return
    if await essential.keyexists(f"m {userid}", db="reqs", key_name="action"):
        await message.channel.send(f"Request to mute {user} already exists")
        return
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

    sent = await message.channel.send(
        f"**Mute {user}?**\nReact to the two options to vote ({numvotes} votes to mute or cancel)\n*Will go away after {seconds} seconds*",
        delete_after=seconds)
    await sent.add_reaction("✅")
    await sent.add_reaction("❌")
    try:
        with con:
            sql = "INSERT INTO reqs (id, channel, action, datetime, guild) values (?,?,?,?,?)"
            data = (int(sent.id), int(message.channel.id), f'm {userid} {numvotes}', int(time.time()+seconds), int(message.guild.id))
            con.execute(sql, data)
            con.commit()
    except:
        await message.channel.send("Something went wrong")
        await sent.delete()

    print(user)

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):

    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "Insufficent privileges to run this command"
    elif isinstance(error, commands.UserInputError):
        message = "Incorrect input"
    else:
        message = "Something went wrong..."

    await ctx.channel.send(message, delete_after=5)
    await ctx.message.delete(delay=5)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    temp, note=await actions.isslowmoded(message)
    if note == "mute":
        await message.delete()
    if temp is not None:
        timeout=await essential.getdata("slowmodetime")
        # Temp represents the time
        #print(time.time(), temp, int(timeout))
        if time.time()<temp+int(timeout):
            await message.delete()
            #await message.channel.send(f"Slowmoded ({round(temp+int(timeout)-time.time(),2)} seconds left)", delete_after=1)
            return
        else:
            with con:
                #print("HI")
                sql = "UPDATE slowmoded SET datetime=? WHERE user_id= ? and channel=?"
                con.execute(sql, (int(time.time()), int(message.author.id), int(message.channel.id)))
                con.commit()
    
    try:
        await client.process_commands(message)
    except Exception as e:
        print(e)
    
    # Process by message type
    if (str(message.type) == "MessageType.pins_add"):
      #essential.refresh_pin_cache(message)
      return
    tokenized = message.content.split()
    if len(tokenized) == 0:
        return
    
    if tokenized[0] == '?mmod' or tokenized[0] == '?mbot'\
    or tokenized[0] == '?meep':
        command = str(message.content)[6:]

        if len(command.split())==0:
          #await message.channel.send("?meep help", delete_after=0.1)
          await message.channel.send(open('assets/help.txt', 'r').read())
          return
        
        firstword = command.split()[0]
        if firstword == 'log':
          print(str(message))
          await message.channel.send(f"Debug info logged ({randomstring(N=20)})", delete_after=2)
          return
          
        if firstword == 'vote':
            msg1 = command[5:]
            sent = await message.channel.send(f"**Custom vote**\n{msg1}")
            await sent.add_reaction("✅")
            await sent.add_reaction("❌")
            return
        if firstword == 'getpins':
            try:
                await respond.pullpins(message)
            except Exception as e:
                await message.channel.send("Something went wrong...")
                print(e)
            return
        #check for empty first character
        if command[0] == ' ':
            print("Incorrect command string: \"" + command + "\"")
            await message.channel.send(
                ":question: **Incorrect command string**", delete_after=3)
            return
        

        if firstword == 'listroles':
            print(message.guild.roles)
            await message.channel.send(str(message.guild.roles), delete_after=15)
            return

        #No other command matches
        '''else:
            await message.channel.send(
                ":grey_question: **Command doesn't exist**", delete_after=3)
        '''
        #print("reached end")

@client.event
async def on_raw_reaction_add(reaction):
    if reaction.member == client.user:return
    emojiname = reaction.emoji.name
    if not (emojiname == '✅' or emojiname == '❌'): return
    #print(reaction)
    message_id = reaction.message_id
    with con:
        sql = "SELECT id, action FROM reqs WHERE id = ?"
        print(message_id)
        data = con.execute(sql, (int(message_id),))
        res=None
        for row in data:
            res=row
            break
        if res is None:
            return
    # At this point, there should be an active request
    action = res[1].split()
    votethreshold=None
    if action[0]=='m' or action[0]=='u' or action[0]=='usm' or action[0]=='sm':
        votethreshold = int(action[2])
    guild = client.get_guild(reaction.guild_id)
    #channel=discord.utils.get(guild.channels, name=int(reaction.channel_id))
    channel = guild.get_channel(reaction.channel_id)
    message = await channel.fetch_message(message_id)
    reactionobj = discord.utils.get(message.reactions, emoji = emojiname)
    if reactionobj and reactionobj.count >= votethreshold:
        if emojiname == '❌':
            await message.delete()
            await channel.send(f"Unmute <@!{action[1]}> was cancelled")
            return
        elif emojiname == '✅':
            if action[0]=='m':
                await actions.mute(message_id)
                return
            elif action[0]=='u':
                temp=await actions.unmute(int(reaction.guild_id), int(action[1]))
                if temp:
                    await channel.send(f"By popular vote, <@!{action[1]}> was unmuted")
                    with con:
                        con.execute("DELETE FROM reqs WHERE id = ? AND action = ?", (res[0], res[1]))
                        con.commit()
                else:
                    await channel.send("Something went wrong")
            elif action[0]=='sm':
                await actions.add_slowmode(message_id)
                return
            elif action[0]=='usm':
                temp=await actions.unslowmode(int(reaction.guild_id), int(action[1]))
                if temp:
                    await channel.send(f"By popular vote, <@!{action[1]}> was un-slowmoded")
                    with con:
                        con.execute("DELETE FROM reqs WHERE id = ? AND action = ?", (res[0], res[1]))
                        con.commit()
                else:
                    await channel.send("Something went wrong")
    #print(str(reaction))
    #print(str(reaction.emoji))
    #print(str(reaction.message_id))


client.run(os.getenv('TOKEN'))
