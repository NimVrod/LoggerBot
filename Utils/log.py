import typing
import discord
import time

class Log:
    def __init__(self, type) -> None:
        self.type = type
        self.embed: discord.Embed = discord.Embed()

    def check_if_guild_in_db(self, guild_id: int) -> bool:
        return True
    
    async def send_log(self, embed: discord.Embed) -> None:
        channel : discord.TextChannel = None
        embed.set_footer(text=f"LoggerBot | Developed by: nimvrod | <t:{time.time()}:f>")
        await channel.send(embed=embed)
    
    