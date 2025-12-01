import discord
import os
import random
from discord.ext import tasks, commands
from dotenv import load_dotenv

from .scrapers.webhallen import get_webhallen_deals
from .scrapers.elgiganten import get_elgiganten_deals
from .scrapers.amazon import get_amazon_deals
from .scrapers.power import get_power_deals

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_NAME = "deals"

MIN_DISCOUNT = 30  # Admin kan ändra detta
ADMIN_IDS = [ ]   # Lägg in ditt Discord-ID här senare

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# ✅ BASIC COMMANDS
# =========================

@bot.command()
async def ping(ctx):
    await ctx.send("PONG ✅ Boten fungerar!")

@bot.command()
async def setdiscount(ctx, percent: int):
    global MIN_DISCOUNT
    MIN_DISCOUNT = percent
    await ctx.send(f"✅ Minimirabatt satt till {percent}%")

# =========================
# ✅ AI FILTER (FAKE-REA SKYDD)
# =========================

def ai_filter(deal):
    title = deal["title"].lower()

    blacklist = ["skyddsfodral", "usb-kabel", "refurbished"]
    for word in blacklist:
        if word in title:
            return False

    return True

# =========================
# ✅ PRICE ERROR DETECTION
# =========================

def is_price_error(deal):
    try:
        price = float(deal["price"].replace("kr", "").replace(",", "."))
        return price < 50
    except:
        return False

# =========================
# ✅ AFFILIATE LINKS
# =========================

def affiliate_link(url, store):
    tags = {
        "Amazon": "?tag=dinaffiliate-21",
        "Webhallen": "?ref=dealbot",
        "Elgiganten": "?utm_source=dealbot",
        "Power": "?utm_source=dealbot"
    }

    return url + tags.get(store, "")

# =========================
# ✅ EMBED BUILDER
# =========================

def build_embed(deal):
    embed = discord.Embed(
        title=deal["title"],
        url=affiliate_link(deal["link"], deal["store"]),
        description=f"🏪 {deal['store']}\n💸 Pris: {deal['price']}",
        color=0x00ff00
    )

    embed.add_field(name="🔥 Rabatt", value=f"{deal['discount']}%", inline=True)

    if is_price_error(deal):
        embed.add_field(name="⚠️ PRICE ERROR", value="Extremt lågt pris!", inline=False)

    return embed

# =========================
# ✅ DEAL SCANNER
# =========================

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
                if deal["discount"] >= MIN_DISCOUNT and ai_filter(deal):
                    embed = build_embed(deal)
                    await channel.send(embed=embed)

# =========================
# ✅ STARTUP
# =========================

@bot.event
async def on_ready():
    print(f"✅ Bot är online som {bot.user}")
    scan_deals.start()

def run_bot():
    bot.run(TOKEN)
