import discord
from discord.ext import commands
from Utils import log, database

class JoinLogs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.invites = {}

    async def set_invites(self, guild):
        self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            if database.read_database(guild.id)["JoinLogs"] == 0:
                continue
            else:
                self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        self.invites[invite.guild.id] = await invite.guild.invites()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guildsettings = database.read_database(member.guild.id)
        if guildsettings["JoinLogs"] == 0:
            return

        em = discord.Embed(title="Member Joined", description=f"{member.mention} joined the server", color=discord.Color.green(), thumbnail=member.display_avatar.url)

        #Calcualte invite code]
        invites = await member.guild.invites()
        for invite in invites:
            for invite2 in self.invites[member.guild.id]:
                if invite.code == invite2.code and invite.uses > invite2.uses:
                    em.add_field(name="Invite", value=f"Invited by {invite.inviter.mention} with code {invite.code}")
                    break
        self.invites[member.guild.id] = invites
        await log.send_log(em, member.guild.get_channel(guildsettings["JoinLogs"]))


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guildsettings = database.read_database(member.guild.id)
        if guildsettings["JoinLogs"] == 0:
            return


        #Calculate whether the member left or was kicked
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                em = discord.Embed(title="Member Kicked", description=f"{member.mention} was kicked from the server",
                                   color=discord.Color.red(), thumbnail=member.display_avatar.url)
                em.add_field(name="Kicked by", value=entry.user.mention)
                await log.send_log(em, member.guild.get_channel(guildsettings["JoinLogs"]))
                return

        #Calculate whether the member left or was banned
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == member.id:
                em = discord.Embed(title="Member Banned", description=f"{member.mention} was banned from the server",
                                   color=discord.Color.red(), thumbnail=member.display_avatar.url)
                em.add_field(name="Banned by", value=entry.user.mention)
                await log.send_log(em, member.guild.get_channel(guildsettings["JoinLogs"]))
                return


        #Member left
        em = discord.Embed(title="Member Left", description=f"{member.mention} left the server", color=discord.Color.red(), thumbnail=member.display_avatar.url)
        await log.send_log(em, member.guild.get_channel(guildsettings["JoinLogs"]))