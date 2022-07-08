import asyncio
import json
import os
import random
import sys
import threading
import tracemalloc
import discord
import httpx
import psutil
import requests
import socks
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands, tasks

tracemalloc.start()

color = 0x00a1d8
administrators = 835446404503437331

def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix
    
config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

queue = []

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()

@bot.command()
async def stock(ctx):
 if ctx.channel.type != discord.ChannelType.private:
        filefile = open('tokens.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        filefile = open('ttoken_spam.txt')
        snum_lines = sum(1 for line in filefile)
        filefile.close()
        embed=discord.Embed(title="Phoenix Stock",color=3447003, description=f"Twitch Stock:\n \nFollow: **{fnum_lines}**\nSpam: **{snum_lines}** ")
        await ctx.send(embed=embed)









@bot.event
async def on_ready():
    print(f'Servers: {len(bot.guilds)}')
    for guild in bot.guilds:
        print(guild.name)
    print()
    bot.loop.create_task(Status_Rotate())
    while True:
        members = sum([guild.member_count for guild in bot.guilds])
        filefile = open('tokens.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        activity = discord.Activity(type=discord.ActivityType.watching, name=f'{fnum_lines} tokens!')
        await bot.change_presence(activity=activity)
        await asyncio.sleep(60)

@tasks.loop()
async def Status_Rotate(seconds=5):
    members = sum([guild.member_count for guild in bot.guilds])
    filefile = open('tokens.txt')
    fnum_lines = sum(1 for line in filefile)
    filefile.close()

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'?? {members} Members')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(30)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'?? {fnum_lines} Stock')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(30)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'discord.gg/phts')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(30)



@bot.command()
async def regular(ctx):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    embed=discord.Embed(title="Receive regular",color=3447003, description=f"```discord.gg/phts``` In your status")
    await ctx.send(embed=embed)

def get_id(user):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None

@bot.event
async def on_member_update(before, after):
    role_id = 959154592690626590
    role = get(before.guild.roles, id=role_id)
    if 'discord.gg/phts' in str(before.activities):
      if 'discord.gg/phts' in str(after.activities):
        pass
      else:
        await after.remove_roles(role)
        channel = bot.get_channel(967478555753730110)
        embed=discord.Embed(description=f"Regular has been removed from {after.mention}", color=discord.Color.red())
        await channel.send(embed=embed)

    if 'discord.gg/phts' in str(after.activities):
        await after.add_roles(role)
        channel = bot.get_channel(967478555753730110)
        embed=discord.Embed(description=f"{after.mention} has claimed Regular!", color=discord.Color.green())
        await channel.send(embed=embed)
    
@bot.command()
async def help(ctx):
    config_file = get_config()
    json_object = json.loads(config_file)
    prefix = json_object['bot_config']["prefix"]
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}help')
    if ctx.channel.type != discord.ChannelType.private:
            embed = discord.Embed(title='Phoenix Bot',description='DM The Bot ``.help``.', color=color)
            await ctx.send(embed=embed)
    else:
            embed = discord.Embed(title='__Phoenix__',description='Help Commands.', color=color)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/842859157295202395/919216214209880084/Phoenix_Tools_Logo.gif')
            embed.add_field(name='Help', value=f'```{prefix}help```', inline=True)
            embed.add_field(name='Twitch Followers', value=f'```{prefix}tfollow <channel>```', inline=False)
            embed.add_field(name='Twitch Unfollow', value=f'```{prefix}tunfollow <channel> (Staff Only)```', inline=False)
            embed.add_field(name='Twitch Spam', value=f'```{prefix}tspam <channel> <message>```', inline=False)
            embed.add_field(name='Twitch Raid', value=f'```{prefix}raid <raidID>```', inline=False)
            embed.add_field(name='Twitch Hosts', value=f'```{prefix}thost <channel>```', inline=False)
            embed.add_field(name='Twitch Views', value=f'```{prefix}tview <channel>```', inline=False)
            embed.add_field(name='Twitch Friends', value=f'```{prefix}tfriend <channel>```', inline=False)
            embed.add_field(name='Twitch Report', value=f'```{prefix}treport <user>```', inline=False)
            embed.add_field(name='Twitch Stock', value=f'```{prefix}stock```', inline=False)
            embed.add_field(name='Regular', value=f'```{prefix}regular```', inline=False)
            await ctx.send(embed=embed)


