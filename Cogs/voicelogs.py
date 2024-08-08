import discord
import discord.ext.commands as commands
from ..Utils.log import Log
import datetime

class VoiceLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = Log("VOICE")
        self.joins = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
        if before.channel is None and after.channel is not None:
            #First join voice channel
            em = discord.Embed(title=f"{member.name} joined {after.channel.name}", color=discord.Color.green())
            self.joins[member.id] = datetime.time()
            self.log.send_log(em)
            pass
        elif before.channel is not None and after.channel is None:
            #Left voice channel
            em = discord.Embed(title=f"{member.name} left {before.channel.name}", color=discord.Color.red())
            if member.id in self.joins:
                time_spent: datetime.time = datetime.time() - self.joins[member.id]    
                em.add_field(name="Time spent", value=f"{time_spent.strftime("%h h %m m %s s")}", inline=False)
            pass
        elif before.channel != after.channel:
            #Move to another voice channel
            pass


def setup(bot):
    bot.add_cog(VoiceLogs(bot))