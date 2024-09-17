import asyncio
import random
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from utils import Embed, Interaction
from utils.constants import NOT_YOUR_BUTTON

from ._base import EconomyBase, GuildContext
from .utils import *

values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
deck = list(values.keys()) * 4


def draw_card():
    return random.choice(deck)


def calculate_hand(hand):
    total = sum(values[card] for card in hand)
    aces = hand.count("A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


class BlackjackView(discord.ui.View):
    message: discord.Message

    def __init__(self, player_hand, dealer_hand, author: discord.User | discord.Member, amount: BalanceConverter):
        super().__init__(timeout=300)
        self.embed: discord.Embed
        self.author = author
        self.amount = amount
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.embed = self.create_embed()

    def create_embed(self):
        embed = Embed()

        embed.add_field(
            name="Your Hand",
            value=f"{', '.join(self.player_hand)}\nValue: {calculate_hand(self.player_hand)}",
        )

        embed.add_field(
            name="Dealer Hand",
            value=f"{self.dealer_hand[0]}, ?",
        )

        embed.set_author(
            name=self.author.display_name,
            icon_url=self.author.avatar.url if self.author.avatar else None,
        )

        return embed

    def check_result(self):
        player_total = calculate_hand(self.player_hand)
        dealer_total = calculate_hand(self.dealer_hand)

        if player_total > 21:
            return "Bust"
        elif dealer_total > 21 or player_total > dealer_total:
            return "Win"
        elif player_total < dealer_total:
            return "Lose"
        else:
            return "Tie"

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(random.choice(NOT_YOUR_BUTTON).replace("[user]", self.author.display_name), ephemeral=True)
            return False

        return True

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: Interaction, _):
        self.player_hand.append(draw_card())

        if calculate_hand(self.player_hand) > 21:
            self.embed.description = f"**Result:** Bust -${self.amount}"
            self.embed.colour = discord.Colour.red()

            self.embed.clear_fields()
            self.embed.add_field(name="Your Hand", value=f"{', '.join(self.player_hand)}\nValue: {calculate_hand(self.player_hand)}")

            self.embed.add_field(name="Dealer Hand", value=f"{', '.join(self.dealer_hand)}\nValue: {calculate_hand(self.dealer_hand)}")

            await remove_money(interaction.client, self.author.id, interaction.guild.id, self.amount)
            await self.message.edit(embed=self.embed, view=None)

        else:
            self.embed = self.create_embed()
            await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: Interaction, _):
        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(draw_card())

        result = self.check_result()

        if result == "Lose" or result == "Bust":
            self.embed.color = discord.Colour.red()
            money = f"-${self.amount}"
            await remove_money(interaction.client, self.author.id, interaction.guild.id, self.amount)
        elif result == "Win":
            self.embed.color = discord.Colour.green()
            money = f"+${self.amount}"
            await add_money(interaction.client, self.author.id, interaction.guild.id, self.amount)
        else:
            self.embed.color = discord.Colour.yellow()
            money = f"no money lost or gained"

        self.embed.description = f"**Result:** {result} {money}"
        self.embed.remove_field(1)
        self.embed.add_field(name="Dealer Hand", value=f"{', '.join(self.dealer_hand)}\nValue: {calculate_hand(self.dealer_hand)}")

        await self.message.edit(embed=self.embed, view=None)


