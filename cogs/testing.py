from discord.ext import commands
import discord
import helpers


class TestingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='initialise', aliases=['init'])
    async def _init(self, ctx, user: discord.User):
        if not helpers.check_channel(ctx): return

        user_id = ctx.author.id
        if user is not None:
            user_id = user.id

        helpers.sql_db.safe_add_entry(helpers.conn, user_id, ctx.guild.id)

        print("Received command INITIALISE from", ctx.message.author)
        await ctx.send('Initialised ' + str(helpers.disp_name(ctx.guild.get_member(user_id))))


    @commands.command(name='balance', aliases=['bal', 'b'])
    async def _balance(self, ctx, *args):
        if not helpers.check_channel(ctx): return
        print("Received command BALANCE from", ctx.message.author)

        bal = helpers.sql_db.select_entry(helpers.conn, ctx.author.id, ctx.guild.id)

        embed = discord.Embed(title="Balance", color=helpers.bot_color(ctx))
        embed.add_field(name=helpers.get_user(bal[0]), value="${:.2f}".format(bal[2]))

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

        helpers.sql_db.update_entry(helpers.conn, ctx.author.id, ctx.guild.id, float(args[0]))

        await ctx.send('Added balance of ' + str(args[0]) + ' to ' + str(helpers.disp_name(ctx.author)))


    @commands.command(name='pay', aliases=['p', 'send'])
    async def _pay(self, ctx, user: discord.User, amount: float):
        if user is None: return

        bal = helpers.sql_db.select_entry(helpers.conn, user.id, ctx.guild.id)
        if bal == 0:
            return
        else:
            await self._add_to_user(ctx.author.id, ctx.guild.id, -amount)
            await self._add_to_user(user.id, ctx.guild.id, amount)
            await ctx.send("Sent " + str(amount) + " to " + user.name)


    async def _add_to_user(self, user_id, guild_id, amount=0.0):
        helpers.sql_db.update_entry(helpers.conn, user_id, guild_id, float(amount))

    @commands.command(name='balancetop', aliases=['baltop', 'bt'])
    async def _balance_top(self, ctx, *args):
        print("Received command BALANCE TOP from", ctx.message.author)

        balances = helpers.sql_db.select_entry_sorted(helpers.conn, ctx.guild.id)

        embed = discord.Embed(title="Top 10 Balances", color=helpers.bot_color(ctx))

        for bal in balances[0:max(10, len(balances))]:
            if (len(args) > 0 and bal[2] >= float(args[0])) or len(args)==0:
                embed.add_field(name=helpers.get_user(bal[0]), value="${:.2f}".format(bal[2]), inline=False)

        await ctx.send(embed=embed)


    @commands.command(name='addrole', aliases=['ar', 'addRole'])
    async def _add_role(self, ctx, *args):
        if not helpers.check(ctx): return
        print("Received command ADD ROLE from", ctx.message.author)

        if (len(args)) < 1: return

        guild: discord.Guild = ctx.guild

        await guild.create_role(name=args[0], color=discord.Color(0x000000))


    @commands.command(name='moverole', aliases=['mover', 'mr'])
    async def _move_role(self, ctx, role: discord.Role, pos: int):
        if not helpers.check_user(ctx): return
        print("Received command MOVE ROLE from", ctx.message.author)
        try:
            await role.edit(position=pos)
            await ctx.send("Role moved.")
        except discord.Forbidden:
            await ctx.send("You do not have permission to do that")
        except discord.HTTPException:
            await ctx.send("Failed to move role")
        except discord.InvalidArgument:
            await ctx.send("Invalid argument")


    @commands.command(name='elevate', aliases=['e', 'ele'])
    async def _elevate(self, ctx, role: discord.Role):
        if not helpers.check_user(ctx): return
        print("Received command ELEVATE from", ctx.message.author)

        roles = ctx.guild.get_member(self.bot.user.id).roles
        top_role = roles[-1]
        top_role_id = top_role.position
        try:
            await role.edit(position=top_role_id-1)
            await ctx.send("Role elevated.")
        except discord.Forbidden:
            await ctx.send("You do not have permission to do that")
        except discord.HTTPException:
            await ctx.send("Failed to move role")
        except discord.InvalidArgument:
            await ctx.send("Invalid argument")


    @commands.command(name='clonerole', aliases=['cr', 'crole'])
    async def _clone_role(self, ctx, role: discord.Role, new_name: str):
        if not helpers.check_user(ctx): return
        print("Received command CLONE ROLE from", ctx.message.author)

        perms = discord.Permissions(permissions=0)
        colour = discord.Colour(role.colour.value)
        guild = ctx.guild

        try:
            await guild.create_role(name=new_name, colour=colour)
            await ctx.send("Role created.")
        except discord.Forbidden:
            await ctx.send("You do not have permission to do that")
        except discord.HTTPException:
            await ctx.send("Failed to move role")
        except discord.InvalidArgument:
            await ctx.send("Invalid argument")

    @commands.command(name='changecolour', aliases=['colour', 'col'])
    async def _change_colour(self, ctx, role: discord.Role, hex: str):
        if not helpers.check_channel(ctx): return
        if role.name != "Green": return

        print("Received command CHANGE COLOUR from", ctx.message.author)

        try:
            col = int(hex, 0)

            await self.bot.edit_role(guild=ctx.guild, role=role, colour=discord.Color(col))
            await ctx.send("Role colour changed.")
        except discord.Forbidden:
            await ctx.send("You do not have permission to do that")
        except discord.HTTPException:
            await ctx.send("Failed to move role")
        except discord.InvalidArgument:
            await ctx.send("Invalid argument")
        finally:
            print("Command failed")


def setup(bot):
    bot.add_cog(TestingCog(bot))