from enum import member

import discord
import discord.ext.commands as commands
from Utils import log, database
from builtins import list
import os

class Chatlogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def attachmets_to_url_string(self, attachments: list[discord.Attachment]) -> str:
        return "\n".join([attachment.url for attachment in attachments])

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        print("Message Deleted")
        guildsettings = database.read_database(message.guild.id)

        if guildsettings["ChatLogs"] == 0 or message.author.bot:
            return

        em = discord.Embed(title="Message Deleted", description=f"{message.author.mention} deleted in {message.channel.mention}", color=discord.Color.red(), thumbnail=message.author.avatar.url)
        em.add_field(name="Content", value=message.content, inline=False)
        em.add_field(name="Attachments", value=self.attachmets_to_url_string(message.attachments), inline=False)
        await log.send_log(em, message.guild.get_channel(guildsettings["ChatLogs"]))

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list[discord.Message]):
        guildsettings = database.read_database(messages[0].guild.id)

        if guildsettings["ChatLogs"] == 0:
            return

        em = discord.Embed(title="Bulk Message Deleted", description=f"{len(messages)} messages were deleted in {messages[0].channel.mention}", color=discord.Color.red())
        with open(f"Temp/bulk{messages[0].guild.id}.txt", "w") as f:
            for message in messages:
                f.write(f"{message.author.name} : {message.content}\n\n")
        await guildsettings["ChatLogs"].send(file=discord.File(f"Temp/bulk{messages[0].guild.id}.txt"))
        #Delete the temp file
        os.remove(f"Temp/bulk{messages[0].guild.id}.txt")
        await log.send_log(em, messages[0].guild.get_channel(guildsettings["ChatLogs"]))

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        guildsettings = database.read_database(before.guild.id)

        if guildsettings["ChatLogs"] == 0 or before.author.bot:
            return

        em = discord.Embed(title="Message Edited", description=f"{before.author.mention} edited in {before.channel.mention}", color=discord.Color.yellow(), thumbnail=before.author.avatar.url)
        em.add_field(name="Before", value=before.content, inline=False)
        em.add_field("Before Attachments", value=self.attachmets_to_url_string(before.attachments), inline=False)
        em.add_field(name="After", value=after.content, inline=False)
        em.add_field(name="After Attachments", value=self.attachmets_to_url_string(after.attachments), inline=False)
        await log.send_log(em, before.guild.get_channel(guildsettings["ChatLogs"]))

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        guildsettings = database.read_database(message.guild.id)

        if guildsettings["AttachmentLogs"] == 0 or message.author.bot:
            return

        if message.attachments:
            em = discord.Embed(title="Attachment Log",
                               description=f"{message.author.mention} attachments in {message.channel.mention}",
                               color=discord.Color.green(), thumbnail=message.author.avatar.url)
            await log.send_log(em, message.guild.get_channel(guildsettings["AttachmentLogs"]))
            channel = message.guild.get_channel(guildsettings["AttachmentLogs"])
            await channel.send(files=[await x.to_file() for x in message.attachments])

