import discord
import random
import essential
import pickle
import os
import time
import hashlib
import asyncio
import json
import datetime
client = essential.client
con=essential.con

async def cachemessage(msg, saveguild=True):
    sql='SELECT EXISTS(SELECT 1 FROM messages WHERE message_id=? LIMIT 1);'
    with con:
        exists=con.execute(sql, (msg.id,)).fetchall()[0][0]
    #print(msg.id, exists)
    if exists==0:
        sql="INSERT INTO messages (message_id, message, updated) values (?,?,?)"
        data=(msg.id, json.dumps(await essential.messagetodict(msg)),datetime.datetime.now().timestamp())
    else:
        sql="UPDATE messages SET message=?, updated=? WHERE message_id=?"
        data=(json.dumps(await essential.messagetodict(msg)), datetime.datetime.now().timestamp(), msg.id)
    with con:
        con.execute(sql, data)
        con.commit()
    
    if not saveguild: return
    sql='SELECT EXISTS(SELECT 1 FROM pins WHERE channel=? AND message_id=? LIMIT 1);'
    with con:
        exists=con.execute(sql, (msg.channel.id, msg.id)).fetchall()[0][0]
    #print(msg.id, exists)
    if exists==0:
        print("Can't insert guild, message doesn't exist")
        return
    else:
        sql="UPDATE pins SET guild=? WHERE message_id=?"
        data=(msg.guild.id, msg.id)
    with con:
        con.execute(sql, data)
        con.commit()

