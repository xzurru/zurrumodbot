import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1284517411005005948
        self.role1_id = 1284519960143462584
        self.role2_id = 1287132493547569192

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Executes when a member joins the server."""
        channel = self.bot.get_channel(self.welcome_channel_id)
        role1 = member.guild.get_role(self.role1_id)
        role2 = member.guild.get_role(self.role2_id)

        if role1:
            await member.add_roles(role1)
        if role2:
            await member.add_roles(role2)

        if channel:
            embed = discord.Embed(
                description=f"Welcome {member.mention}! Welcome, If you have any questions, use our support system. Have fun on the Discord!",
                color=discord.Color.green()
            )
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url="https://via.placeholder.com/150")
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
