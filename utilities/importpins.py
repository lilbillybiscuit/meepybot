from discord.ext import commands
import os

client = commands.Bot(command_prefix='?')
channel_id=905292900756250676


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

client.run(os.getenv('TOKEN'))

channel=client.get_channel(channel_id)

async def pullpins(ctx):
    channel=ctx.channel
    pins = list(await channel.pins())
    if len(pins) == 0:
        print("No pins exist")
        return
    for message in pins:
        message_id=message.id
        channel_id=message.channel.id
        if not await essential.keyexists(key=id, db="pins", key_name="message_id"):
            essential.con.execute(f"INSERT INTO pins (channel, message_id) values (?,?)", (message.channel.id,id))
            essential.con.commit()