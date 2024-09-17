import discord
from discord import app_commands
from discord.ext import commands

from ._base import EconomyBase, GuildContext
from .utils import *


class BankCog(EconomyBase):
    @commands.hybrid_command(description="Deposit money into your bank.", aliases=["dep"])
    @app_commands.describe(amount="The amount of money you want to deposit into the bank.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def deposit(self, ctx: GuildContext, amount: BalanceConverter):
        if not await has_enough_money(self.bot, ctx.author.id, ctx.guild.id, amount):
            balance = await get_balance(self.bot, ctx.author.id, ctx.guild.id)

            return await self.send_embed(ctx, text=f"{self.bot.E['no']} | You only have **${balance}**.", color=discord.Color.red())

        await add_bank(self.bot, ctx.author.id, ctx.guild.id, amount)
        await remove_money(self.bot, ctx.author.id, ctx.guild.id, amount)

        return await self.send_embed(
            ctx,
            text=f"{self.bot.E['yes']} | Deposited **${amount}** into your bank.",
            color=discord.Color.green(),
        )

    @commands.hybrid_command(description="Withdraw money from your bank.", aliases=["with"])
    @app_commands.describe(amount="The amount of money you want to withdraw from the bank.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def withdraw(self, ctx: GuildContext, amount: BankConverter):
        if not await has_enough_bank(self.bot, ctx.author.id, ctx.guild.id, amount):
            bank = await get_bank(self.bot, ctx.author.id, ctx.guild.id)

            return await self.send_embed(ctx, text=f"{self.bot.E['no']} | You only have **${bank}**.", color=discord.Color.red())

        await remove_bank(self.bot, ctx.author.id, ctx.guild.id, amount)
        await add_money(self.bot, ctx.author.id, ctx.guild.id, amount)

        return await self.send_embed(
            ctx,
            text=f"{self.bot.E['yes']} | Withdrew **${amount}** from your bank.",
            color=discord.Color.green(),
        )
