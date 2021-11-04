import discord
import random
client = ""

async def getrandompin(ctx, num=None):
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

