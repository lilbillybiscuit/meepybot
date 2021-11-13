import discord
import random
import essential
import time
import sqlite3 as sl
import asyncio
client = essential.client
con = essential.con
from discord.ext import tasks

@tasks.loop(seconds=1.0)
async def background():
    while True:
        with con:
            data = con.execute("SELECT id, action, min(datetime), channel, guild FROM reqs")
        res=None
        for row in data:
            res=row
            break
        if None in res:
            break
        id, actions, temptime, channel, guild = res
        actions=actions.split()
        if int(time.time())<int(temptime):
            break
        print(res)
        if (actions[0]=='m' or actions[0]=='u') or (actions[0]=='sm' or actions[0]=='usm'):
            await essential.delete_message(guild=guild, channel=channel, message=id)
            with con:
                data=(res[0], res[1], res[3], res[4])
                con.execute("DELETE FROM REQS WHERE id = ? AND action = ? and channel = ? AND guild = ?", data)
                con.commit()
        
        if (actions[0]=='fu'): #force unmute
            guild = client.get_guild(guild)
            role = discord.utils.get(guild.roles, name="text-muted")
            member = guild.get_member(int(actions[1]))
            #print(member, actions[1])
            #print(role)
            await member.remove_roles(role)
            #client.remove_roles(member, role)
            #print(channel)
            channel=client.get_channel(int(channel))
            #channel = discord.utils.get(guild.channels, name=int(channel))
            await channel.send(f"<@!{member.id}> was unmuted after time expired")
            with con:
                data=(res[0], res[1], res[3], res[4])
                con.execute("DELETE FROM REQS WHERE id = ? AND action = ? and channel = ? AND guild = ?", data)
                con.commit()
        elif actions[0]=='fusm':
            guild = client.get_guild(guild)
            role = discord.utils.get(guild.roles, name="slowmoded")
            member = guild.get_member(int(actions[1]))
            #print(member, actions[1])
            #print(role)
            await member.remove_roles(role)
            #client.remove_roles(member, role)
            #print(channel)
            channel=client.get_channel(int(channel))
            #channel = discord.utils.get(guild.channels, name=int(channel))
            await channel.send(f"<@!{member.id}> was un-slowmoded after time expired")
            with con:
                data=(res[0], res[1], res[3], res[4])
                con.execute("DELETE FROM REQS WHERE id = ? AND action = ? and channel = ? AND guild = ?", data)
                con.commit()
        #print(f"Deleted {res} from event queue")
def start_background():
    background.start()

async def isslowmoded(message):
    if message.author.guild_permissions.administrator:
        return (None, None)
    user_id=int(message.author.id)
    with con:
        if discord.utils.get(message.author.roles, name="text-muted"):
            if int(await essential.getdata("bot_muting")) == 1:
                return (None, "mute")
        if discord.utils.get(message.author.roles, name="slowmoded") is None:
            return (None, None)
        sql = "SELECT user_id,channel,datetime FROM slowmoded where user_id=:uid AND channel=:channel;"
        res=con.execute(sql, {"uid": user_id, "channel" : message.channel.id})
        works=False
        data=0
        for row in res:
            works=True
            data=row
            if works: break
        if works:
            return (data[2], "slow")
        else:
            sql = "INSERT INTO slowmoded (user_id, channel, datetime) values (?,?,?)"
            data= (user_id, message.channel.id, int(time.time()))
            con.execute(sql, data)
            con.commit()
            return (0, "slow")
#Consolidate with "mute" later
async def add_slowmode(bot_message_id):
    with con:
        sql = "SELECT id, channel, action, datetime, guild FROM reqs WHERE id = ? AND action like 'sm %'"
        data = con.execute(sql, (bot_message_id,))
        
    res=None
    for row in data:
        res=row
        break
    if res[0] is None:
        print("Error, poll not found")
        return False
    with con:
        con.execute("DELETE FROM reqs WHERE id = ? AND channel = ? AND action = ?", (res[0], res[1], res[2]))
        con.commit()
    message_id, channel, action, temptime, guild = res
    action = action.split()
    seconds = await essential.getdata("mute_duration")
    with con:
        sql = "INSERT INTO reqs (id, channel, action, datetime, guild) values (?,?,?,?,?)"
        data = (int(time.time()), int(channel), f'fusm {action[1]} {int(action[2])}', int(time.time()+int(seconds)), int(guild))
        con.execute(sql, data)
        con.commit()
    guild = client.get_guild(guild)
    channel = guild.get_channel(channel)
    member = guild.get_member(int(action[1]))
    role = discord.utils.get(guild.roles, name = 'slowmoded')
    await member.add_roles(role)
    await channel.send(f"By popular vote, <@!{action[1]}> was slowmoded for {seconds} seconds\nThey can send a message every **{await essential.getdata('slowmodetime')}** seconds")
    if (member.guild_permissions.administrator):
        await channel.send("(Won't do anything since they are an admin)", delete_after=5)

async def unslowmode(guild, member_id):
    try:
        guild = client.get_guild(guild)
        member = guild.get_member(member_id)
        role = discord.utils.get(guild.roles, name="slowmoded")
        await member.remove_roles(role)
        return True
    except:
        return False

#context is from the reaction, will be transferred to message
#user_id is the one that's being considered
#adds the mute role to the user_id
async def mute(bot_message_id):
    with con:
        sql = "SELECT id, channel, action, datetime, guild FROM reqs WHERE id = ? AND action like 'm %'"
        data = con.execute(sql, (bot_message_id,))
        
    res=None
    for row in data:
        res=row
        break
    if res[0] is None:
        print("Error, poll not found")
        return False
    with con:
        con.execute("DELETE FROM reqs WHERE id = ? AND channel = ? AND action = ?", (res[0], res[1], res[2]))
        con.commit()
    message_id, channel, action, temptime, guild = res
    action = action.split()
    seconds = await essential.getdata("mute_duration")
    with con:
        sql = "INSERT INTO reqs (id, channel, action, datetime, guild) values (?,?,?,?,?)"
        data = (int(time.time()), int(channel), f'fu {action[1]} {int(action[2])}', int(time.time()+int(seconds)), int(guild))
        con.execute(sql, data)
        con.commit()
    guild = client.get_guild(guild)
    channel = guild.get_channel(channel)
    member = guild.get_member(int(action[1]))
    role = discord.utils.get(guild.roles, name = 'text-muted')
    await member.add_roles(role)
    await channel.send(f"By popular vote, <@!{action[1]}> was muted for {seconds} seconds")
    if (member.guild_permissions.administrator):
        await channel.send("(Won't do anything since they are an admin)", delete_after=5)


async def unmute(guild, member_id):
    try:
        guild = client.get_guild(guild)
        member = guild.get_member(member_id)
        role = discord.utils.get(guild.roles, name="text-muted")
        await member.remove_roles(role)
        return True
    except:
        return False

async def strike(member_id, guild_id):
    sql = "SELECT * FROM strikes WHERE user_id=? AND guild_id=?"
    res=0
    with con:
        hi = con.execute(sql, (int(member_id), guild_id))
        res=None
        for row in hi:
            res=row
            break
        if res == None:
            return
    maxstrikes=await essential.getdata("strike_limit")
        