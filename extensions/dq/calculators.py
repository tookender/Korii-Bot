from numerize import numerize
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
	async def calc_potential(self, ctx, current_power: int, current_upgrades: int, total_upgrades: int):
		upgrade_cost = calculate_upgrade_cost(current_upgrades, total_upgrades)
		potential = calculate_potential(current_power, current_upgrades, total_upgrades)
        
		humanized_cost = f"({numerize.numerize(upgrade_cost)})"
		humanized_potential = f"({numerize.numerize(potential)})"

		embed = Embed(
            title="Potential Calculator",
            description=f"💪 **Max Power:** {potential:,} {humanized_cost if potential > 999 else ''}\n"\
						f"💰 **Upgrade Cost:** {upgrade_cost:,} {humanized_potential if upgrade_cost > 999 else ''}"
		)

		return await ctx.send(embed=embed)