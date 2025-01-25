import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1284517411005005948
        self.role1_id = 1287132493547569192
        self.role2_id = 1284519960143462584

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
                title="Welcome to the Server!",
                description=(
                    f"Hello {member.mention}, Welcome, If you have any questions, use our support system. Have fun on the Discord!\n\n"
                    f"You are member **#{len(member.guild.members)}**!"
                ),
                color=discord.Color.blue()
            )
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else "https://via.placeholder.com/150")

            embed.set_footer(text="We hope you enjoy your time here!")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
