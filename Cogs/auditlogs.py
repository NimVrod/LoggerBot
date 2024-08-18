import discord
from discord.ext import commands
from Utils import log, database

class AuditLogs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_audit_log_entry(self, entry:discord.AuditLogEntry):
        guildSettings = database.read_database(entry.guild.id)
        if guildSettings["AuditLogs"] == 0:
            return

        em = discord.Embed(title="Audit log entry", description=f"Action: {entry.action}\nBy: {entry.user.mention}\nReason: {entry.reason}\nTarget: {entry.target}", color=discord.Color.blurple(), thumbnail=entry.user.display_avatar.url)
        await log.send_log(em, entry.guild.get_channel(guildSettings["AuditLogs"]))