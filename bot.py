import os
import discord
from discord import app_commands

TOKEN = os.environ["DISCORD_BOT_TOKEN"]


class DollarBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


client = DollarBot()


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="SBURB - Land of Dollars and Coins"
        ),
    )
    print("Logged in as", client.user)


@client.tree.command(name="say", description="Make the bot send a message")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    message="What to send",
    channel="Where to send it (defaults to this channel)",
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

    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("Admins only.", ephemeral=True)
        return

    target = channel or interaction.channel
    try:
        await target.send(message)
    except discord.Forbidden:
        await interaction.followup.send(
            "I don't have permission to send there.", ephemeral=True
        )
        return

    await interaction.followup.send("Sent.", ephemeral=True)


client.run(TOKEN)
