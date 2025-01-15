import discord
from discord.ext import commands
import json
from pathlib import Path

# File to save AFK data
AFK_FILE = Path("afk_data.json")

# Load or initialize AFK data
if AFK_FILE.exists():
    with open(AFK_FILE, "r") as f:
        afk_data = json.load(f)
else:
    afk_data = {}

# Save AFK data
def save_afk_data():
    with open(AFK_FILE, "w") as f:
        json.dump(afk_data, f, indent=4)

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_recently_set = set()  # Temporary storage for recently set AFKs

    @commands.command(name="afk")
    async def afk(self, ctx, *, reason: str = "No reason provided"):
        """Set yourself as AFK with an optional reason."""
        user_id = str(ctx.author.id)

        # Check if user is already AFK
        if user_id in afk_data:
            await ctx.send(f"{ctx.author.mention}, you are already AFK. Use `$unafk` to remove your AFK status.")
            return

        # Set user as AFK
        afk_data[user_id] = reason
        save_afk_data()
        self.afk_recently_set.add(user_id)  # Add to temporary storage
        await ctx.send(f"{ctx.author.mention}, you are now AFK: {reason}")

    @commands.command(name="unafk")
    async def unafk(self, ctx):
        """Remove your AFK status."""
        user_id = str(ctx.author.id)

        if user_id not in afk_data:
            await ctx.send(f"{ctx.author.mention}, you are not AFK.")
            return

        # Remove AFK status
        reason = afk_data.pop(user_id)
        save_afk_data()
        await ctx.send(f"Welcome back, {ctx.author.mention}! Your AFK status has been removed: '{reason}'.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)

        # Prevent removing AFK if it was just set
        if user_id in self.afk_recently_set:
            self.afk_recently_set.remove(user_id)  # Remove from temporary storage
            return

        # Remove AFK if the user sends a message
        if user_id in afk_data:
            reason = afk_data.pop(user_id)
            save_afk_data()
            await message.channel.send(f"Welcome back, {message.author.mention}! Your AFK status has been removed: '{reason}'.")

        # Check if someone is pinged and is AFK
        mentions = message.mentions
        for user in mentions:
            if str(user.id) in afk_data:
                reason = afk_data[str(user.id)]
                await message.channel.send(f"{user.mention} is currently AFK: {reason}")

async def setup(bot):
    await bot.add_cog(AFK(bot))
