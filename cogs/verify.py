import discord
from discord.ext import commands

# Role ID to assign upon verification
VERIFIED_ROLE_ID = 1328778534935855254  # Replace with your role ID

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="verify")
    async def verify(self, ctx):
        """Verify a user and assign a role."""
        user = ctx.author
        guild = ctx.guild

        # Check if the role exists in the guild
        role = guild.get_role(VERIFIED_ROLE_ID)
        if not role:
            await ctx.send(f"⚠️ The verification role with ID `{VERIFIED_ROLE_ID}` does not exist in this server.")
            return

        # Check if the user already has the role
        if role in user.roles:
            await ctx.send("✅ You are already verified!")
            return

        # Assign the role
        try:
            await user.add_roles(role, reason="User verified themselves.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to assign roles.")
            return

        # Collect user data
        user_data = {
            "Username": f"{user.name}#{user.discriminator}",
            "User ID": user.id,
            "Account Created": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Server Join Date": user.joined_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Roles": ", ".join([role.name for role in user.roles if role.name != "@everyone"]),
        }

        # Create embed
        embed = discord.Embed(
            title="Verification Successful",
            description="You have been successfully verified! Here's the data we have about you:",
            color=discord.Color.green(),
        )
        for key, value in user_data.items():
            embed.add_field(name=key, value=value, inline=False)

        embed.set_footer(text="If you have questions about your data, contact an admin.")
        embed.set_thumbnail(url=user.avatar.url if user.avatar else guild.icon.url)

        # Send verification message
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Verify(bot))
