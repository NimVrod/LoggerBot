import typing
import discord
import datetime
from Utils import database as db


async def send_log(embed: discord.Embed, channel: discord.TextChannel) -> None:
    if not channel:
        return
        
    embed.set_footer(text=f"LoggerBot | Developed by: nimvrod | If you're enjoying LoggerBot, please consider leaving a review on Top.gg! https://top.gg/bot/1271203231888052354#reviews")
    embed.timestamp = datetime.datetime.now()
    embed.url = "https://discord.gg/sJuQPRkDkq"
    
    try:
        await channel.send(f"<t:{round(datetime.datetime.now().timestamp())}:T> or <t:{round(datetime.datetime.now().timestamp())}:R>", embed=embed)
        guild = channel.guild
        guild_db = db.read_database(guild.id)
        guild_db["LastLog"] = (datetime.datetime.now().timestamp())
        db.write_database(guild.id, guild_db)
    except Exception as e:
        print(f"Error sending log to channel {channel.id}: {e}")

    
    