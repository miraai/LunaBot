import aiohttp
from discord.ext import commands
from .utils import checks
import discord
import inspect
import asyncio


# to expose to the eval command
import datetime
from collections import Counter

class Admin:
    """Admin-only commands that make the bot dynamic-y."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, *, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\nModule could not be loaded.')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\nModule has been loaded.')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, *, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('\nModule could not be unloaded.')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\nModule has been unloaded.')

    @commands.command(name='reload', hidden=True)
    @checks.is_owner()
    async def _reload(self, *, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\nModule could not be reloaded.')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\nModule has been reloaded.')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def debug(self, ctx, *, code : str):
        """Evaluates code."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await self.bot.say(python.format(result))

    # so i desperately tried to change the game, and it kinda works, but it doesnt really, and im confused okay
    @commands.command(pass_context=True)
    async def game(self, ctx, *game):
        if ctx.message.channel.permissions_for(ctx.message.author).administrator:
            gameName = ' '.join(game)
            await self.bot.change_status(game=discord.Game(name=gameName))
            await self.bot.say('**Ok.** I changed the game to **{0}**'.format(gameName))
        else:
            await self.bot.say('**No.**! Admin only command')


    #this should change bot's avatar, like, who knows what it does really
    @commands.command(pass_context=True)
    @checks.is_owner()
    async def avatar(self, ctx, url: str):
        '''Sets new avatar for Luna'''
        #async with aiohttp.get(''.join(url)) as img:
        #   with open('tempAva.png', 'wb') as f:
        #       f.write(await img.read())
        #with open('tempAva.png', 'rb') as f:
        #                 await self.bot.edit_profile(avatar=f.read())
        #asyncio.sleep(2)
        #await self.bot.say('**Ok!** New avatar set!')
        async with aiohttp.get(''.join(url)) as img:
            await self.bot.edit_profile(avatar = await img.read())
        await self.bot.say('**Ok!** New avatar set!')

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def name(self, ctx, *name):
        '''Changes Bot Name'''
        if ctx.message.channel.permissions_for(ctx.message.author).administrator:
            name = ' '.join(name)
            await self.bot.edit_profile(username=name)
            msg = '**Ok!** New name set: **{0}**'.format(name)
        else:
            msg = '**No!** Owner Only command!'

        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def topic(self, ctx, topic: str):
        """Sets a channel topic."""
        try:
            await self.bot.edit_channel(ctx.message.channel, topic=topic)
        except discord.Forbidden:
            await self.bot.say('**Error!** Bot Owner command.')
        else:
            await self.bot.say('**Done!** Topic set for this channel.')

    @commands.command(aliases=['cc'], pass_context=True)
    @checks.is_owner()
    async def createchannel(self, ctx, name: str):
        """Creates a new channel"""
        try:
            await self.bot.create_channel(ctx.message.server, type=discord.ChannelType.text, name=name)
        except discord.Forbidden:
            await self.bot.say('**Error!** You don\' have a permission to do that.')
        else:
            await self.bot.say('**Done!** Channel created!')

    @commands.command(aliases=['dc'], pass_context=True)
    @checks.is_owner()
    async def deletechannel(self, ctx, channel : discord.Channel):
        """Deletes a channel"""
        try:
            await self.bot.delete_channel(channel)
        except discord.Forbidden:
            await self.bot.say('**Error!** You don\' have a permission to do that.')
        else:
            await self.bot.say('**Done!** Channel deleted!')

    @commands.command(aliases=['ec'], pass_context=True)
    @checks.is_owner()
    async def editchannel(self, ctx, channel : discord.Channel, name: str):
        """Edit channel's name"""
        try:
            await self.bot.edit_channel(channel, name=name)
        except discord.Forbidden:
            await self.bot.say('**Error!** You don\' have a permission to do that.')
        else:
            await self.bot.say('**Done!** Channel name changed!')

    @commands.command(aliases=['cvc'], pass_context=True)
    @checks.is_owner()
    async def createvchannel(self, ctx, name: str):
        """Creates a new voice channel"""
        try:
            await self.bot.create_channel(ctx.message.server, type=discord.ChannelType.voice, name=name)
        except discord.Forbidden:
            await self.bot.say('**Error!** You don\' have a permission to do that.')
        else:
            await self.bot.say('**Done!** Voice channel created!')

def setup(bot):
    bot.add_cog(Admin(bot))
