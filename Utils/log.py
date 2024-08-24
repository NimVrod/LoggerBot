import typing
import discord
import datetime


    
async def send_log(embed: discord.Embed, channel:discord.TextChannel) -> None:
    embed.set_footer(text=f"LoggerBot | Developed by: nimvrod | If you're enjoying LoggerBot, please consider leaving a review on Top.gg! https://top.gg/bot/1271203231888052354#reviews")
    embed.timestamp = datetime.datetime.now()
    embed.url = "https://discord.gg/sJuQPRkDkq"
    await channel.send(f"<t:{round(datetime.datetime.now().timestamp())}:T> or <t:{round(datetime.datetime.now().timestamp())}:R>",embed=embed)
    
    