import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
from os.path import join, dirname

client = discord.Client()
bot = commands.Bot(command_prefix='!')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Bot Token
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

initial_cogs = ['cogs.owner', 'cogs.testing', 'cogs.channels', 'cogs.roles']

if __name__ == '__main__':
    for extension in initial_cogs:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Streaming(name="money out of your bank", url='www.bankwest.com'))
    print(f'Successfully logged in and booted...!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN, bot=True)
