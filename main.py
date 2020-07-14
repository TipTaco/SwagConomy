import discord
from discord.ext import commands

import sql_db

import os
from dotenv import load_dotenv
from os.path import join, dirname

client = discord.Client()
bot = commands.Bot(command_prefix='!')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Bot Token
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

# User IDs
USER_TIPTACO = os.environ.get("TIPTACO")
# Channel IDs
CHANNEL_BOT_GUNK = os.environ.get("BOT_GUNK")
CHANNEL_TESTING_GENERAL = os.environ.get("TESTING_GENERAL")

# Channels to respond to economy commands in
trusted_channels = [CHANNEL_BOT_GUNK, CHANNEL_TESTING_GENERAL]
# The trusted people who can use the commands
trusted_users = [USER_TIPTACO]
# The user to DM (if needed)
the_true_boy = USER_TIPTACO

database = "sql_currency.db"
conn = sql_db.create_conn(database)


def check_channel(ctx):
    return any(ctx.message.channel.id == int(x) for x in trusted_channels)


def check_user(ctx):
    return any(ctx.author.id == int(x) for x in trusted_users) and ctx.author.id != bot.user.id


def check(ctx):
    return check_channel(ctx) and check_user(ctx)


def disp_name(user):
    if user is None:
        return ""

    if isinstance(user, discord.Member):
        if user.nick is not None:
            return str(user.nick)
        else:
            return str(user.name)
    elif isinstance(user, discord.User):
        return str(user.name)


def get_user(user_id):
    return bot.get_user(user_id)


def bot_color(ctx):
    return discord.Color(ctx.guild.get_member(bot.user.id).color.value)


@bot.command(name='initialise', aliases=['init'])
async def _init(ctx, user: discord.User):
    if not check_channel(ctx): return

    user_id = ctx.author.id
    if user is not None:
        user_id = user.id

    sql_db.safe_add_entry(conn, user_id, ctx.guild.id)

    print("Received command INITIALISE from", ctx.message.author)
    await ctx.send('Initialised ' + str(disp_name(ctx.guild.get_member(user_id))))


@bot.command(name='balance', aliases=['bal', 'b'])
async def _balance(ctx, *args):
    if not check_channel(ctx): return
    print("Received command BALANCE from", ctx.message.author)

    bal = sql_db.select_entry(conn, ctx.author.id, ctx.guild.id)

    embed = discord.Embed(title="Balance", color=bot_color(ctx))
    embed.add_field(name=get_user(bal[0]), value="${:.2f}".format(bal[2]))

    if bal != 0:
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to get bal")

@bot.command(name='add', aliases=['a'])
#@commands.has_role('King')
async def _add(ctx, *args):
    if not check(ctx): return
    if len(args) <= 0: return
    print("Received command ADD from", ctx.message.author)

    sql_db.update_entry(conn, ctx.author.id, ctx.guild.id, float(args[0]))

    await ctx.send('Added balance of ' + str(args[0]) + ' to ' + str(disp_name(ctx.author)))


@bot.command(name='pay', aliases=['p', 'send'])
async def _pay(ctx, user: discord.User, amount: float):
    if user is None: return

    bal = sql_db.select_entry(conn, user.id, ctx.guild.id)
    if bal == 0:
        return
    else:
        await _add_to_user(ctx.author.id, ctx.guild.id, -amount)
        await _add_to_user(user.id, ctx.guild.id, amount)
        await ctx.send("Sent " + str(amount) + " to " + user.name)


async def _add_to_user(user_id, guild_id, amount=0.0):
    sql_db.update_entry(conn, user_id, guild_id, float(amount))

@bot.command(name='balancetop', aliases=['baltop', 'bt'])
async def _balance_top(ctx, *args):
    print("Received command BALANCE TOP from", ctx.message.author)

    balances = sql_db.select_entry_sorted(conn, ctx.guild.id)

    embed = discord.Embed(title="Top 10 Balances", color=bot_color(ctx))

    for bal in balances[0:max(10, len(balances))]:
        if (len(args) > 0 and bal[2] >= float(args[0])) or len(args)==0:
            embed.add_field(name=get_user(bal[0]), value="${:.2f}".format(bal[2]), inline=False)

    await ctx.send(embed=embed)


@bot.command(name='addrole', aliases=['ar', 'addRole'])
async def _add_role(ctx, *args):
    if not check(ctx): return
    print("Received command ADD ROLE from", ctx.message.author)

    if (len(args)) < 1: return

    guild: discord.Guild = ctx.guild

    await guild.create_role(name=args[0], color=discord.Color(0x000000))


@bot.command()
async def moverole(ctx, role: discord.Role, pos: int):
    if not check(ctx): return
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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
