from discord.ext import commands
import discord
from cogs.utils import checks
import datetime, re
import json, asyncio
import copy
import logging
import traceback
import sys
from collections import Counter

#added this so i can have INFO logging level shown in the console
logging.basicConfig(level=logging.INFO)

description = """
Mirai made a lunatic! RUN!
"""
#HERE BE DRAGONS

initial_extensions = [
    'cogs.meta',
    'cogs.mod',
    'cogs.tags',
    'cogs.lounge',
    'cogs.repl',
    'cogs.carbonitex',
    'cogs.mentions',
    'cogs.api',
    'cogs.stars',
    'cogs.admin',
    'cogs.buttons',
    'cogs.customreactions',
]
#so these should be kinda modules/plugins

'''
This is me logging stuff in a file called luna.log
'''
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='luna.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True)

#prefix, can be either ? or !
prefix = ['?', '!', '\N{HEAVY EXCLAMATION MARK SYMBOL}']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None, help_attrs=help_attrs)

#still not clear with what these events are for, i assume its something like even handlers or whatever
#so basically, if the command which can not be used in DM is used there, bot sends the message that it cant be used
#if the command is disabled and someone tries to use it, bot shows the message that its disabled
#no idea whats the rest for
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

#event on_ready(), so, when the bot starts this is shown in the console, still trying to get author name and id to work
@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('Discord Version: ' + discord.__version__)
    print('Author: Mirai')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_resumed():
    print('resumed...')

#event that logs commands being used in the server. Still trying to get server ID in it, im stupid
#scratch that, i figured Server ID thingy
@bot.event
async def on_command(command, ctx):
    bot.commands_used[command.name] += 1
    message = ctx.message
    destination = None
    if message.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name}) [{0.server.id}]'.format(message)

    log.info('{0.timestamp}: {0.author.name} [{0.author.id}] in {1}: {0.content}'.format(message, destination))

#fuck me
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

#okay, owner only command, repeats a COMMAND specified number of times, takes number of times to repeat the command
#and command we want to repeat, command is !do
@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)

#im not sure why i need this
@bot.command()
async def changelog():
    """Gives a URL to the current bot changelog."""
    await bot.say('https://discord.gg/y2PcWMM')

#loads bot credentials.json as file. Takes client_id, carbon_key and bots_key=client_id now (i will fix it)
#if id is missing, it wont load the file
def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    if any('debug' in arg.lower() for arg in sys.argv):
        bot.command_prefix = '$'

    credentials = load_credentials()
    bot.client_id = credentials['client_id']
    bot.commands_used = Counter()
    bot.carbon_key = credentials['carbon_key']
    bot.bots_key = credentials['bots_key']
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    #bot runs the token from the credentials and it starts
    bot.run(credentials['token'])
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
