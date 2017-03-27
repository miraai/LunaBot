import discord
from discord.ext import commands
from cogs.utils import config
from cogs.utils import checks


class CustomReactions:
    """Custom reactions"""

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('customs.json', loop=bot.loop)

    @commands.command(aliases=['acr'], pass_context=True, no_pm=True)
    @checks.is_owner()
    async def addcustom(self, ctx, command : str, text: str):
        """Adds custom reaction."""
        command = command.lower()
        custom = self.config.get(command, "")
        if custom != "":
            await self.bot.say('**Error**. Luna already has that command.')
            return
        else:
            await self.config.put(command, text)
            await self.bot.say("Custom reaction successfully added.")

    @commands.command(pass_context=True, no_pm=True)
    async def reaction(self, ctx, command: str):
        """Shows custom reaction.
        It doesnt have to be used, since it can be triggered by the message.
        """
        command = command.lower()
        text = self.config.get(command, "")
        if text != "":
            await self.bot.say(text)
        else:
            await self.bot.say("That reaction does not exist.")

    @commands.command(aliases=['allr'], pass_context=True, no_pm=True)
    async def reactions(self, ctx):
        """Shows all custom reactions."""
        commands = self.config.all()
        out = '```xl\n'
        for c in enumerate(commands):
            out+= str(c[0]+1) +'. ' + str(c[1]) + ': \"' + str(commands[c[1]]) + '\"\n'
        out += "```"
        await self.bot.say(out)

    #creates a trigger for a custom reaction
    async def on_message(self, message):
        if message.author.bot:
            return
        text = self.config.get(message.content, "")
        if text == "":
            return
        await self.bot.send_message(message.channel, text)

    @commands.command(aliases=['dcr'], pass_context=True, no_pm=True)
    @checks.is_owner()
    async def delcustom(self, cfx, command: str):
        """Deletes a custom reaction."""
        command = command.lower()
        text = self.config.get(command, "")
        if text == "":
            await self.bot.say("That reaction does not exist")
        else:
            await self.config.remove(command)
            await self.bot.say("Custom reaction deleted.")


def setup(bot):
    bot.add_cog(CustomReactions(bot))
