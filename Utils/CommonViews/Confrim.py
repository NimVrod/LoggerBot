import discord
import builtins
from typing import Awaitable, Callable

class ConfirmView(discord.ui.View):
    def __init__(self, author: discord.User, confirm_action: Callable[[], Awaitable[None]], cancel_action: Callable[[], Awaitable[None]]):
        super().__init__()
        self.author = author
        self.confirm_action = confirm_action
        self.cancel_action = cancel_action

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked yes", ephemeral=True)
        await self.confirm_action()
        self.stop()
        return True

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked no", ephemeral=True)
        await self.cancel_action()
        self.stop()
        return False
