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

        channel = entry.guild.get_channel(guildSettings["AuditLogs"])
        if not channel:
            return
            
        user_mention = entry.user.mention if entry.user else "Unknown User"
        thumbnail_url = entry.user.display_avatar.url if entry.user else None
        
        em = discord.Embed(title="Audit log entry", description=f"Action: {entry.action}\nBy: {user_mention}\nReason: {entry.reason}\nTarget: {entry.target}", color=discord.Color.blurple(), thumbnail=thumbnail_url)
        await log.send_log(em, channel)