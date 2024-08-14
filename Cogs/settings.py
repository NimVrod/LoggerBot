import discord
from discord.ext import commands
from discord.commands import Option
from Utils import database
from Utils.CommonViews.Confrim import ConfrimView

class SettingsView(discord.ui.View):

    def __init__(self, guild_id: int):
        super().__init__()
        self.guildSettings = database.read_database(guild_id)

    async def check_colors(self):
        for child in self.children:
            if child.type == discord.ui.Button:
                child : discord.ui.Button
                if self.guildSettings[child.label] == 0:
                    child.style = discord.ButtonStyle.red

        await self.message.edit(view=self)

    async def response(self, button : discord.ui.Button, interaction: discord.Interaction,):
        for key in self.guildSettings:
            if key == button.label:
                if self.guildSettings[key] == 0:
                    try:
                        channel = await interaction.guild.create_text_channel(name="VoiceLogs", reason=f"Set by {interaction.user.name}")
                    except discord.Forbidden:
                        await interaction.response.send_message("I don't have the permission to create a channel", ephemeral=True)
                        return
                    self.guildSettings[key] = channel.id
                    button.style = discord.ButtonStyle.green
                    await interaction.response.send_message(f"Subscribed to these logs, The channel was created for you at <#{channel.id}>", ephemeral=True)
                else:
                    self.guildSettings[key] = 0
                    button.style = discord.ButtonStyle.red
                    await interaction.response.send_message("Unsubscribing from these logs, You may delete the channel, if this was a mistake resubscribe yousing the /set command", ephemeral=True)

        await interaction.message.edit(view=self)
        database.write_database(interaction.guild.id, self.guildSettings)




    @discord.ui.button(label="VoiceLogs", style=discord.ButtonStyle.green, emoji="🔒")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.response(button, interaction,)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="settings", description="Change the settings of the bot")
    async def settings(self, ctx):
        if not database.check_if_guild_in_db(ctx.guild.id):
            database.create_database(ctx.guild.id)

        em = discord.Embed(title="Settings", description="Change the settings of the bot", color=discord.Color.green())
        em.add_field(name="VoiceLogs", value="See who,when and which voice channel did they join", inline=False)

        await ctx.respond(embed=em, view=SettingsView(ctx.guild.id))

async def setup(bot):
    await bot.add_cog(MyCog(bot))