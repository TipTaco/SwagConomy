import sql_db
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
from os.path import join, dirname

client = discord.Client()
bot = commands.Bot(command_prefix='!')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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

categories = ['Colours', 'Supporters', 'Ranks', 'Education', 'Bots', 'Achievements', 'Games', 'Interests', 'Curses']


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


def format_category(category):
    return "__" + str(category) + "__"


def get_roles_by_category(all_roles, category):
    if not category.startswith("__"):
        category = format_category(category)