class GamblingCog(EconomyBase):
    async def amount_autocomplete(self, interaction: Interaction, current: str):
        amounts = ["all", "half", "100", "250", "500", "750", "1000"]
        return [app_commands.Choice(name=amount, value=amount) for amount in amounts if current.lower() in amount.lower()]

    async def roulette_autocomplete(self, interaction: Interaction, current: str):
        options = ["red", "black", "green", "00"] + [str(i) for i in range(37)]
        return [app_commands.Choice(name=option, value=option) for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(description="Coinflip an amount of money.", aliases=["cf"])
    @app_commands.describe(choice="Whether you want to bet on heads or tails.")
    @app_commands.describe(amount="The amount you want to bet on the coinflip.")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="heads", value="Bet your money on heads."),
            app_commands.Choice(name="tails", value="Bet your money on tails."),
        ]
    )
    @app_commands.autocomplete(amount=amount_autocomplete)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def coinflip(self, ctx: GuildContext, choice: Literal["heads", "h", "tails", "t"], amount: BalanceConverter):
        balance = await get_balance(self.bot, ctx.author.id, ctx.guild.id)

        if not await has_enough_money(self.bot, ctx.author.id, ctx.guild.id, amount):
            return await self.send_embed(
                ctx,
                text=f"{self.bot.E['no']} You only have **${balance}**.",
                color=discord.Color.red(),
            )

        async with ctx.typing():
            await asyncio.sleep(1)

        number = random.randint(1, 1000)

        if number & 2 == 0:
            result = "heads"
        else:
            result = "tails"

        if choice == result or choice == result[0]:
            won = True
        else:
            won = False

        embed = await self.send_embed(
            ctx,
            text=f"🪙 The coin landed on **{result}**. You **{'won!!!' if won else 'lost :('}**",
            color=discord.Color.green() if won else discord.Color.red(),
            return_embed=True,
            footer=f"Bet: ${amount}",
        )

        embed.add_field(name="Your balance", value=f"{balance} -> {f'{balance + amount}' if won else f'{balance - amount}'}", title=False)

        if won:
            await add_money(self.bot, ctx.author.id, ctx.guild.id, amount)
        else:
            await remove_money(self.bot, ctx.author.id, ctx.guild.id, amount)

        return await ctx.send(embed=embed, silent=True)

    @commands.hybrid_command(description="Bet money on blackjack.", aliases=["bj"])
    @app_commands.describe(amount="The amount you want to bet on the blackjack.")
    @app_commands.autocomplete(amount=amount_autocomplete)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blackjack(self, ctx: GuildContext, amount: BalanceConverter):
        balance = await get_balance(self.bot, ctx.author.id, ctx.guild.id)

        if not await has_enough_money(self.bot, ctx.author.id, ctx.guild.id, amount):
            return await self.send_embed(
                ctx,
                text=f"{self.bot.E['no']} You only have **${balance}**.",
                color=discord.Color.red(),
            )

        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]

        view = BlackjackView(player_hand, dealer_hand, ctx.author, amount)

        try:
            message = await ctx.send(embed=view.embed, view=view, silent=True)
        except discord.HTTPException:
            return
        else:
            if view is not discord.utils.MISSING:
                view.message = message

    @commands.hybrid_command(description="Bet your money on roulette.")
    @app_commands.describe(amount="The amount you want to bet on roulette.")
    @app_commands.describe(choice="What you want to bet on. Options: green, red, black, 00, and numbers from 0-36")
    @app_commands.autocomplete(amount=amount_autocomplete)
    @app_commands.autocomplete(choice=roulette_autocomplete)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roulette(self, ctx: GuildContext, amount: BalanceConverter, choice: RouletteConverter):
        number = random.randint(0, 37)

        if number == 0:
            correct_color = "green"
        elif number % 2 == 0:
            correct_color = "red"
        else:
            correct_color = "black"

        emoji_colors = {
            "green": "🟩",
            "red": "🟥",
            "black": "⬛",
        }

        if number == 37:
            number = 00

        if choice == correct_color:
            await self.send_embed(
                ctx,
                text=f"{self.bot.E['yes']} **Success!** The color is **{emoji_colors[correct_color]} {correct_color} ({number})**. +${amount}",
                color=discord.Color.green(),
            )

            return await add_money(self.bot, ctx.author.id, ctx.guild.id, amount)

        await self.send_embed(
            ctx,
            text=f"{self.bot.E['no']} **You failed :(** The correct color was **{emoji_colors[correct_color]} {correct_color} ({number})**. -${amount}",
            color=discord.Color.red(),
        )

        return await remove_money(self.bot, ctx.author.id, ctx.guild.id, amount)
