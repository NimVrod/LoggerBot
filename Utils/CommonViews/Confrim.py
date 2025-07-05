import discord
import builtins
from typing import Callable

class ConfirmView(discord.ui.View):
    def __init__(self, author: discord.User, confirm_action: Callable[[], None], cancel_action: Callable[[], None]):
        super().__init__()
        self.author = author
        self.confirm_action = confirm_action
        self.cancel_action = cancel_action

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("You clicked yes", ephemeral=True)
        await self.confirm_action()
        self.stop()
        return True

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("You clicked no", ephemeral=True)
        await self.cancel_action()
        self.stop()
        return False