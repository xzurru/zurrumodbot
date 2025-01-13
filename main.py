import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys

# Workaround für Windows event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Lade Umgebungsvariablen
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

COGS = ["moderation", "help", "welcome", "rank", "audit", "ticket", "fun", "log", "dev", "casino", "safe_link", "automod", "flag"]

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    
    # Setze den Status des Bots auf "Streamt for help $helpmenu"
    activity = discord.Streaming(name="for help $helpmenu", url="https://twitch.tv/xzurru")
    await bot.change_presence(activity=activity)

async def load_extensions():
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Bot starten
asyncio.run(main())
