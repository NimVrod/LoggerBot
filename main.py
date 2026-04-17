import asyncio
import logging
import os

import discord
import discord.ext.commands as commands
import discord.ext.tasks as tasks
from discord import app_commands
from dotenv import load_dotenv

from Utils import database

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
intents.voice_states = True

logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


class LoggerBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="$$", intents=intents)
        self.synced = False

    async def setup_hook(self) -> None:
        for extension in (
            "Cogs.settings",
            "Cogs.voicelogs",
            "Cogs.chatlogs",
            "Cogs.joinlogs",
            "Cogs.auditlogs",
        ):
            await self.load_extension(extension)


bot = LoggerBot()


@tasks.loop(minutes=10)
async def presence_update() -> None:
    await bot.change_presence(activity=discord.Game(name=f"Guilds: {len(bot.guilds)}"))


@bot.event
async def on_ready() -> None:
    print("Bot running, guilds: ", len(bot.guilds))
    await bot.change_presence(activity=discord.Game(name="Recently updated"))
    for guild in bot.guilds:
        if not database.check_if_guild_in_db(guild.id):
            database.create_database(guild.id)
    database.check_for_changes()

    if not bot.synced:
        await bot.tree.sync()
        bot.synced = True

    if not presence_update.is_running():
        await asyncio.sleep(600)
        presence_update.start()


@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction) -> None:
    em = discord.Embed(title="Pong!", description=f"{round(bot.latency * 1000)}ms", color=discord.Color.green())
    await interaction.response.send_message(embed=em)


async def owner_only(interaction: discord.Interaction) -> bool:
    return await bot.is_owner(interaction.user)


@bot.tree.command(name="eval", description="Evaluate code")
@app_commands.check(owner_only)
@app_commands.describe(code="Evaluate code")
async def eval_command(interaction: discord.Interaction, code: str) -> None:
    try:
        result = eval(code)
        em = discord.Embed(title="Eval", description=str(result), color=discord.Color.green())
        await interaction.response.send_message(embed=em)
    except Exception as e:
        em = discord.Embed(title="Error", description=str(e), color=discord.Color.red())
        await interaction.response.send_message(embed=em)


@eval_command.error
async def eval_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Only the bot owner can use this command.", ephemeral=True)
        return
    raise error


async def main() -> None:
    load_dotenv()
    token = os.getenv("TOKEN")
    if token is None:
        raise RuntimeError("Missing TOKEN environment variable.")
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())



