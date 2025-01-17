import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys

# Workaround for Windows event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

COGS = [
    "moderation", "help", "welcome", "rank", "ticket", "fun", "log", 
    "dev", "casino", "safe_link", "automod", "flag", "verify", "afk",
    "fishsim"
]

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

    # Set bot status
    activity = discord.Streaming(name="for help $helpmenu", url="https://twitch.tv/xzurru")
    await bot.change_presence(activity=activity)

    # Sync guild-specific commands
    try:
        guild = discord.Object(id=int(GUILD_ID))  # Specific guild
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands successfully to guild {GUILD_ID}.")
    except discord.HTTPException as e:
        print(f"Error syncing commands: {e}")

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

# Start the bot
asyncio.run(main())
