from discord.ext import commands
import discord
from discord import app_commands
import random
import praw
from musicmain import *
from windpower import *
import re
from funionpraw import *
import requests




url = "https://discord.com/api/v10/applications/1118513672835301459/commands"
json = {
    "name": "blep",
    "type": 1,
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot FunionBot#9084"
}


r = requests.post(url, headers=headers, json=json)




reddit= praw.Reddit(
    client_id="KGm4wiSMA0UNCOnLa0wjKQ",
    client_secret="_HWsTH494M17czrc6mKWygDo7cVY8w",
    username="FunionBot",
    password="78787890Hi!",
    user_agent="funionbot"
)




BOT_TOKEN = "MTExODUxMjI1MDA0MzUwMjU5Mw.Gx8AXg.iCFnjTqRwi6fQj4byuTu9eDrvlgTzHcY4bQXbk"
CHANNEL_ID = 1118513672835301459
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "getwind", description = "Get the current UK wind", guild=discord.Object(id=1118513672835301459)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@bot.command()
async def hello(ctx):
	await ctx.send("Hello!")

@bot.command()
async def add(ctx, x, y):
	result = int(x) + int(y)
	await ctx.send(f"{x} + {y} = {result}")

@bot.command()
async def boink(ctx):
	await ctx.send("boink to you too")

@bot.command()
async def shiba(ctx):
	subreddit = reddit.subreddit("shiba")
	all_subs = []
	hot = subreddit.hot(limit = 50)

	for submission in hot:
		all_subs.append(submission)

	random_sub = random.choice(all_subs)
	extension = random_sub.url[len(random_sub.url)-3:].lower()

	while extension not in ["jpg", "png"]:
		random_sub = random.choice(all_subs)
		extension = random_sub.url[len(random_sub.url) - 3 :].lower()
	name = random_sub.title
	url = random_sub.url
	em = discord.Embed(title = name)
	em.set_image(url = url)
	await ctx.send(embed = em)

@bot.command()
async def getsong(ctx):
    await ctx.send("What artist are you looking for?")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    try:
        response = await bot.wait_for("message", timeout=30.0, check=check)
        artist_name = response.content
        await ctx.send(f"Searching for {artist_name}...")
    except asyncio.TimeoutError:
        await ctx.send("Request has timed out")

    token = get_token()
    result = search_for_artist(token, artist_name)
    if result is not None:
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)
        if songs:
            song_list = "\n".join([f"{idx + 1}: {song['name']}" for idx, song in enumerate(songs)])
            await ctx.send(f"Here are the top songs:\n{song_list}\nChoose by number to play")
        else:
            await ctx.send("No songs found for this artist.")
    else:
        await ctx.send("No artist with this name exists.")
    
    try:
        response_2 = await bot.wait_for("message", timeout=30.0, check=check)
        song_request = int(response_2.content)
        if 1 <= song_request <= len(songs):
            song = songs[song_request - 1]
            await ctx.send(f"Song found!\nhttps://open.spotify.com/track/{song['uri'][14:]}")
            await ctx.send("Do you want to play the track in the chat?")
        else:
            await ctx.send("Invalid song choice.")
    except asyncio.TimeoutError:
        await ctx.send("Request has timed out")


@bot.command()
async def getwind(ctx):
	 	await ctx.send(f"The wind power in the UK is {get_wind()}GW, last updated: {get_time_ng()}")

@bot.command()
async def getcoal(ctx):
        await ctx.send(f"The coal power in the UK is {get_coal()}GW, last updated: {get_time_ng()}")

@bot.command()
async def getgas(ctx):
        await ctx.send(f"The gas power in the UK is {get_gas()}GW, last updated: {get_time_ng()}")

@bot.command()
async def getsolar(ctx):
        await ctx.send(f"The solar power in the UK is {get_solar()}GW, last updated: {get_time_ng()}")

@bot.command()
async def gethydroelectricity(ctx):
        await ctx.send(f"The hydroelectricity power in the UK is {get_hydro()}GW, last updated: {get_time_ng()}")

@bot.command()
async def getnuclear(ctx):
        await ctx.send(f"The nuclear power in the UK is {get_nuclear()}GW, last updated: {get_time_ng()}")

@bot.command()
async def getbiomass(ctx):
        await ctx.send(f"The biomass power in the UK is {get_biomass()}GW, last updated: {get_time_ng()}")



bot.run(BOT_TOKEN)

