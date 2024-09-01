import discord
from discord import app_commands
from discord.ext import commands

from ._base import DQBase
from utils.calculators import *
from utils import Embed


class CalculatorsCog(DQBase):
	@commands.hybrid_command(description="Calculate max potential of an item and the upgrade cost.", aliases=["potential", "pot", "calc_pot", "calcpot", "potcalc"])
	@app_commands.describe(current_power="Current power of your item.")
	@app_commands.describe(current_upgrades="Current amount of upgrades on your item.")
	@app_commands.describe(total_upgrades="Total amount of upgrades of your item.")
	async def calc_potential(self, ctx, current_power, current_upgrades, total_upgrades):
		upgrade_cost = calculate_upgrade_cost(current_upgrades, total_upgrades)
		potential = calculate_potential(current_power, current_upgrades, total_upgrades)
        
		embed = Embed(
            title="Potential Calculator",
            description=f"💪 **Max Power:** {potential:,}\n"\
						f"💰 **Upgrade Cost:** {upgrade_cost:,}"
		)

		return await ctx.send(embed=embed)