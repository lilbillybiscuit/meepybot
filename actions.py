import discord
import random
import essential
client = essential.client


#context is from the reaction, will be transferred to message
#user_id is the one that's being considered
#adds the mute role to the user_id
async def mute(ctx, user_id):
  member=ctx.message.author
  