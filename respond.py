import discord
import random
import essential
import pickle
import os

client = essential.client

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
  print(message)
  embed=0
  nickname="[Doesn't exist]"
  try:
      nickname=ctx.channel.guild.get_member(message.author.id).nick
  except:
      nothing=4
  if message.attachments:
    embed = discord.Embed(title=f"{nickname} said:", description=message.content)
    embed.set_image(url=message.attachments[0].url)
  else:
    embed = discord.Embed(title=f"{nickname} said:", description=message.content)

  await ctx.channel.send(embed=embed)
  return

async def addpin(ctx, command):
    id = int(command.split()[1])
    message=await ctx.channel.fetch_message(id)
    if await essential.keyexists(key=id, db="pins", key_name="message_id"):
        await essential.removerow(key=id, db="pins", key_name="message_id")
        embed=0
        nickname="[Doesn't exist]"
        try:
            nickname=ctx.channel.guild.get_member(message.author.id).nick
        except:
            nothing=4
        if message.attachments:
            embed = discord.Embed(title=f"{nickname}:", description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(title=f"{nickname}:", description=message.content)
        await ctx.channel.send(embed=embed)
        await ctx.channel.send("was deleted")
    else:
        essential.con.execute(f"INSERT INTO pins (channel, message_id) values (?,?)", (message.channel.id,id))
        essential.con.commit()
        embed=0
        nickname="[Doesn't exist]"
        try:
            nickname=ctx.channel.guild.get_member(message.author.id).nick
        except:
            nothing=4
        if message.attachments:
            embed = discord.Embed(title=f"{nickname}:", description=message.content)
            embed.set_image(url=message.attachments[0].url)
        else:
            embed = discord.Embed(title=f"{nickname}:", description=message.content)
        await ctx.channel.send(embed=embed)
        await ctx.channel.send("was saved")