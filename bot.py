import os
import discord

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="DOLLARSTUCK"),
    )
    print("Logged in as", client.user)


client.run(TOKEN)
