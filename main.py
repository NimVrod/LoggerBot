import discord
import os
from dotenv import load_dotenv
import discord.ext.commands as commands
import logging
from Utils import database

from Cogs import settings, voicelogs

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='$$')


bot.add_cog(settings.MyCog(bot))
bot.add_cog(voicelogs.VoiceLogs(bot))

@bot.event
async def on_ready():
    print("Bot running, guilds: ", len(bot.guilds))
    database.check_for_changes()

load_dotenv()
bot.run(os.getenv('TOKEN'))



