import discord
from discord.ext import commands
from discord.commands import Option

class SettingsView(discord.ui.View):
    @discord.ui.button(label="VoiceLogs", style=discord.ButtonStyle.primary, emoji="🔒")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("VoiceLogs are enabled", ephemeral=True)
        self.children[0].emoji = "🔓"
        await interaction.message.edit(view=self)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="settings", description="Change the settings of the bot")
    async def settings(self, ctx: commands.Context):
        em = discord.Embed(title="Settings", description="Change the settings of the bot", color=discord.Color.green())
        em.add_field(name="VoiceLogs", value="See who,when and which voice channel did they join", inline=False)

        await ctx.respond(embed=em, view=SettingsView())

async def setup(bot):
    await bot.add_cog(MyCog(bot))