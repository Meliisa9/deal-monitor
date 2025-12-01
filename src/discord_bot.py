import discord
import os
import random
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_NAME = "deals"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ TEST-PING
@bot.command()
async def ping(ctx):
    await ctx.send("PONG ✅")

# ✅ FEJK DEALS (kommer ersättas med riktiga senare)
DEALS = [
    "🔥 50% rabatt på Nike-skor – https://example.com",
    "💻 Gaming-tangentbord -30% – https://example.com",
    "🎧 AirPods på REA – https://example.com",
    "📱 iPhone-tillbehör -40% – https://example.com",
]

# ✅ LOOP SOM SKICKAR DEAL AUTOMATISKT
@tasks.loop(minutes=2)
async def post_deal():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
        if channel:
            deal = random.choice(DEALS)
            await channel.send(deal)

@bot.event
async def on_ready():
    print(f"✅ Bot är online som {bot.user}")
    post_deal.start()

def run_bot():
    bot.run(TOKEN)
