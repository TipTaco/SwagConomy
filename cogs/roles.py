from discord.ext import commands

class RolesCog(commands.cog):

    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(RolesCog(bot))

