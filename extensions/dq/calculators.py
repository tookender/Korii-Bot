from numerize.numerize import numerize
from discord import app_commands, ui, ButtonStyle
from discord.ext import commands

from ._base import DQBase
from utils.dq.calculators import calculate_upgrade_cost, calculate_potential, calculate_damage, calculate_runs
from utils import Embed
from typing import Optional
from decimal import Decimal
from utils.dq.data import abilities_ticks

def n(value):
	return numerize(value, 3)

def fn(num):
    suffixes = ["", "K", "M", "B", "T", "Q", "Qi", "Sx", "Sp", "Oc", " Nonillion", " Decillion", " Undecillion", " Duodecillion", " Tredecillion", " Quattuordecillion", " i don't like you"]
    dnum = Decimal(num)
    
    for i, suffix in enumerate(suffixes):
        unit = Decimal(1000) ** i
        if dnum < unit * 1000:
            formatted_number = dnum / unit
            return f"{formatted_number:.2f}".rstrip('0').rstrip('.') + suffix
    
    return f"{dnum:.2e}"

class DamageView(ui.View):
    def __init__(self, damage_data, ability_name):
        super().__init__()
        self.damage_data = damage_data
        self.ticks = next((item["ticks"] for item in abilities_ticks if item["name"] == ability_name), 1)
        
        if self.ticks == 1:
            self.remove_item(self.full_damage)

    @ui.button(label="Show Full Damage", style=ButtonStyle.green)
    async def full_damage(self, interaction, button):
        ticked_damage = {
            category: {
                key: value * self.ticks for key, value in stats.items()
            } for category, stats in self.damage_data.items()
        }
        
        embed = create_damage_embed(f"Full Damage Calculator ({self.ticks} ticks)", ticked_damage)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def create_damage_embed(title: str, damage_data: dict) -> Embed:
    embed = Embed(title=title)
    embed.set_author(name="Dungeon Quest Helper", url="https://www.roblox.com/games/2414851778")

    for category, label, emoji in [
        ("No Inner", "No Inner", "❌"),
        ("With Inner", "With Inner", "✨"),
        ("With Enhanced Inner", "With Enhanced Inner", "🌟")
    ]:
        stats = damage_data[category]
        embed.add_field(
            name=f"{emoji} {label}",
            value=f"**Low Damage:** {fn(stats['Low Damage'])}\n**Average Damage:** {fn(stats['Average'])}\n**High Damage:** {fn(stats['High Damage'])}",
            inline=False
        )
    
    return embed

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
		embed.set_author(name="Dungeon Quest Helper", url="https://www.roblox.com/games/2414851778")

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
		# AV
		app_commands.Choice(name="Gravity Leap", value="Gravity Leap"),
		app_commands.Choice(name="Unstable Warp (2 ticks)", value="Unstable Warp (2 ticks)"),
		app_commands.Choice(name="Mighty Cleave (fully charged, 2 ticks)", value="Mighty Cleave (fully charged, 2 ticks)"),
		app_commands.Choice(name="Mighty Cleave (half charged)", value="Mighty Cleave (half charged)"),
		app_commands.Choice(name="Sacrificial Orbs (fully charged)", value="Sacrificial Orbs (fully charged)"),
		app_commands.Choice(name="Sacrificial Orbs (half charged)", value="Sacrificial Orbs (half charged)"),
		app_commands.Choice(name="Shatterstrike (6 ticks)", value="Shatterstrike (6 ticks)"),
		app_commands.Choice(name="Voidflames (5 ticks)", value="Voidflames (5 ticks)"),

		# YP
		app_commands.Choice(name="Spinning Blade Smash / Void Dragon", value="Spinning Blade Smash / Void Dragon"),
		app_commands.Choice(name="Kunai Knives (3 ticks)", value="Kunai Knives (3 ticks)"),
		app_commands.Choice(name="Rift Beam (37 ticks)", value="Rift Beam (37 ticks)"),
		app_commands.Choice(name="Triple Quake (3 ticks)", value="Triple Quake (3 ticks)"),
		app_commands.Choice(name="Chain Storm (6 ticks)", value="Chain Storm (6 ticks)"),

		# GS
		app_commands.Choice(name="Blade Barrage / God Spear / Amethyst Beams / Jade Rain", value="Blade Barrage / God Spear / Amethyst Beams / Jade Rain"),
		app_commands.Choice(name="Jade Roller", value="Jade Roller"),
		app_commands.Choice(name="Solar Beam (2 ticks)", value="Solar Beam (2 ticks)"),
	])
	async def calc_damage(self, ctx, ability: app_commands.Choice[str], helmet_power: Optional[int] = 0, armor_power: Optional[int] = 0, weapon_power: Optional[int] = 0,
						ring1_power: Optional[int] = 0, ring2_power: Optional[int] = 0, damage_skill_points: Optional[int] = 0):
		damage = calculate_damage(ability, armor_power, helmet_power, weapon_power, ring1_power, ring2_power, damage_skill_points)
		
		embed = create_damage_embed("Damage Range Calculator", damage)
		view = DamageView(damage, ability.value)
		
		return await ctx.send(embed=embed, view=view)
	
	@commands.hybrid_command(description="Calculate the number of runs needed to reach the goal level given the selected dungeon.")
	@app_commands.describe(current_level="The current level.")
	@app_commands.describe(goal_level="The goal level.")
	@app_commands.describe(dungeon_name="The name of the dungeon.")
	@app_commands.describe(event_active="Whether the x2 EXP event is active.")
	@app_commands.describe(booster_active="Whether the EXP potion is active.")
	@app_commands.describe(vip="Whether you have VIP.")
	@app_commands.choices(dungeon_name=[
		app_commands.Choice(name="Abyssal Void", value="Abyssal Void"),
		app_commands.Choice(name="Yokai Peak", value="Yokai Peak"),
		app_commands.Choice(name="Gilded Skies", value="Gilded Skies"),
		app_commands.Choice(name="Northern Lands", value="Northern Lands"),
		app_commands.Choice(name="Enchanted Forest", value="Enchanted Forest"),
		app_commands.Choice(name="Aquatic Temple", value="Aquatic Temple"),
		app_commands.Choice(name="Volcanic Chambers", value="Volcanic Chambers"),
		app_commands.Choice(name="Orbital Outpost", value="Orbital Outpost"),
		app_commands.Choice(name="Steampunk Sewers", value="Steampunk Sewers"),
		app_commands.Choice(name="Ghastly Harbor", value="Ghastly Harbor"),
		app_commands.Choice(name="The Canals", value="The Canals"),
		app_commands.Choice(name="Samurai Palace", value="Samurai Palace"),
		app_commands.Choice(name="The Underworld", value="The Underworld"),
		app_commands.Choice(name="King's Castle", value="King's Castle"),
		app_commands.Choice(name="Pirate Island", value="Pirate Island"),
		app_commands.Choice(name="Winter Outpost (Current)", value="Winter Outpost (Current)"),
		app_commands.Choice(name="Winter Outpost (Legacy)", value="Winter Outpost (Legacy)"),
		app_commands.Choice(name="Desert Temple (Current)", value="Desert Temple (Current)"),
		app_commands.Choice(name="Desert Temple (Legacy)", value="Desert Temple (Legacy)"),
	])
	async def calc_runs(self, ctx, current_level: int, goal_level: int, dungeon_name: str, event_active: Optional[bool] = False, booster_active: Optional[bool] = False, vip: Optional[bool] = False):
		result = calculate_runs(current_level, goal_level, dungeon_name, event_active, booster_active, vip)
		
		embed = Embed(title="Dungeon Runs Calculator",
				description=f"To go from **Level {result['current_level']}** to **Level {result['goal_level']}** in **{result['dungeon_name']}** you will need **{fn(result['xp_needed'])} XP**")
		embed.set_author(name="Dungeon Quest Helper", url="https://www.roblox.com/games/2414851778")

		runs = result["runs"]

		for run in runs.items():
			embed.add_field(name=f"{run[0]} Runs", value=f"**{fn(run[1])}** runs", inline=True)
		
		await ctx.send(embed=embed)