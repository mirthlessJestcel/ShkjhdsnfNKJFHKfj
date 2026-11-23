import os
import discord

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="SBURB (1 out of 1 players) - Land of Dollars and Coins"
        ),
    )
    print("Logged in as", client.user)


client.run(TOKEN)
