import asyncio
import os
import random
import discord
from discord import app_commands

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

GUILD_ID = 1529673738809905283
WELCOME_CHANNEL_ID = 1529795554932953128
WELCOME_MESSAGE = "hi! welcome to the uhm... whatever! welcome!!! {mention}"

ALLOWED_USER_IDS = [
    344289949605953537,
    1300607456371671057,
    1215802650004820010,
    1506710201720635640,
]

GUILD = discord.Object(id=GUILD_ID)


class DollarBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        await self.tree.sync(guild=GUILD)


client = DollarBot()


async def already_welcomed(channel, member):
    async for message in channel.history(limit=15):
        if message.author.id == client.user.id and member in message.mentions:
            return True
    return False


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="SBURB™  - Land of Barb and Darkness"),
    )
    print("Logged in as", client.user)


@client.event
async def on_member_join(member: discord.Member):
    if member.bot or member.guild.id != GUILD_ID:
        return

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    await asyncio.sleep(random.uniform(0, 2))
    try:
        if await already_welcomed(channel, member):
            return
        await channel.send(WELCOME_MESSAGE.format(mention=member.mention))
    except discord.Forbidden:
        return


@client.tree.command(name="say", description="Employ crackersona!!!", guild=GUILD)
@app_commands.describe(
    message="WHAT YOUR'E SENDING",
    channel="THE CHANNEL YOU'RE SENDING IT TOO, BE CARFUL!!!!!",
)
async def say(
    interaction: discord.Interaction,
    message: str,
    channel: discord.TextChannel | None = None,
):
    try:
        await interaction.response.defer(ephemeral=True)
    except discord.HTTPException:
        return

    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.followup.send("YOU CAN'T FUCKING DO THIS!", ephemeral=True)
        return

    target = channel or interaction.channel
    try:
        await target.send(message)
    except discord.Forbidden:
        await interaction.followup.send("I can't do that :(", ephemeral=True)
        return

    await interaction.followup.send("Seeeent :3", ephemeral=True)


client.run(TOKEN)
