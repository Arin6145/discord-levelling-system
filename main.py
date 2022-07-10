import json
from discord.ext import commands
from datetime import time
import time
import discord

bot = commands.Bot(command_prefix="?", intents = discord.Intents.all())

#COGS
from rank_card import ranking

#ON READY
@bot.event
async def on_ready():
    print('---> Logged in as {0.user}'.format(bot))
    await bot.add_cog(ranking(bot))
    print("---> Ranking card loaded")

#CHAT POINTS
@bot.event
async def on_message(member):
    with open("data.json", "r") as f:   
        user = json.load(f)
    id = member.author.id
    if member.content.startswith("?") or member.author.bot is True or member.guild is None:
        await bot.process_commands(member)
    elif str(id) not in user:
        user[str(id)] = {}
        user[str(id)]['xp'] = 0
        user[str(id)]['level'] = 1
        with open("data.json", "w") as f: 
            json.dump(user, f, indent=4)
        await bot.process_commands(member)
    else:
        if str(id) in user:
            user[str(id)]["xp"] += 2
            level_have = user[str(id)]["level"]
            user[str(id)]["level"] = int(user[str(id)]["xp"] ** (1/3))
            new_level = user[str(id)]["level"]
            if new_level > level_have:
                #channel = bot.get_channel("ID HERE") #ENTER ID OF UPDATE CHANNEL HERE (WITHOUT INVERTED COMMA)
                await member.channel.send(f"GG! <@{id}> has levelled up to Level - {new_level}")
                await bot.process_commands(member)
        with open("data.json", "w") as f: 
            json.dump(user, f, indent=4)

#POINTS ON VC
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None: 
        join_time = time.time()
        id = member.id
        with open("time_data.json","r") as f:
            user = json.load(f)
            user[str(id)] = int(join_time)
        with open("time_data.json","w") as f:
            json.dump(user, f, indent=4)              
    if before.channel is not None and after.channel is None:
        leave_time = time.time()
        id = member.id
        with open("time_data.json","r") as f:
            user = json.load(f)
            initial = user[str(id)]
            time_spent = int(leave_time) - int(initial)
            points = int((time_spent/60) * 10)
            with open("data.json","r") as f:
                file = json.load(f)
                file[str(id)]["xp"] += points
                file[str(id)]["level"] = int(file[str(id)]["xp"] ** (1/3))
            with open("data.json", "w") as f:
                json.dump(file, f, indent=4)

#PING
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`") 

bot.run("OTgyMDk5ODI1NDE3OTEyNDEx.Gfyuig.QvC8OJb69RPHCtPAU_nGeD-86sH918aVoB5JHE") #ENTER BOT TOKEN HERE (INSIDE INVERTED COMMA)