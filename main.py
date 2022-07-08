import discord
import requests
import random
from discord.ext import commands



prefix = "."
token = "OTk1MDMxMTg3MDcwMzg2MjY4.GdT2R6.2CVp9hR_3Ljby2VfnsK9MUITkv9PHx0jM-ILpE"
color = 0xfb00ff

bot = commands.Bot(command_prefix=prefix, help_command=None)




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








def follow_user(username):

    token = open('tokens.txt', 'r').read().splitlines()
    tokens = random.choice(token)

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
        "X-Device-Id": "o9Mf6aJaLEuNlPc7a1MOSXkO21SBCMHr",
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
    r = requests.post('https://gql.twitch.tv/gql', headers=headers, json=json)




@bot.command()
async def follow(ctx, channel_name):

    username = get_user(channel_name)

    follow_amount = 25

    embed = discord.Embed(title="Twitch followers", description=f"Sending **{follow_amount}** Twitch Followers to **{username}**", color=color)
    await ctx.send(embed=embed)
    for i in range(int(follow_amount)):
        follow_user(username)


bot.run(token)
