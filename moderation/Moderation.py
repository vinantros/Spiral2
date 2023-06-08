import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')
        

    @commands.command()
    async def delete_channel(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        await ctx.send(f'{channel} has been deleted.')
        

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        await member.add_roles(muted_role)
        await ctx.send(f'{member} has been muted.')
        
    @commands.command()
    async def create_channel(self, ctx, channel_name: str):
        new_channel = await ctx.guild.create_text_channel(channel_name)
        await ctx.send(f'New channel {new_channel.mention} has been created.')

def setup(bot):
    bot.add_cog(Moderation(bot))