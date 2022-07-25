import json
from discord.ext import commands, tasks
from datetime import time
import time, os
import discord
import operator
import datetime

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#COGS
from rank_card import ranking

#ON READY
@bot.event
async def on_ready():
    print('---> Logged in as {0.user}'.format(bot))
    await bot.add_cog(ranking(bot))
    print("---> Ranking card generator loaded")
    await clearDaily.start()
    await clearWeekly.start()

#CHAT POINTS
@bot.event
async def on_message(member):
    with open("data.json", "r") as f:   
        user = json.load(f)
    id = member.author.id
    if  member.content.startswith("?") or member.author.bot is True or member.guild is None:
        await bot.process_commands(member)
    elif str(id) not in user:
        user[str(id)] = {}
        user[str(id)]['xp'] = 0
        user[str(id)]['level'] = 1
        user[str(id)]['d-xp'] = 0
        user[str(id)]['daily'] = 1
        user[str(id)]['w-xp'] = 0
        user[str(id)]['weekly'] = 1
        user[str(id)]['m-xp'] = 0
        user[str(id)]['monthly'] = 1
        with open("data.json", "w") as f: 
            json.dump(user, f, indent=4)
        await bot.process_commands(member)
    else:
        if str(id) in user:
            user[str(id)]["xp"] += 2
            user[str(id)]["d-xp"] += 2
            user[str(id)]["w-xp"] += 2
            user[str(id)]["m-xp"] += 2
            level_have = user[str(id)]["level"]
            user[str(id)]["level"] = int(user[str(id)]["xp"] ** (1/3))
            user[str(id)]["daily"] = int(user[str(id)]["d-xp"] ** (1/3))
            user[str(id)]["weekly"] = int(user[str(id)]["w-xp"] ** (1/3))
            user[str(id)]["monthly"] = int(user[str(id)]["m-xp"] ** (1/3))
            new_level = user[str(id)]["level"]
            if new_level > level_have:
                #channel = bot.get_channel("1000186784757579908") #Channel ID here "to receive updates"
                await member.channel.send(f"> <@{id}>님이 {new_level}레벨로 오르셨습니다!")
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
                file[str(id)]["d-xp"] += points
                file[str(id)]["w-xp"] += points
                file[str(id)]["m-xp"] += points
                file[str(id)]["level"] = int(file[str(id)]["xp"] ** (1/3))
                file[str(id)]["daily"] = int(file[str(id)]["d-xp"] ** (1/3))
                file[str(id)]["weekly"] = int(file[str(id)]["w-xp"] ** (1/3))
                file[str(id)]["monthly"] = int(file[str(id)]["m-xp"] ** (1/3))
            with open("data.json", "w") as f:
                json.dump(file, f, indent=4)

#Leaderboard
@bot.command(name="리더보드")
async def leaderboard(ctx):
    try:
        with open("data.json","r") as f:
            file = json.load(f)
        tempDict = {}
        for i in file:
            tempDict[i] = file[i]["xp"]
        leaderboard = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
        items = leaderboard.items()
        firstTen = list(items)[:10]
        dAgain = dict(firstTen)
        key = dAgain.keys()
        topList = list(key)
        embed=discord.Embed(color=0xff00ea)
        embed.add_field(name="레벨 리더보드", value=f"""
    #1 - <@{topList[0]}>
    #2 - <@{topList[1]}>
    #3 - <@{topList[2]}>
    #4 - <@{topList[3]}>
    #5 - <@{topList[4]}>
    #6 - <@{topList[5]}>
    #7 - <@{topList[6]}>
    #8 - <@{topList[7]}>
    #9 - <@{topList[8]}>
    #10 - <@{topList[9]}>
    """, inline=False)
        embed. set_image(url="https://media.discordapp.net/attachments/870649335451361320/870944688545366057/Narrow_rgb_loading.gif")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("> 리더보드를 보기위한 데이터가 부족합니다")

