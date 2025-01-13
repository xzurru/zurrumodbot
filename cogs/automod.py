import discord
from discord.ext import commands
import json
from pathlib import Path

# File to store blocked words
BLOCKED_WORDS_FILE = Path("blocked_words.json")

# Load blocked words
if BLOCKED_WORDS_FILE.exists():
    with open(BLOCKED_WORDS_FILE, "r") as f:
        blocked_words = json.load(f)
else:
    blocked_words = []

# Save blocked words
def save_blocked_words():
    with open(BLOCKED_WORDS_FILE, "w") as f:
        json.dump(blocked_words, f, indent=4)

class AutoModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addword")
    @commands.has_permissions(administrator=True)
    async def add_word(self, ctx, *, word: str):
        """Adds a word to the blocklist."""
        if word in blocked_words:
            await ctx.send(f"The word `{word}` is already in the blocklist.")
            return

        blocked_words.append(word)
        save_blocked_words()
        await ctx.send(f"The word `{word}` has been added to the blocklist.")

    @commands.command(name="removeword")
    @commands.has_permissions(administrator=True)
    async def remove_word(self, ctx, *, word: str):
        """Removes a word from the blocklist."""
        if word not in blocked_words:
            await ctx.send(f"The word `{word}` is not in the blocklist.")
            return

        blocked_words.remove(word)
        save_blocked_words()
        await ctx.send(f"The word `{word}` has been removed from the blocklist.")

    @commands.command(name="listwords")
    @commands.has_permissions(administrator=True)
    async def list_words(self, ctx):
        """Displays all blocked words."""
        if not blocked_words:
            await ctx.send("The blocklist is empty.")
            return

        await ctx.send("Blocked words:\n" + "\n".join(f"- {word}" for word in blocked_words))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Checks messages for blocked words."""
        if message.author.bot:
            return

        for word in blocked_words:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention}, your message contained a blocked word and has been removed.")
                return

async def setup(bot):
    await bot.add_cog(AutoModeration(bot))