@bot.command()
async def hazhelp(ctx):
    config_file = get_config()
    json_object = json.loads(config_file)
    prefix = json_object['bot_config']["prefix"]
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}help')
    embed = discord.Embed(title='__Phoenix__',description='Hazza Commands.', color=color)
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/835446404503437331/a_24e2b6a64ae253c8b05e31c2ee15fe98.gif?size=4096')
    embed.add_field(name='Help', value=f'```{prefix}hazhelp```', inline=True)
    embed.add_field(name='Server IP', value=f'```{prefix}ip```', inline=True)
    embed.add_field(name='Restart Bot', value=f'```{prefix}restartbot```', inline=True)
    embed.add_field(name='Change Prefix', value=f'```{prefix}setprefix```', inline=True)
    embed.add_field(name='Custom amount of follows', value=f'```{prefix}tcustom <user> <amount>```', inline=False)
    embed.add_field(name='Instagram Followers', value=f'```{prefix}igfollow <user> <amount>```', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> {bot.command_prefix}clear')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=None)
            await ctx.send('**Cleared by Hazza! :sunglasses:**')
        else:
            await ctx.message.delete()

@bot.command()
async def tfollow(ctx, arg):
 logschannel = bot.get_channel(967478555753730110)   
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfollow')
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**Error** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=3447003, description=f" Adding **{num_lines}** follows to **{arg}** :fire:")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=3447003, description=f" Adding **{follow_count}** Twitch Follows to **{arg}**")
                    await ctx.send(embed=embed)
                    Logembed = discord.Embed(color=15418782, description=f"{ctx.author.mention} Sent **{follow_count}** Follows to **{arg}** ")
                    await logschannel.send(embed=Logembed)
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = random.choice(open("tokens.txt", "r" ).read().splitlines())

                            proxy_list = open('proxy.txt','r').read().splitlines()


                            proxy = random.choice(proxy_list)
                            proxies = {
                            'http': f'http://{proxy}',
                            'https':f'http://{proxy}'
                            }
                            
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break

@bot.command()
@commands.has_any_role('.','Staff')
async def tunfollow(ctx, arg):
 logschannel = bot.get_channel(967478555753730110)   
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfollow')
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**Error** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=3447003, description=f" Removing **{num_lines}** follows from **{arg}** ??")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=3447003, description=f" Removing **{follow_count}** Twitch Follows from **{arg}**")
                    await ctx.send(embed=embed)
                    await logschannel.send(f'{ctx.author.mention} Removed **{follow_count}** from **{arg}**')
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = random.choice(open("tokens.txt", "r" ).read().splitlines())
                            
                            payload = '[{\"operationName\":\"FollowButton_UnfollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"f7dae976ebf41c755ae2d758546bfd176b4eeb856656098bb40e0a672ca0d880\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break




@bot.command()
@commands.has_role('.')
async def tcustom(ctx, arg, amount:int):
 logschannel = bot.get_channel(967478555753730110)   
 if ctx.channel.type != discord.ChannelType.private:
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfollow')
    role_config = json.loads(config_file)['tfollow']
    for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = amount
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**Error** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                embed=discord.Embed(color=3447003, description=f" Adding **{follow_count}** Twitch Follows to **{arg}**")
                await ctx.send(embed=embed)
                await logschannel.send(f'{ctx.author.mention} Sent **{follow_count}** To **{arg}**')
                follow_count = amount

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range (amount):
                        
                        try:
                            ttoken = random.choice(open("tokens.txt", "r" ).read().splitlines())
                            
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break


