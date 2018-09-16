from discord.ext import commands
from datetime import datetime
import discord
from .utils import checks
import random


class Buttons:
    """Buttons that make you feel."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def feelgood(self):
        """press"""
        await self.bot.say('*pressed*')

    @commands.command()
    async def feelbad(self):
        """depress"""
        await self.bot.say('*depressed*')

    @commands.command()
    async def love(self):
        """What is love?"""
        responses = [
            'https://www.youtube.com/watch?v=HEXWRTEbj1I',
            'https://www.youtube.com/watch?v=i0p1bmr0EmE',
            'an intense feeling of deep affection',
            'something we don\'t have'
        ]

        response = random.choice(responses)
        await self.bot.say(response)

    @commands.command()
    async def bored(self):
        """boredom looms"""
        await self.bot.say('http://i.imgur.com/Vv4QoGy.gif')

    @commands.command(hidden=True)
    async def codeworks(self):
        """code magic"""
        await self.bot.say('http://i.imgur.com/uz2GLai.gif')

    @commands.command()
    async def hello(self):
        """Displays my intro message."""
        await self.bot.say('Hello! I\'m a bot and I\'m a lunatic! Mirai#3133 made me.')

    # doesnt do anything, just for funzies
    @commands.command()
    async def night(self):
        """Good night message."""
        await self.bot.say('Good night! :crescent_moon:')

    @commands.command()
    async def morning(self):
        """Good night message."""
        await self.bot.say('Good morning! :sunny:')
        
    @commands.command()
    async def sad(self):
        """Sad panda"""
        await self.bot.say('Sad :panda:')

def setup(bot):
    bot.add_cog(Buttons(bot))
