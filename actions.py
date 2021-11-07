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


async def isslowmoded(message):
    user_id=int(message.author.id)
    with con:

        if discord.utils.get(message.author.roles, name="slowmoded") is None:
            return None
        sql = "SELECT user_id,channel,datetime FROM slowmoded where user_id=:uid AND channel=:channel;"
        res=con.execute(sql, {"uid": user_id, "channel" : message.channel.id})
        works=False
        data=0
        for row in res:
            works=True
            data=row
            if works: break
        if works:
            return data[2]
        else:
            sql = "INSERT INTO slowmoded (user_id, channel, datetime) values (?,?,?)"
            data= (user_id, message.channel.id, int(time.time()))
            con.execute(sql, data)
            con.commit()
            return 0
#context is from the reaction, will be transferred to message
#user_id is the one that's being considered
#adds the mute role to the user_id
async def mute(ctx, user_id):
  member=ctx.message.author
  