@bot.command()
@commands.has_role('.')
async def tfollowproxy(ctx, arg):
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel =json_object['bot_config']["twitch_channel"]
    if ctx.channel.id == int(genchannel):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                target_id = get_id(arg)

                if target_id == None:
                    embed=discord.Embed(color=color, description=f"**Error** `ID SCRAPE Error {arg}`")
                    await ctx.send(embed=embed)
                    break
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                filefile = open('tokens.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    embed=discord.Embed(color=color, description=f"**Sending** `{num_lines}` Followers TO `{arg}`")
                    await ctx.send(embed=embed)
                    caunt_to_follow = num_lines
                else:
                    embed=discord.Embed(color=color, description=f"**Sending** {follow_count} Followers TO `{arg}`")
                    await ctx.send(embed=embed)
                    caunt_to_follow = follow_count
                class Follow():
                    sent = 0
                        
                def start_follow():
                    for i in range(caunt_to_follow):
                        try:
                            session = requests.Session()
                            proxy = random.choice(open("proxy.txt","r").read().splitlines())
                            proxies = {"https": f"http://{proxy}"}
                            ttoken = tokens[i]
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                            session.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxies, timeout=30)
                        except: None
                x = threading.Thread(target=start_follow)
                x.start()
                break

@bot.command()
async def tspam(ctx, arg1, *, args):
 if ctx.channel.type != discord.ChannelType.private:
    logschannel = bot.get_channel(967478555753730110)
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tspam')
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"] 
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['tspam'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                def start_spam():
                    for i in range(2):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me {args} \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=3447003, description=f"Sending **{x}** messages to **{arg1}**")
                await ctx.send(embed=embed)
                await logschannel.send(f'{ctx.author.mention} Sent **{spam_count}** spam To **{arg1}**')
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break
            
