from discord.ext import commands
import discord
import helpers


class ChannelsCog(commands.Cog, name='Channels'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='createchannel', aliases=['crchan', 'cc'])
    async def _create_channel(self, ctx, channel_name: str):
        print("Received command CREATE CHANNEL from", ctx.message.author)
        await ctx.guild.create_channel(name=channel_name)


def setup(bot):
    bot.add_cog(ChannelsCog(bot))

