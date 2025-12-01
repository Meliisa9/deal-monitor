import discord
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv

from scrapers.webhallen import get_webhallen_deals
from scrapers.elgiganten import get_elgiganten_deals
from scrapers.amazon import get_amazon_deals
from scrapers.power import get_power_deals

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_NAME = "deals"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("PONG ✅")

def build_embed(deal):
    embed = discord.Embed(
        title=deal["title"],
        url=deal["link"],
        description=f"🏪 {deal['store']}\n💸 Pris: {deal['price']}",
        color=0x00ff00
    )

    if deal["image"]:
        embed.set_thumbnail(url=deal["image"])

    embed.add_field(name="🔥 Rabatt", value=f"{deal['discount']}%", inline=True)
    return embed

@tasks.loop(minutes=2)
async def scan_deals():
    all_deals = []

    all_deals += get_webhallen_deals()
    all_deals += get_elgiganten_deals()
    all_deals += get_amazon_deals()
    all_deals += get_power_deals()

    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

        if channel:
            for deal in all_deals:
                embed = build_embed(deal)
                await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Bot är online som {bot.user}")
    scan_deals.start()

def run_bot():
    bot.run(TOKEN)
