import discord
import random
import essential
import time
client = essential.client
con = essential.con

# Only use with python threads
def background():
    while True:
        with con:
            data = con.execute("SELECT id, action, min(datetime) FROM reqs")
            res=None
            for row in data:
                res=row
                break
            if res is None:
                continue
            tokenized=res[1].split()
            actions=tokenized[1].split()
            if (time.time()<int(tokenized[2])):
                continue
            if (action[0]=='m' or action[0]=='u'):
                hi=5
        time.sleep(1)

async def hasadmin(message):
    role = discord.utils.find(lambda r: r.name == 'Member', ctx.message.guild.roles)
    if role in user.roles:
        await bot.say("{} is not muted".format(user))
    else:
        await bot.add_roles(user, role)

async def isslowmoded(message):
    user_id=int(user_id)
    if essential.keyexists(user_id, db="slowmoded", key_name="user_id"):
        return True
    else:
        return False
#context is from the reaction, will be transferred to message
#user_id is the one that's being considered
#adds the mute role to the user_id
async def mute(ctx, user_id):
  member=ctx.message.author
  