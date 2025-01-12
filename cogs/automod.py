import discord
from discord.ext import commands
import json
from pathlib import Path

# Save Data
BLOCKED_WORDS_FILE = Path("blocked_words.json")

# loading
if BLOCKED_WORDS_FILE.exists():
    with open(BLOCKED_WORDS_FILE, "r") as f:
        blocked_words = json.load(f)
else:
    blocked_words = []

# Sava
def save_blocked_words():
    with open(BLOCKED_WORDS_FILE, "w") as f:
        json.dump(blocked_words, f, indent=4)

class AutoModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addword")
    @commands.has_permissions(administrator=True)
    async def add_word(self, ctx, *, word: str):
        """Fügt ein Wort zur Blockliste hinzu."""
        if word in blocked_words:
            await ctx.send(f"Das Wort `{word}` steht bereits auf der Blockliste.")
            return

        blocked_words.append(word)
        save_blocked_words()
        await ctx.send(f"Das Wort `{word}` wurde der Blockliste hinzugefügt.")

    @commands.command(name="removeword")
    @commands.has_permissions(administrator=True)
    async def remove_word(self, ctx, *, word: str):
        """Entfernt ein Wort von der Blockliste."""
        if word not in blocked_words:
            await ctx.send(f"Das Wort `{word}` steht nicht auf der Blockliste.")
            return

        blocked_words.remove(word)
        save_blocked_words()
        await ctx.send(f"Das Wort `{word}` wurde von der Blockliste entfernt.")

    @commands.command(name="listwords")
    @commands.has_permissions(administrator=True)
    async def list_words(self, ctx):
        """Zeigt alle blockierten Wörter an."""
        if not blocked_words:
            await ctx.send("Die Blockliste ist leer.")
            return

        await ctx.send("Blockierte Wörter:\n" + "\n".join(f"- {word}" for word in blocked_words))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Überprüft Nachrichten auf blockierte Wörter."""
        if message.author.bot:
            return

        for word in blocked_words:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention}, diese Nachricht enthält ein blockiertes Wort und wurde entfernt.")
                return

async def setup(bot):
    await bot.add_cog(AutoModeration(bot))