async def getrandompin2(ctx, arg=None):
    sql = "SELECT channel, message_id FROM pins WHERE channel=:chan ORDER BY RANDOM() LIMIT 1"
    data = {"chan" : int(ctx.channel.id)}
    if arg is not None:
        sql = "SELECT channel, message_id FROM pins WHERE channel=:chan ORDER BY datetime ASC LIMIT :arg,1"
        data = {"chan" : int(ctx.channel.id), "arg": int(arg)}
    res = essential.con.execute(sql, data)
    for row in res:
        res=row
        break
    messages=[await ctx.channel.fetch_message(res[1])]
    message=messages[0]
    embed=0
    nickname="[Doesn't exist]"
    try:
        nickname=ctx.channel.guild.get_member(message.author.id).nick
    except Exception as e:
        print(e)
        nothing=4
    
    #Message embed code starts here
    otherattachment=False
    if message.attachments:
        if "image" in message.attachments[0].content_type:
            embed = discord.Embed(description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(description=message.content)
            otherattachment = True
    else:
        embed = discord.Embed(description=message.content)
    
    embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
    embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")
    if otherattachment:
        await ctx.channel.send(embed=embed, files=[await f.to_file() for f in message.attachments])
    else:
        await ctx.channel.send(embed=embed) 
    return

async def getrandompin(ctx, num=None):
    '''pins=0
    cachepath=f"cache/pincache_{ctx.channel.id}"
    if os.path.exists(cachepath):
        with open(cachepath, 'rb') as f:
        pins=pickle.load(f)
    else:
        await essential.refresh_pin_cache(ctx)'''
    pins = list(await ctx.channel.pins())
    if len(pins) == 0:
        await ctx.channel.send("No pins exist")
        return
    message=0
    if num is not None and int(num)<len(pins):
        message=pins[len(pins)-int(num)-1]
    else:
        message=random.choice(pins)
    embed=0
    nickname="[Doesn't exist]"
    try:
        nickname=ctx.channel.guild.get_member(message.author.id).nick
    except:
        nothing=4
    
    #Message embed code starts here
    otherattachment=False
    if message.attachments:
        if "image" in message.attachments[0].content_type:
            embed = discord.Embed(description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(description=message.content)
            otherattachment = True
    else:
        embed = discord.Embed(description=message.content)

    embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
    embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")

    if otherattachment:
        await ctx.channel.send(embed=embed, files=[await f.to_file() for f in message.attachments])
    else:
        await ctx.channel.send(embed=embed) 
    return

async def addsinglepin(ctx, command):
    id = int(command)
    message=await ctx.channel.fetch_message(id)

    if await essential.keyexists(key=id, db="pins", key_name="message_id"):
        await ctx.channel.send("Pin already exists", delete_after=3)
    else:
        essential.con.execute(f"INSERT INTO pins (channel, message_id, datetime, guild) values (?,?,?,?)", (message.channel.id,id,int(time.time()),message.guild.id))
        essential.con.commit()
        embed=0
        nickname="[Doesn't exist]"
        try:
            nickname=ctx.channel.guild.get_member(message.author.id).nick
        except:
            nothing=4
        #Message embed code starts here
        otherattachment=False
        if message.attachments:
            if "image" in message.attachments[0].content_type:
                embed = discord.Embed(description=message.content)
                embed.set_image(url=message.attachments[0].url)
            else:
                embed = discord.Embed(description=message.content)
                otherattachment = True
        else:
            embed = discord.Embed(description=message.content)
        
        embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
        embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")
        if otherattachment:
            await ctx.channel.send("**Pinned:**",embed=embed, files=[await f.to_file() for f in message.attachments])
        else:
            await ctx.channel.send("**Pinned:**",embed=embed)

async def unpin(ctx, command):
    id = int(command)
    message=await ctx.channel.fetch_message(id)
    await essential.removerow(key=id, db="pins", key_name="message_id")
    embed=0
    nickname="[Doesn't exist]"
    try:
        nickname=ctx.channel.guild.get_member(message.author.id).nick
    except:
        nothing=4
    #Message embed code starts here
    otherattachment=False
    if message.attachments:
        if "image" in message.attachments[0].content_type:
            embed = discord.Embed(description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(description=message.content)
            otherattachment = True
    else:
        embed = discord.Embed(description=message.content)
    
    embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
    embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")

    if otherattachment:
        await ctx.channel.send("**Unpinned:**",embed=embed, files=[await f.to_file() for f in message.attachments])
    else:
        await ctx.channel.send("**Unpinned:**",embed=embed) 

async def addpin(ctx, args: list):
    id = int(args[0])
    messages=await ctx.channel.fetch_message(id)
    
    messages=[]
    for i in range(0, len(args)):
        id = args[i]
        try:
            temp = await ctx.channel.fetch_message(int(id))
        except:
            args[i]=None
            continue
        messages.append(temp)
    
    if not len(messages)==0:
        tempvar=hashlib.md5()
        tempstr=""
        for tempmsg in messages:
            hi=9
        id = 5 #HASH FUNCTION GOES HERE
    
    # Warn if there's more than one attachment
    tempvar=0
    for msg in messages:
        if msg.attachments: tempvar+=1
    if tempvar>1:
        await ctx.channel.send("Warning: Pin group contains more than one attachment, messages might not be displayed correctly", delete_after=5)
    
    
    if len(messages)==0 and await essential.keyexists(key=id, db="pins", key_name="message_id"):
        await ctx.channel.send("Pin already exists", delete_after=3)
    elif not len(messages)==0 and await essential.keyexists(key=id, db="pins", key_name="message_id"):
        await ctx.channel.send("Pin group already exists", delete_after=3)
    else:
        addstr=""
        for tempid in args:
            if tempid == None: continue
            addstr+=str(tempid)+" "
        # Remember that for multi-message pins, id is the hash value
        data=(messages[0].channel.id,id,int(time.time()), addstr, messages[0].guild.id)
        essential.con.execute(f"INSERT INTO pins (channel, message_id, datetime, additional_pins, guild) values (?,?,?,?,?)", data)
        essential.con.commit()
        embed=0
        nickname="[Doesn't exist]"
        try:
            nickname=ctx.channel.guild.get_member(messages[0].author.id).nick
        except:
            nothing=4
        
        message = messages[0]
        #Need to change this to accomidate for messages array
        #Message embed code starts here
        otherattachment=False
        if message.attachments:
            if "image" in message.attachments[0].content_type:
                embed = discord.Embed(description=message.content)
                embed.set_image(url=message.attachments[0].url)
            else:
                embed = discord.Embed(description=message.content)
                otherattachment = True
        else:
            embed = discord.Embed(description=message.content)
        
        embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
        embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")
        if otherattachment:
            await ctx.channel.send("**Pinned:**",embed=embed, files=[await f.to_file() for f in message.attachments])
        else:
            await ctx.channel.send("**Pinned:**",embed=embed)
        
        await cachemessage(message, saveguild=False)

async def unpin(ctx, command):
    id = int(command)
    message=await ctx.channel.fetch_message(id)
    await essential.removerow(key=id, db="pins", key_name="message_id")
    embed=0
    nickname="[Doesn't exist]"
    try:
        nickname=ctx.channel.guild.get_member(message.author.id).nick
    except:
        nothing=4
    #Message embed code starts here
    otherattachment=False
    if message.attachments:
        if "image" in message.attachments[0].content_type:
            embed = discord.Embed(description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(description=message.content)
            otherattachment = True
    else:
        embed = discord.Embed(description=message.content)
    
    embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
    embed.add_field(name='\u200B', value=f"\n[Message ID: {message.id}]({message.jump_url})")

    if otherattachment:
        await ctx.channel.send("**Unpinned:**",embed=embed, files=[await f.to_file() for f in message.attachments])
    else:
        await ctx.channel.send("**Unpinned:**",embed=embed) 

async def pullpins(ctx):
    channel=ctx.channel
    pins = list(await channel.pins())
    if len(pins) == 0:
        print("No pins exist")
        return
    for message in pins:
        message_id=message.id
        channel_id=message.channel.id
        if not await essential.keyexists(key=int(message_id), db="pins", key_name="message_id"):
            essential.con.execute(f"INSERT INTO pins (channel, message_id) values (?,?)", (int(channel_id), int(message_id)))
            essential.con.commit()
    await channel.send(f"Successfully grabbed pins from {channel.name}")
    
async def update_channel_pins(ctx):
    channel_id=ctx.channel.id
    send = await ctx.channel.send("Updating pin cache for this channel...")
    sql = "SELECT message_id FROM pins WHERE channel=?"
    with con:
        res = con.execute(sql, (channel_id,)).fetchall()
    counter=0
    for elem in res:
        if counter%4==0:
            await send.edit(content=f"Updating pin cache for this channel ({round(counter/len(res)*100,1)}% done)...")
        counter+=1
        try:
            msg = await ctx.channel.fetch_message(elem[0])
        except:
            continue
        await cachemessage(msg)
        await asyncio.sleep(0.5)
    await send.edit(content="Successfully refreshed!")

