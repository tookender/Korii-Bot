import random

import discord
from discord import app_commands

from utils import Interaction, Cog


class ActionsCog(Cog):
    def __init__(self):
        self.prank_messages = []
        self.lucky_messages = []
        self.unlucky_messages = []

    def fill(self, name: str, variable: list):
        file = open(name, encoding="utf-8")
        for line in file.readlines():
            if not line.startswith("##"):
                variable.append(line.replace("\n", ""))

    async def cog_load(self):
        self.fill("data/messages/prank_messages.txt", self.prank_messages)
        self.fill("data/messages/lucky_messages.txt", self.lucky_messages)
        # self.fill("bot/assets/unlucky_messages.txt", self.unlucky_messages)

    @app_commands.command(description="Do a funny lil' prank on someone to show how grateful you are!")
    @app_commands.describe(user="The user you want to prank.")
    @app_commands.guild_only()
    async def prank(self, interaction: Interaction, user: discord.Member):
        if not interaction.guild:
            return

        if interaction.user == user:
            user = random.choice(interaction.guild.members)

        prank_message = random.choice(self.prank_messages)
        prank_message = prank_message.replace("<user>", user.mention)
        prank_message = prank_message.replace("<author>", interaction.user.mention)

        return await interaction.response.send_message(prank_message)

    @app_commands.command(description="Wish life and prosperity upon anyone you want!")
    @app_commands.describe(user="Who shall receive your kind treatment?")
    @app_commands.guild_only()
    async def lucky(self, interaction: Interaction, user: discord.Member):
        if not interaction.guild:
            return

        if interaction.user == user:
            user = random.choice(interaction.guild.members)

        lucky_message = random.choice(self.lucky_messages)
        lucky_message = lucky_message.replace("<user>", user.mention)
        lucky_message = lucky_message.replace("<author>", interaction.user.mention)

        return await interaction.response.send_message(lucky_message)

    @app_commands.command(description="Hope that your victims will have a bad time.")
    @app_commands.describe(user="Who will become your next victim?")
    @app_commands.guild_only()
    async def unlucky(self, interaction: Interaction, user: discord.Member):
        if not interaction.guild:
            return

        if interaction.user == user:
            user = random.choice(interaction.guild.members)

        unlucky_message = random.choice(self.unlucky_messages)
        unlucky_message = unlucky_message.replace("<user>", user.display_name)
        unlucky_message = unlucky_message.replace("<author>", interaction.user.display_name)

        return await interaction.response.send_message(unlucky_message)
