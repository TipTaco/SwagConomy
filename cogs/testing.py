from discord.ext import commands
import discord
import helpers
import sql_db


class TestingCog(commands.Cog, name='Testing'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='initialise', aliases=['init'])
    async def _init(self, ctx, user: discord.User):
        if not helpers.check_channel(ctx): return

        user_id = ctx.author.id
        if user is not None:
            user_id = user.id

        sql_db.safe_add_entry(helpers.conn, user_id, ctx.guild.id)

        print("Received command INITIALISE from", ctx.message.author)
        await ctx.send('Initialised ' + str(helpers.disp_name(ctx.guild.get_member(user_id))))


    @commands.command(name='balance', aliases=['bal', 'b'])
    async def _balance(self, ctx, *args):
        if not helpers.check_channel(ctx): return
        print("Received command BALANCE from", ctx.message.author)
        await ctx.send("Command Received")
        bal = sql_db.select_entry(helpers.conn, ctx.author.id, ctx.guild.id)
        await ctx.send("Database got" + str(bal))

        embed = discord.Embed(title="Balance", color=helpers.bot_color(ctx))
        await ctx.send("Embed made")

        embed.add_field(name=helpers.get_user(bal[0]), value="${:.2f}".format(bal[2]))
        await ctx.send("Field added")

        if bal != 0:
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to get bal")

    @commands.command(name='add', aliases=['a'])
    #@commands.has_role('King')
    async def _add(self, ctx, *args):
        if not helpers.check(ctx): return
        if len(args) <= 0: return
        print("Received command ADD from", ctx.message.author)

        sql_db.update_entry(helpers.conn, ctx.author.id, ctx.guild.id, float(args[0]))

        await ctx.send('Added balance of ' + str(args[0]) + ' to ' + str(helpers.disp_name(ctx.author)))


    @commands.command(name='pay', aliases=['p', 'send'])
    async def _pay(self, ctx, user: discord.User, amount: float):
        if user is None: return

        bal = sql_db.select_entry(helpers.conn, user.id, ctx.guild.id)
        if bal == 0:
            return
        else:
            await self._add_to_user(ctx.author.id, ctx.guild.id, -amount)
            await self._add_to_user(user.id, ctx.guild.id, amount)
            await ctx.send("Sent " + str(amount) + " to " + user.name)


    async def _add_to_user(self, user_id, guild_id, amount=0.0):
        sql_db.update_entry(helpers.conn, user_id, guild_id, float(amount))

    @commands.command(name='balancetop', aliases=['baltop', 'bt'])
    async def _balance_top(self, ctx, *args):
        print("Received command BALANCE TOP from", ctx.message.author)

        balances = sql_db.select_entry_sorted(helpers.conn, ctx.guild.id)

        embed = discord.Embed(title="Top 10 Balances", color=helpers.bot_color(ctx))

        for bal in balances[0:max(10, len(balances))]:
            if (len(args) > 0 and bal[2] >= float(args[0])) or len(args)==0:
                embed.add_field(name=helpers.get_user(bal[0]), value="${:.2f}".format(bal[2]), inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TestingCog(bot))