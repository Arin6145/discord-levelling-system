import json
from discord.ext import commands
from datetime import time
import time

bot = commands.Bot(command_prefix="?")

#COGS
from rank_card import ranking
bot.add_cog(ranking(bot))

#ON READY
@bot.event
async def on_ready():
    print('---> Logged in as {0.user}'.format(bot))

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
            if level_have < new_level:
                await member.channel.send(f"<@{id}> has levelled up to Level - {new_level}")
    
        with open("data.json", "w") as f: 
            json.dump(user, f, indent=4)

        await bot.process_commands(member)

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

bot.run("TOKEN")