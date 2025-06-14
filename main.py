import discord
import os
from dotenv import load_dotenv
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import logging
import logging.handlers
import asyncio

from pyexpat.errors import messages

from Utils import database

from Cogs import settings, voicelogs, chatlogs, joinlogs, auditlogs

intents = discord.Intents(messages=True, guilds=True, members=True, message_content=True, voice_states=True, moderation=True)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot = commands.Bot(command_prefix='$$', intents=intents)


bot.add_cog(settings.MyCog(bot))
bot.add_cog(voicelogs.VoiceLogs(bot))
bot.add_cog(chatlogs.Chatlogs(bot))
bot.add_cog(joinlogs.JoinLogs(bot))
bot.add_cog(auditlogs.AuditLogs(bot))

@tasks.loop(minutes=10)
async def presence_update():
    await bot.change_presence(activity=discord.Game(name="Guilds: " + str(len(bot.guilds))))

@bot.event
async def on_ready():
    print("Bot running, guilds: ", len(bot.guilds))
    await bot.change_presence(activity=discord.Game(name="Recently updated"))
    for guild in bot.guilds:
        if not database.check_if_guild_in_db(guild.id):
            database.create_database(guild.id)
    database.check_for_changes()
    await asyncio.sleep(600)
    presence_update.start()

@bot.slash_command(name="ping", description="Check the bot's latency")
async def ping(ctx):
    em = discord.Embed(title="Pong!", description=f"{round(bot.latency * 1000)}ms", color=discord.Color.green())
    await ctx.respond(embed=em)


@bot.slash_command(name="eval", description="Evaluate code")
@commands.is_owner()
async def evalCommand(ctx, code: str):
    try:
        result = eval(code)
        em = discord.Embed(title="Eval", description=result, color=discord.Color.green())
        await ctx.respond(embed=em)
    except Exception as e:
        em = discord.Embed(title="Error", description=e, color=discord.Color.red())
        await ctx.respond(embed=em)

load_dotenv()
bot.run(os.getenv('TOKEN'), log_handler=handler)



