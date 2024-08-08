import discord
import os
from dotenv import load_dotenv
import discord.ext.commands as commands
import Cogs.settings as settings

bot = commands.Bot(command_prefix='$$')


bot.load_extension('Cogs.settings')

load_dotenv()
bot.login(os.getenv('TOKEN'))