import discord
from discord import app_commands
from discord.ext import commands
from Utils import database
from Utils.CommonViews.Confrim import ConfirmView

class SettingsView(discord.ui.View):

    def __init__(self, guild_id: int, bot: commands.Bot):
        super().__init__()
        self.guildSettings = database.read_database(guild_id)
        self.bot = bot
        self.check_colors()

    def check_colors(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if self.guildSettings.get(child.label) == 0:
                    child.style = discord.ButtonStyle.red
                    child.emoji = "🔒"
                else:
                    child.style = discord.ButtonStyle.green
                    child.emoji = "📝"

        #await self.message.edit(view=self)

    async def response(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("You need to have manage server permissions to do this", ephemeral=True)
            return

        for key in self.guildSettings:
            if key == "LastLog":
                continue

            if key == button.label:
                if self.guildSettings[key] == 0:
                    try:
                        channel = await interaction.guild.create_text_channel(name=button.label, reason=f"Set by {interaction.user.name}", overwrites={interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)})
                    except discord.Forbidden:
                        await interaction.response.send_message("I don't have the permission to create a channel", ephemeral=True)
                        return
                    self.guildSettings[key] = channel.id
                    button.style = discord.ButtonStyle.green
                    button.emoji = "📝"
                    await interaction.response.send_message(f"Subscribed to {button.label}, The channel was created for you at {channel.mention}", ephemeral=True)
                else:
                    self.guildSettings[key] = 0
                    button.style = discord.ButtonStyle.red
                    button.emoji = "🔒"
                    await interaction.response.send_message(f"Unsubscribing from {button.label}, You may delete the channel, if this was a mistake resubscribe using the /set command", ephemeral=True)

        await interaction.message.edit(view=self)
        database.write_database(interaction.guild.id, self.guildSettings)




    @discord.ui.button(label="VoiceLogs", style=discord.ButtonStyle.green, emoji="📝")
    async def voicelogs_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.response(interaction, button)

    @discord.ui.button(label="ChatLogs", style=discord.ButtonStyle.green, emoji="📝")
    async def chatlogs_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.response(interaction, button)

    @discord.ui.button(label="AttachmentLogs", style=discord.ButtonStyle.green, emoji="📝")
    async def attachmentlogs_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.response(interaction, button)

    @discord.ui.button(label="JoinLogs", style=discord.ButtonStyle.green, emoji="📝")
    async def joinlogs_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button.style == discord.ButtonStyle.red:
            cog = self.bot.get_cog("JoinLogs")
            await cog.set_invites(interaction.guild)
        await self.response(interaction, button)

    @discord.ui.button(label="AuditLogs", style=discord.ButtonStyle.green, emoji="📝")
    async def auditlogs_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.response(interaction, button)


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot


    @app_commands.command(name="settings", description="Change the settings of the bot")
    async def settings(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        if not database.check_if_guild_in_db(interaction.guild.id):
            database.create_database(interaction.guild.id)

        guildSettings = database.read_database(interaction.guild.id)
        guild: discord.Guild = interaction.guild
        for key in guildSettings:
            try:
                channel = await guild.fetch_channel(guildSettings[key])
            except discord.NotFound:
                guildSettings[key] = 0
                continue

        em = discord.Embed(title="Settings", description="Change the settings of the bot", color=discord.Color.green())
        em.add_field(name="VoiceLogs", value="See who,when and which voice channel did they join", inline=True)
        em.add_field(name="ChatLogs", value="See who deleted, edited or bulk deleted messages", inline=True)
        em.add_field(name="AttachmentLogs", value="See who uploaded attachments", inline=True)
        em.add_field(name="JoinLogs", value="See who joined and who invited them", inline=True)
        em.add_field(name="AuditLogs", value="See who did what in the server", inline=True)

        view = SettingsView(interaction.guild.id, self.bot)
        await interaction.response.send_message(embed=em, view=view)

    @app_commands.command(name="set", description="Set the guildsettings")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.describe(option="The setting you want to change", channel="The channel you want to set")
    @app_commands.choices(option=[app_commands.Choice(name=x, value=x) for x in database.first_time.keys() if x != "LastLog"])
    async def set(self, interaction: discord.Interaction, option: app_commands.Choice[str], channel: discord.TextChannel):
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        if not database.check_if_guild_in_db(interaction.guild.id):
            database.create_database(interaction.guild.id)

        guildSettings = database.read_database(interaction.guild.id)
        guildSettings[option.value] = channel.id
        database.write_database(interaction.guild.id, guildSettings)
        await interaction.response.send_message(f"Set the {option.value} to {channel.mention}")

    @set.error
    async def set_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You need Manage Server permission to use this command.", ephemeral=True)
            return
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not database.check_if_guild_in_db(member.guild.id):
            database.create_database(member.guild.id)
        guildSettings = database.read_database(member.guild.id)
        em = discord.Embed(title=f"Welecome to {member.guild.name}", description="Currently active logs:\n", color=discord.Color.green())
        for key in guildSettings:
            if guildSettings[key] != 0:
                em.description += f"✅ {key} active\n"
            else:
                em.description += f"❌ {key} inactive\n"
        em.set_footer(text="Find out more using /settings")
        # await member.send(embed=em) # Uncomment this line to send the embed to the member who joined




async def setup(bot):
    await bot.add_cog(MyCog(bot))
