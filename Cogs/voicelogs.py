import discord
import discord.ext.commands as commands
import datetime
from Utils import database, log

def time_delta_to_string(delta: datetime.timedelta) -> str:
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

class VoiceLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.joins = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
        if database.read_database(member.guild.id)["VoiceLogs"] == 0:
            return

        if before.channel is None and after.channel is not None:
            #First join voice channel
            em = discord.Embed(title=f"Voice join", description=f"<@{member.id}> joined {after.channel.mention}", color=discord.Color.green(), thumbnail=member.display_avatar.url)
            self.joins[member.id] = datetime.datetime.now()
            channel = member.guild.get_channel(database.read_database(member.guild.id)["VoiceLogs"])
            if channel:
                await log.send_log(em, channel)
        elif before.channel is not None and after.channel is None:
            #Left voice channel
            em = discord.Embed(title="Voice Left", description=f"{member.mention} left {before.channel.mention}", color=discord.Color.red(), thumbnail=member.display_avatar.url)
            if member.id in self.joins:
                time_spent: datetime.timedelta = datetime.datetime.now() - self.joins[member.id]
                em.add_field(name="Time spent", value=f"Spent time in voice: {time_delta_to_string(time_spent)}", inline=False)
            channel = member.guild.get_channel(database.read_database(member.guild.id)["VoiceLogs"])
            if channel:
                await log.send_log(em, channel)
        elif before.channel != after.channel:
            #TODO: Add a check if user was moved or switched by themselves
            async for entry in member.guild.audit_logs(limit=1):
                if entry.action == discord.AuditLogAction.member_move:
                    em = discord.Embed(title="Voice Moved", description=f"<@{member.id}> was moved from {before.channel.mention} to {after.channel.mention} by {entry.user.mention}", color=discord.Color.blue(), thumbnail=member.display_avatar.url)
                    channel = member.guild.get_channel(database.read_database(member.guild.id)["VoiceLogs"])
                    if channel:
                        await log.send_log(em, channel)
                    return

            em = discord.Embed(title="Voice Switch", description=f"<@{member.id}> switched from {before.channel.mention} to {after.channel.mention}", color=discord.Color.yellow(), thumbnail=member.display_avatar.url)
            channel = member.guild.get_channel(database.read_database(member.guild.id)["VoiceLogs"])
            if channel:
                await log.send_log(em, channel)


def setup(bot):
    bot.add_cog(VoiceLogs(bot))