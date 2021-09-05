import requests
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from googleapiclient.discovery import build

client = commands.Bot(command_prefix="++")

Key = "AIzaSyCinMTVoEIIV1H1uQd9js45N-8RtE8BANE"  # Replace with your API key.

BlogID = "8729103923525983742"  # Replace with your BlogId here.

Roles = ["CSGO", "Garry's Mod", "GTA 5"]  # Add your server roles here.

blog = build("blogger", "v3", developerKey=Key)

Token = 'ODc3MDQ1MzUwNjM5MjI2ODkw.YRs6Ig.abGat6kf5CF6s6kSP_4j5Hj4lhQ' # Replace with Discord Bot Token.


@client.event
async def on_ready():
    print("Bot has started running")
    await client.change_presence(activity=discord.Game(name="cmd: ++search"))


@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/" + BlogID + "/posts/search"
    complete_url = base_url + "?q=" + search_term + \
        "&key=" + Key
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n", color=0x349bfc)
    embed.set_author(name="XinDrama - Tempat Download dan Nonton Film Gratis")
    embed.set_thumbnail(url="https://1.bp.blogspot.com/-dg_fms3hg7U/YRtCrnkkIMI/AAAAAAAAAAM/y0Wdq08oWEQ5-LYm_0PQ8yiy7GJW6x2AQCLcBGAsYHQ/s406/20210725_142931.png")
    try:
        for count, value in enumerate(result["items"]):
            title = result["items"][count]["title"]
            url = result["items"][count]["url"]
            embed.description = embed.description + \
                f"{count + 1}. [{title}]({url})\n"
        embed.set_footer(text='This message will be deleted in 1 Hour.')

        await ctx.send(embed=embed, delete_after=3600.0)
    except:
        await ctx.send("There is something wrong with the response.")

client.recentPosts = None
client.recentPostsTime = None
client.recentPostsEdit = None


@tasks.loop(seconds=5.0)
async def fetchUpdates():
    posts = blog.posts().list(blogId=BlogID).execute()
    postsList = posts["items"]
    postTime = postsList[0]["published"]
    if not client.recentPosts:
        client.recentPostsTime = postTime
        client.recentPosts = postsList
    elif client.recentPostsTime != postTime:
        titleValue = str(posts["items"][0]["title"])
        urlValue = str(posts["items"][0]["url"])

        channel = client.get_channel(876861832021831690)  # Add channel ID
        embed = discord.Embed(title="New posts available on the blog!",
                              description=f"[{titleValue}]({urlValue})")

        channel = client.get_channel(876861832021831690)  # Add channel ID
        embed = discord.Embed(title="New posts available on the blog!",
                              description=f"[{titleValue}]({urlValue})")

        embed.set_author(name="DockGo Rewin")
        embed.set_thumbnail(url="https://1.bp.blogspot.com/-dg_fms3hg7U/YRtCrnkkIMI/AAAAAAAAAAM/y0Wdq08oWEQ5-LYm_0PQ8yiy7GJW6x2AQCLcBGAsYHQ/s406/20210725_142931.png")
        for i in Roles:
            if i.lower() in postsList[0]["title"].lower():
                guild = client.guilds[0]
                await channel.send(discord.utils.get(guild.roles, name=i).mention, delete_after=86400.0)
                await channel.send(embed=embed, delete_after=86400.0)
                break

        client.recentPostsTime = postTime
        client.recentPosts = postsList

fetchUpdates.start()

client.run(Token, bot=True)
