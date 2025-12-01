import discord
from .config import DISCORD_TOKEN

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot är online som {client.user}")

async def run_bot():
    await client.start(DISCORD_TOKEN)
