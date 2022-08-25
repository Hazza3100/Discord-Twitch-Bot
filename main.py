import threading
import discord
import requests
import random
import json


from discord.ext import commands



with open('config.json') as f:
    cfg = json.load(f)

token = cfg['bot_token']
prefix = cfg['prefix']
color = 0xfb00ff
bot_channel1 = cfg['bot_channel1']
bot_channel2 = cfg['bot_channel2']
use_proxy = cfg['use_proxy']
dont_change = cfg['dont_change']
role_1 = cfg['role1']
role_2 = cfg['role2']
role_3 = cfg['role3']
role_4 = cfg['role4']
role_5 = cfg['role5']

default_amount = cfg['default_amount']
role1_amount = cfg['role1_amount']
role2_amount = cfg['role2_amount']
role3_amount = cfg['role3_amount']
role4_amount = cfg['role4_amount']
role5_amount = cfg['role5_amount']


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)




def get_user(channel_name):

    json = {"operationName": "ChannelShell",
            "variables": {
                "login": channel_name
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
                }
            }
        }

    headers = {
        'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
    }
    r = requests.post('https://gql.twitch.tv/gql', json=json, headers=headers)
    return r.json()['data']['userOrError']['id']



@bot.command()
async def follow(ctx, channel_name):
    if ctx.channel.id == int(bot_channel1) or ctx.channel.id == int(bot_channel2):
        if dont_change == True:
            print("Change config dont_change to false")
        else:
            username = get_user(channel_name)

            role1 = discord.utils.get(ctx.guild.roles, name=role_1)
            role2 = discord.utils.get(ctx.guild.roles, name=role_2)
            role3 = discord.utils.get(ctx.guild.roles, name=role_3)
            role4 = discord.utils.get(ctx.guild.roles, name=role_4)
            role5 = discord.utils.get(ctx.guild.roles, name=role_5)

            follow_amount = default_amount

            if role5 in ctx.author.roles:
                follow_amount = role5_amount
            elif role4 in ctx.author.roles:
                follow_amount = role4_amount
            elif role3 in ctx.author.roles:
                follow_amount = role3_amount
            elif role2 in ctx.author.roles:
                follow_amount = role2_amount
            elif role1 in ctx.author.roles:
                follow_amount = role1_amount

            embed = discord.Embed(title="Twitch followers", description=f"Sending **{follow_amount}** Twitch Followers to **{channel_name}**", color=color)
            await ctx.send(embed=embed, delete_after=5)
            await ctx.message.delete()


            def follow_user():
                for i in range(follow_amount):
                    token = open('tokens.txt', 'r').read().splitlines()
                    tokens = random.choice(token)

                    proxy_list = open('proxies.txt','r').read().splitlines()


                    proxy = random.choice(proxy_list)
                    proxies = {
                    'http': f'http://{proxy}',
                    'https':f'http://{proxy}'
                    }

                    headers = {
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-GB",
                        "Authorization": f"OAuth {tokens}",
                        "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
                        "Connection": "keep-alive",
                        "Content-Length": "541",
                        "Content-Type": "text/plain;charset=UTF-8",
                        "Host": "gql.twitch.tv",
                        "Origin": "https://www.twitch.tv",
                        "Referer": "https://www.twitch.tv/",
                        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": "Windows",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                        }

                    json = {
                    "operationName": "FollowButton_FollowUser",
                    "variables": {
                        "input": {
                        "disableNotifications": False,
                        "targetID": f"{username}"
                        }
                    },
                    "extensions": {
                        "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08"
                        }
                    }
                    }
                    if use_proxy == False:
                        r = requests.post('https://gql.twitch.tv/gql', headers=headers, json=json)
                    else:
                        r = requests.post('https://gql.twitch.tv/gql', headers=headers, json=json, proxies=proxies)

            threading.Thread(target=follow_user).start()

bot.run(token)
