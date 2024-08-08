import discord
import os
import discord.ext.commands as commands
import Cogs.settings as settings

bot = commands.Bot(command_prefix='$$')


bot.load_extension('Cogs.settings')

bot.login(os.getenv('TOKEN'))   