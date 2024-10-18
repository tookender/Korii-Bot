from numerize.numerize import numerize
from discord import app_commands
from discord.ext import commands

from ._base import DQBase
from utils.calculators import calculate_upgrade_cost, calculate_potential, calculate_damage
from utils import Embed
from typing import Optional
from decimal import Decimal

def n(value):
	return numerize(value, 3)

def fn(num):
    suffixes = ["", "K", "M", "B", "T", "Q", "Qi"]
    dnum = Decimal(num)
    
    for i, suffix in enumerate(suffixes):
        unit = Decimal(1000) ** i
        if dnum < unit * 1000:
            formatted_number = dnum / unit
            return f"{formatted_number:.2f}".rstrip('0').rstrip('.') + suffix
    
    return f"{dnum:.2e}"

class CalculatorsCog(DQBase):
	@commands.hybrid_command(description="Calculate max potential of an item and the upgrade cost.", aliases=["potential", "pot", "calc_pot", "calcpot", "potcalc", "potentialcalc"])
	@app_commands.describe(current_power="Current power of your item.")
	@app_commands.describe(current_upgrades="Current amount of upgrades on your item.")
	@app_commands.describe(total_upgrades="Total amount of upgrades of your item.")
	async def calc_potential(self, ctx, current_power: int, current_upgrades: int, total_upgrades: int):
		upgrade_cost = calculate_upgrade_cost(current_upgrades, total_upgrades)
		potential = calculate_potential(current_power, current_upgrades, total_upgrades)
        
		humanized_cost = f"({n(upgrade_cost)})"
		humanized_potential = f"({n(potential)})"

		embed = Embed(title="Potential Calculator")

		embed.add_field(name="💪 Max Power", value=f"{potential:,} {humanized_potential if potential > 999 else ''}", inline=False)
		embed.add_field(name="💰 Upgrade Cost", value=f"{upgrade_cost:,} {humanized_cost if upgrade_cost > 999 else ''}", inline=False)

		return await ctx.send(embed=embed)
	
	abilities = [
		"Spinning Blade Smash / Void Dragon", "Kunai Knives (3 ticks)", "Rift Beam (37 ticks)", "Triple Quake (3 ticks)", "Chain Storm (6 ticks)",
		"Blade Barrage / God Spear / Amethyst Beams / Jade Rain", "Jade Roller", "Solar Beam (2 ticks)"
	]

	@commands.hybrid_command(description="Calculate your damage range with the given values.", aliases=["damage", "dmg", "calc_dmg", "calcdmg", "dmgcalc", "damagecalc"])
	@app_commands.describe(ability="Choose an ability, from Gilded Skies up to Yokai Peak.")
	@app_commands.describe(helmet_power="The power of your helmet.")
	@app_commands.describe(armor_power="The power of your armor.")
	@app_commands.describe(weapon_power="The power of your weapon.")
	@app_commands.describe(ring1_power="The power of your 1st ring.")
	@app_commands.describe(ring2_power="The power of your 2nd ring.")
	@app_commands.describe(damage_skill_points="The amount of damage skill points you have.")
	@app_commands.choices(ability=[
		app_commands.Choice(name="Spinning Blade Smash / Void Dragon", value="Spinning Blade Smash / Void Dragon"),
		app_commands.Choice(name="Kunai Knives (3 ticks)", value="Kunai Knives (3 ticks)"),
		app_commands.Choice(name="Rift Beam (37 ticks)", value="Rift Beam (37 ticks)"),
		app_commands.Choice(name="Triple Quake (3 ticks)", value="Triple Quake (3 ticks)"),
		app_commands.Choice(name="Chain Storm (6 ticks)", value="Chain Storm (6 ticks)"),
		app_commands.Choice(name="Blade Barrage / God Spear / Amethyst Beams / Jade Rain", value="Blade Barrage / God Spear / Amethyst Beams / Jade Rain"),
		app_commands.Choice(name="Jade Roller", value="Jade Roller"),
		app_commands.Choice(name="Solar Beam (2 ticks)", value="Solar Beam (2 ticks)"),
	])
	async def calc_damage(self, ctx, ability: app_commands.Choice[str], helmet_power: Optional[int] = 0, armor_power: Optional[int] = 0, weapon_power: Optional[int] = 0,
						ring1_power: Optional[int] = 0, ring2_power: Optional[int] = 0, damage_skill_points: Optional[int] = 0):
		damage = calculate_damage(ability, armor_power, helmet_power, weapon_power, ring1_power, ring2_power, damage_skill_points)

		ni_low = damage['No Inner']['Low Damage']
		ni_avg = damage['No Inner']['Average']
		ni_high = damage['No Inner']['High Damage']

		wi_low = damage['With Inner']['Low Damage']
		wi_avg = damage['With Inner']['Average']
		wi_high = damage['With Inner']['High Damage']

		ei_low = damage['With Enhanced Inner']['Low Damage']
		ei_avg = damage['With Enhanced Inner']['Average']
		ei_high = damage["With Enhanced Inner"]["High Damage"]

		embed = Embed(title="Damage Range Calculator", description=f"{damage}")

		embed.add_field(name="❌ No Inner", value=f"**Low Damage:** {fn(ni_low)}\n**Average Damage:** {fn(ni_avg)}\n**High Damage:** {fn(ni_high)}", inline=False)
		embed.add_field(name="✨ With Inner", value=f"**Low Damage:** {fn(wi_low)}\n**Average Damage:** {fn(wi_avg)}\n**High Damage:** {fn(wi_high)}", inline=False)
		embed.add_field(name="🌟 With Enhanced Inner", value=f"**Low Damage:** {fn(ei_low)}\n**Average Damage:** {fn(ei_avg)}\n**High Damage:** {fn(ei_high)}", inline=False)

		return await ctx.send(embed=embed)