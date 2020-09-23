from discord.ext import commands
import discord
import helpers

class RolesCog(commands.Cog, name='Roles'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='giverole', aliases=['gr', 'giveRole'])
    async def _give_role(self, ctx, role):
        if not str(ctx.message.author.id) == str(helpers.USER_TIPTACO): return
        print("Received command GIVE ROLE from", ctx.message.author)

        user = ctx.message.author

        await user.add_roles(discord.utils.get(user.guild.roles, name=role))

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
            await role.edit(position=top_role_id - 1)
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
    bot.add_cog(RolesCog(bot))

