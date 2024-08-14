import discord
import os
from dotenv import load_dotenv
import discord.ext.commands as commands
import logging

from pyexpat.errors import messages

from Utils import database

from Cogs import settings, voicelogs, chatlogs

intents = discord.Intents(messages=True, guilds=True, members=True, message_content=True, voice_states=True)
logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='$$', intents=intents)


bot.add_cog(settings.MyCog(bot))
bot.add_cog(voicelogs.VoiceLogs(bot))
bot.add_cog(chatlogs.Chatlogs(bot))

@bot.event
async def on_ready():
    print("Bot running, guilds: ", len(bot.guilds))
    database.check_for_changes()

load_dotenv()
bot.run(os.getenv('TOKEN'))