@bot.command()
async def treport(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    logschannel = bot.get_channel(967478555753730110)
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}treport')
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]
    
                
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        
        role_config = json.loads(config_file)['treport']
        for role_name in role_config:
            spam_count = json.loads(config_file)['treport'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                
                num_lines = sum(1 for line in open('tokens.txt'))
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**Error** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                
                def start_spam(ttoken):
                    xcc = open("report_reason.txt","r")
                    reportndescription = random.choice(xcc.read().splitlines())
                    xcc.close()
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '32193c1413662035',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"ReportUserModal_ReportUser","variables":{"input":{"description":"report context: USER_REPORT\\n\\nvideo > terrorism_mass_violence\\n\\ndescription: '+reportndescription+'","reason":"terrorism_mass_violence","content":"LIVESTREAM_REPORT","contentID":"","extra":"","targetID":"'+target_id+'","wizardPath":["video","terrorism_mass_violence"]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"dd2b8f6a76ee54aff685c91537fd75814ffdc732a74d3ae4b8f2474deabf26fc"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data).text

                    except:
                        None
                            
                            
                embed=discord.Embed(color=3447003, description=f"Sending **{spam_count}** reports to **{arg}**")
                await ctx.send(embed=embed)
                await logschannel.send(f'{ctx.author.mention} Sent **{spam_count}** reports To **{arg}**')
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                    
                try:
                    
                    for i in range(x):
                        c = open("tokens.txt")
                        ttoken = random.choice(c.read().splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                        c.close()
                        
                except:
                    None
                break
    
@bot.command()
async def tfriend(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    logschannel = bot.get_channel(967478555753730110)
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfriend')
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]

    if ctx.channel.id == int(genchannel) or ctx.channel.id ==int(genchannel2): 
        role_config = json.loads(config_file)['tfriend']
        for role_name in role_config:
            spam_count = json.loads(config_file)['tfriend'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"Error Invalid username {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                def start_spam(ttoken):
                    
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '99ef7e05659bbca4',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"FriendButton_CreateFriendRequest","variables":{"input":{"targetID":"'+target_id+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"380d8b19fcffef2fd8654e524444055dbca557d71968044115849d569d24129a"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)

                    except:
                        None 
                embed=discord.Embed(color=3447003, description=f"Sending **{spam_count}** friends to **{arg}**")
                await ctx.send(embed=embed)
                await logschannel.send(f'{ctx.author.mention} Sent **{spam_count}** friends To **{arg}**')
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                try:
                    for i in range(x):
                        xx = open("tokens.txt").read()
                        ttoken = random.choice(xx.splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                except:
                    None
                break

@bot.command()
async def ttrollfor(ctx, arg1):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}ttroll')
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]  
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['ttroll'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me GET TROLLED LOL \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=3447003, description=f" **{arg1}** getting trolled for **{x}** times!")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break

@bot.command()
async def traidd(ctx, arg1):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}traid')
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]  
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['traid']
        for role_name in role_config:
            spam_count = json_object['traid'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me Get raided by {ctx.author} \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=3447003, description=f" **{arg1}** getting raided for **{x}** times!")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break

@bot.command()
async def raidold(ctx, arg):
 logschannel = bot.get_channel(967478555753730110)   
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfollow')
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**Error** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                filefile = open('tokens.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=3447003, description=f"Adding **{num_lines}** follows to **{arg}** ??")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=3447003, description=f"Adding **{follow_count}** follows to **{arg}** ??")
                    await ctx.send(embed=embed)
                    await logschannel.send(f'{ctx.author.mention} Sent **{follow_count}** to **{arg}**')
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = random.choice(open("tokens.txt", "r" ).read().splitlines())
                            
                            payload = '[{"operationName":"chatCreateRaid","variables":{"input":{"sourceID":"531102483","targetID":"422939631"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"f4fc7ac482599d81dfb6aa37100923c8c9edeea9ca2be854102a6339197f840a"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("tokens.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("tokens.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break

@bot.command()
async def thost(ctx, arg1):
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}host')
    logschannel = bot.get_channel(967478555753730110)
    if  discord.utils.get(ctx.guild.roles, name='Loyal') in ctx.author.roles or discord.utils.get(ctx.guild.roles, name='Chatter') in ctx.author.roles or discord.utils.get(ctx.guild.roles, name='.') in ctx.author.roles or discord.utils.get(ctx.guild.roles, name='Active') in ctx.author.roles:
        config_file = get_config()
        json_object = json.loads(config_file)
        genchannel = json_object['bot_config']["twitch_channel"] 
        genchannel2 = json_object['bot_config']["twitch_channel_2"]
        if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
            role_config = json.loads(config_file)['thost']
            for role_name in role_config:
                spam_count = json_object['thost'][role_name]
                role_id = discord.utils.get(ctx.guild.roles, name=role_name)
                if role_id in ctx.author.roles:    
                    xfile = open('ttoken_spam.txt')
                    num_lines = sum(1 for line in xfile)
                    xfile.close()
                    target_id = get_id(arg1)
                    def start_spam():
                        for i in range(5):
                            try:
                                filefile = open("ttoken_spam.txt")
                                ttoken = random.choice(filefile.read().splitlines())
                                filefile.close()
                                try:
                                    payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                    headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                    httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                                except:
                                    None
                                def test_proxy():
                                    while True:
                                        try:
                                            proxyfile = open("proxy.txt","r")
                                            proxy = random.choice(proxyfile.read().splitlines())
                                            proxyfile.close()
                                            session = requests.Session()
                                            proxies = {"https": f"http://{proxy}"}
                                            session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                            return proxy
                                        except:
                                            None
                                headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                                response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                                proxy = test_proxy().split(":")
                                token_name = response['login']
                                s = socks.socksocket()
                                s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                                s.connect(("irc.chat.twitch.tv", 6667))
                                s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                                s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                                s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                                s.send(('PRIVMSG #' + token_name + f' :/raid {arg1} \r\n').encode('utf8'))
                                s.close()
                            except Exception as e:
                                print(e)
                            
                    if num_lines < spam_count:
                        x = num_lines
                    else:
                        x = spam_count
                            
                    embed=discord.Embed(color=color, description=f"Hosting **{arg1}** **{spam_count}** times wait 2-3 minutes!")
                    await ctx.send(embed=embed)
                    await logschannel.send(f'{ctx.author.mention} Hosted **{arg1}** **{spam_count}** times')
                    try:
                        for i in range(x):

                            threading.Thread(target=start_spam).start()
                    except:
                        None
                    break
    else:
        embed = discord.Embed(color=color, description='Only **Loyal, Chatter** can use this!')
        await ctx.send(embed=embed)

View_Channel = 959820125912043582


@bot.command()
@commands.has_any_role('Loyal','Chatter','.')
async def tview(ctx, channel):
    logschannel = bot.get_channel(967478555753730110)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}view')
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
    #if ctx.channel.id == View_Channel:
        if discord.utils.get(ctx.guild.roles, name='Loyal') in ctx.author.roles or discord.utils.get(ctx.guild.roles, name='Chatter') or discord.utils.get(ctx.guild.roles, name='.') in ctx.author.roles:

            role4 = discord.utils.get(ctx.guild.roles, name="Chatter")
            role5 = discord.utils.get(ctx.guild.roles, name="Loyal")
            role6 = discord.utils.get(ctx.guild.roles, name=".")

            follow_count = 35

            if role4 in ctx.author.roles:
                follow_count = 30
            elif role5 in ctx.author.roles:
                follow_count = 50
            elif role6 in ctx.author.roles:
                follow_count = 500


            embed = discord.Embed(color=3447003, description=f"Sending **{follow_count}** Views to **{channel}** ")
            await ctx.send(embed=embed)

            Logembed = discord.Embed(color=15418782, description=f"{ctx.author.mention} Sent **{follow_count}** Views to **{channel}** ")
            await logschannel.send(embed=Logembed)        

            def send_views():

                for i in range(50000):

                    lines = open("proxy.txt", "r").read().splitlines()
                    proxy = random.choice(lines)
                    proxies = {"http": "http://"+proxy, "https": "http://"+proxy}  

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-US',
                        'Authorization': 'undefined',
                        'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain; charset=UTF-8',
                        'Device-ID': '6GsDKc6Jagdhp140DfRs7IjMgInpV5Iw',
                        'Origin': 'https://www.twitch.tv',
                        'Prefer': 'safe',
                        'Referer': 'https://www.twitch.tv/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
                        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    data = '{"operationName":"PlaybackAccessToken_Template","query":"query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}","variables":{"isLive":true,"login":"'+channel+'","isVod":false,"vodID":"","playerType":"site"}}'
                    try:
                        r = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data, proxies=proxies)
                        #print(response.text)
                        start = r.text.find('"value":"') + 9
                        end = r.text.find('","signature')
                        xtoken = r.text[start:end]
                        token = xtoken.replace('\\', '')
                        start = r.text.find('signature":"') + 12
                        end = r.text.find('","__typename')
                        sig = r.text[start:end]
                        linktoken = token.replace('{', '%7B').replace('}', '%7D').replace('"', "%22").replace(':', '%3A').replace(',', '%2C')
                    except:
                        None

                    headers = {
                        'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
                    }

                    params = {
                        'allow_source': 'true',
                        'fast_bread': 'true',
                        'p': '3839592',
                        'play_session_id': '587e61679bcc5503d760eda271c30dc0',
                        'player_backend': 'mediaplayer',
                        'playlist_include_framerate': 'true',
                        'reassignments_supported': 'true',
                        'sig': sig,
                        'supported_codecs': 'avc1',
                        'token': token,
                        'cdm': 'wv',
                        'player_version': '1.10.0',
                    }
                    try:
                        response = requests.get(f'https://usher.ttvnw.net/api/channel/hls/{channel}.m3u8?allow_source=true&fast_bread=true&p=5725800&play_session_id=df4348c5caad4f981aba7aab8df7759a&player_backend=mediaplayer&playlist_include_framerate=true&reassignments_supported=true&sig={sig}&supported_codecs=avc1&token={linktoken}&cdm=wv&player_version=1.10.0', params=params, headers=headers, proxies=proxies)
                        start = response.text.find('https://video-weaver')
                        end = response.text.find('.m3u8') + 5
                        link = response.text[start:end]
                    except:
                        None
                    #print(response.status_code)

                    headers = {
                        'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
                    }
                    try:
                        requests.get(link, headers=headers, proxies=proxies)
                        #print(response.status_code)
                    except:
                        None
                    for x in range(15):
                        threading.Thread(target=send_views).start()


#Misc commands

r = requests.post("https://www.iplocation.net/find-ip-address")

#print(r.text)


ipInfo = requests.get('https://ipinfo.io/ip').text
#print(ipInfo)

@bot.command()
@commands.has_role('.')
async def ip(ctx):
    await ctx.send(f'Server IP is: **{ipInfo}**')




@bot.command()
async def ping(ctx):
    hazza = discord.Embed(title = '__Server Usage__', description = '', color=color)
    hazza.add_field(name = 'Ping', value =f"{round(bot.latency * 1000)}ms", inline = False)
    hazza.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    hazza.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
    hazza.add_field(name = 'Available Memory', value = f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%', inline = False)
    await ctx.send(embed = hazza)







bot.run(token)