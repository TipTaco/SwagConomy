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


@bot.command(name='initialise', aliases=['init'])
async def _init(ctx, *args):
    if not check_channel(ctx): return

    sql_db.safe_add_entry(conn, ctx.author.id, ctx.guild.id)

    print("Received command INITIALISE from", ctx.message.author)
    await ctx.send('Initialised ' + str(disp_name(ctx.author)))


@bot.command(name='balance', aliases=['bal', 'b'])
async def _balance(ctx, *args):
    if not check_channel(ctx): return
    print("Received command BALANCE from", ctx.message.author)

    bal = sql_db.select_entry(conn, ctx.author.id, ctx.guild.id)

    await ctx.send('Balance of ' + str(disp_name(ctx.author)) + ' is ' + str(bal))


@bot.command(name='add', aliases=['a'])
@commands.has_role('King')
async def _add(ctx, *args):
    if not check_channel(ctx): return
    if len(args) <= 0: return
    print("Received command ADD from", ctx.message.author)

    sql_db.update_entry(conn, ctx.author.id, ctx.guild.id, int(args[0]))

    await ctx.send('Added balance of ' + str(args[0]) + ' to ' + str(disp_name(ctx.author)))


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
