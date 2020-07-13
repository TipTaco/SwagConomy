import discord
from discord.ext import commands
from discord.ext.commands import Bot

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


@bot.command(name='balance', aliases=['bal', 'b'])
async def _balance(ctx, *args):
    if not check(ctx): return
    print("Received command BALANCE from", ctx.message.author)
    await ctx.send('Balance of ' + str(disp_name(ctx.author)) + ' is 0')


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


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
