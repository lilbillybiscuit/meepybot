import discord
import random
client = ""

async def getrandompin(ctx):
  pins = list(await ctx.channel.pins())
  if len(pins) == 0:
    await ctx.channel.send("No pins exist")
    return
  message=random.choice(pins)
  print(message)
  embed=0
  if message.attachments:
    embed = discord.Embed(title=f"{ctx.channel.guild.get_member(message.author.id).nick} said:", description=message.content)
    embed.set_image(url=message.attachments[0].url)
  else:
    embed = discord.Embed(title=f"{ctx.channel.guild.get_member(message.author.id).nick} said:", description=message.content)

  await ctx.channel.send(embed=embed)
  return

