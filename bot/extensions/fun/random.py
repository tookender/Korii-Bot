import asyncio
import random
from typing import Optional

import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from bot.utilities.embed import Embed


class RandomCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    fun = app_commands.Group(name="fun", description="General entertainment commands.")

    async def wait_and_send(
        self, interaction: discord.Interaction, content: str, wait: int = 2
    ):
        split = content.split("...")

        await interaction.response.send_message(
            f"{split[0]}... {self.bot.E['loading']}"
        )
        await asyncio.sleep(wait)
        return await interaction.edit_original_response(content=content)

    @fun.command(description="Turn a user's profile picture into emojis.")
    @app_commands.describe(
        user="The user's profile picture you wish to turn into emojis."
    )
    @app_commands.guild_only()
    async def emojify(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        request = await self.bot.session.get("https://api.jeyy.xyz/text/emojify", params={"image_url": user.display_avatar.url})
        json = await request.json()

        embed = Embed(description=f"```\n{json['text']}\n```")

        return await interaction.response.send_message(embed=embed)

    @fun.command(description="Ask the eightball a question!")
    @app_commands.describe(question="The question you wish to ask the magic eightball.")
    async def eightball(self, interaction: discord.Interaction, question: str):
        answers = [
            "it is certain",
            "it is decidedly so",
            "without a doubt",
            "yes - definitely",
            "you may rely on it",
            "as I see it, yes",
            "most likely",
            "outlook good",
            "yes",
            "signs point to yes",
            "reply hazy, try again",
            "ask again later",
            "better not tell you now",
            "cannot predict now",
            "concentrate and ask again",
            "don't count on it",
            "my reply is no",
            "my sources say no",
            "outlook not so good",
            "very doubtful",
        ]

        return await self.wait_and_send(
            interaction,
            f"🎱 **|** The magic eight ball says... {random.choice(answers)}.",
        )

    @fun.command(description="Measures the specified person's banana.")
    @app_commands.describe(user="The user of which you want to measure the banana.")
    @app_commands.guild_only()
    async def banana(
        self, interaction: discord.Interaction, user: Optional[discord.Member] = None
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        ap = "'"

        emojis = ["🍌", "🍆", "🥒"]

        return await self.wait_and_send(
            interaction,
            f"{random.choice(emojis)} **|** {'Your banana' if not user else f'{user.display_name}{ap}s banana'} is... {random.randint(3, 25)} cm long!",
        )

    @fun.command(description="Generates a random number.")
    @app_commands.describe(minimum="The minimum random number.")
    @app_commands.describe(maximum="The max random number.")
    async def random_number(
        self,
        interaction: discord.Interaction,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
    ):
        nl = "\n"
        add = None

        if not minimum:
            minimum = 1

        if not maximum:
            maximum = 1000

        if minimum > maximum:
            minimum = 1
            maximum = 1000
            add = "Minimum number was over maximum number."

        return await self.wait_and_send(
            interaction,
            f"🔢 **|** The randomly generated number between `{minimum}` and `{maximum}` is... **{random.randint(minimum, maximum)}**!{f'{nl}{add}' if add else ''}",
        )

    @fun.command(description="Flip a virtual coin.")
    async def coinflip(self, interaction: discord.Interaction):
        answers = ["heads", "tails"]

        return await self.wait_and_send(
            interaction, f"🪙 **|** The coin landed on... {random.choice(answers)}!"
        )

    @fun.command(description="Roll a virtual dice.")
    async def dice(self, interaction: discord.Interaction):
        return await self.wait_and_send(
            interaction,
            f"🎲 **|** The dice landed on the number... {random.randint(1, 6)}!",
        )

    @fun.command(description="Try it and see.")
    async def tias(self, interaction: discord.Interaction):
        return await interaction.response.send_message("https://tryitands.ee/")