#Daily
@bot.command(name="오늘레벨")
async def daily(ctx):
    try:
        with open("data.json","r") as f:
            file = json.load(f)
        tempDict = {}
        for i in file:
            tempDict[i] = file[i]["d-xp"]
        leaderboard = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
        items = leaderboard.items()
        firstTen = list(items)[:10]
        dAgain = dict(firstTen)
        key = dAgain.keys()
        topList = list(key)
        embed=discord.Embed(color=0xff00ea)
        embed.add_field(name="오늘의 레벨 리더보드", value=f"""
    #1 - <@{topList[0]}>
    #2 - <@{topList[1]}>
    #3 - <@{topList[2]}>
    #4 - <@{topList[3]}>
    #5 - <@{topList[4]}>
    #6 - <@{topList[5]}>
    #7 - <@{topList[6]}>
    #8 - <@{topList[7]}>
    #9 - <@{topList[8]}>
    #10 - <@{topList[9]}>
    """, inline=False)
        embed. set_image(url="https://media.discordapp.net/attachments/870649335451361320/870944688545366057/Narrow_rgb_loading.gif")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("> 리더보드를 보기위한 데이터가 부족합니다")

#Weekly
@bot.command(name="주간레벨")
async def weekly(ctx):
    try:
        with open("data.json","r") as f:
            file = json.load(f)
        tempDict = {}
        for i in file:
            tempDict[i] = file[i]["w-xp"]
        leaderboard = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
        items = leaderboard.items()
        firstTen = list(items)[:10]
        dAgain = dict(firstTen)
        key = dAgain.keys()
        topList = list(key)
        embed=discord.Embed(color=0xff00ea)
        embed.add_field(name="주간 리더보드", value=f"""
    #1 - <@{topList[0]}>
    #2 - <@{topList[1]}>
    #3 - <@{topList[2]}>
    #4 - <@{topList[3]}>
    #5 - <@{topList[4]}>
    #6 - <@{topList[5]}>
    #7 - <@{topList[6]}>
    #8 - <@{topList[7]}>
    #9 - <@{topList[8]}>
    #10 - <@{topList[9]}>
    """, inline=False)
        embed. set_image(url="https://media.discordapp.net/attachments/870649335451361320/870944688545366057/Narrow_rgb_loading.gif")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("> 리더보드를 보기위한 데이터가 부족합니다")

#Monthly
@bot.command(name="매달레벨")
async def monthly(ctx):
    try:
        with open("data.json","r") as f:
            file = json.load(f)
        tempDict = {}
        for i in file:
            tempDict[i] = file[i]["m-xp"]
        leaderboard = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
        items = leaderboard.items()
        firstTen = list(items)[:10]
        dAgain = dict(firstTen)
        key = dAgain.keys()
        topList = list(key)
        embed=discord.Embed(color=0xff00ea)
        embed.add_field(name="매달 리더보드", value=f"""
    #1 - <@{topList[0]}>
    #2 - <@{topList[1]}>
    #3 - <@{topList[2]}>
    #4 - <@{topList[3]}>
    #5 - <@{topList[4]}>
    #6 - <@{topList[5]}>
    #7 - <@{topList[6]}>
    #8 - <@{topList[7]}>
    #9 - <@{topList[8]}>
    #10 - <@{topList[9]}>
    """, inline=False)
        embed. set_image(url="https://media.discordapp.net/attachments/870649335451361320/870944688545366057/Narrow_rgb_loading.gif")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("> 리더보드를 보기위한 데이터가 부족합니다")

#Daily Loop
@tasks.loop(hours=24)
async def clearDaily():
    with open('data.json', 'r') as f:
        file = json.load(f)
    for i in file:
        file[i]['d-xp'] = 0
        file[i]['daily'] = 1
    with open('data.json', 'w') as f:
        json.dump(file, f, indent=4)
    if str(datetime.datetime.utcnow().day) == "1" or str(datetime.datetime.utcnow().day) == "01":
            with open('data.json', 'r') as f:
                file = json.load(f)
            for i in file:
                file[i]['m-xp'] = 0
                file[i]['monthly'] = 1
            with open('data.json', 'w') as f:
                json.dump(file, f, indent=4)    

#Weekly Loop
@tasks.loop(hours=168)
async def clearWeekly():
    with open('data.json', 'r') as f:
        file = json.load(f)
    for i in file:
        file[i]['w-xp'] = 0
        file[i]['weekly'] = 1
    with open('data.json', 'w') as f:
        json.dump(file, f, indent=4)

bot.run(os.getenv(TOKEN)) #Bot Token
