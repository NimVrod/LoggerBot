import discord
from discord.ext import commands
from Utils import log, database

class JoinLogs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            if database.read_database(guild.id)["JoinLogs"] == 0:
                continue
            else:
                self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guildsettings = database.read_database(member.guild.id)
        if guildsettings["JoinLogs"] == 0:
            return

        em = discord.Embed(title="Member Joined", description=f"{member.mention} joined the server", color=discord.Color.green(), thumbnail=member.avatar.url)

        #Calcualte invite code]
        invites = await member.guild.invites()
        for invite in invites:
            for invite2 in self.invites[member.guild.id]:
                if invite.code == invite2.code and invite.uses > invite2.uses:
                    em.add_field(name="Invite", value=f"Invited by {invite.inviter.mention} with code {invite.code}")
                    break
        await log.send_log(em, member.guild.get_channel(guildsettings["JoinLogs"]))