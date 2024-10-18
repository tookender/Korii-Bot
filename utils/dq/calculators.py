# --------------------------------------------- #
# Please view 'notice.md' for more information. #
# --------------------------------------------- #

import json
from typing import Optional
from .data import abilities, dungeons

def calculate_potential(power, current, total):
    """
    Calculate the potential of an item.

    Parameters:
    power (int): The current power of the item.
    current (int): The current amount of upgrades on the item.
    total (int): The total amount of upgrades available for the item.

    Returns:
    int: The potential of the item.
    """
    potential = power
    upgrades = current
    while potential < 200 and upgrades < total:
        if potential < 20:
            potential += 1
        else:
            potential += potential // 20
        upgrades += 1
    potential += (total - upgrades) * 10
    return potential


def calculate_upgrade_cost(current, total):
    """
    Calculate the upgrade cost of an item.
    Code is very weird, do not question it.

    Parameters:
    current (int): The current amount of upgrades on the item.
    total (int): The total amount of upgrades available for the item.

    Returns:
    int: The upgrade cost of the item.
    """
    cost = 0
    if current < 24:
        if current == 0 and total > 0:
            cost = 100
        c = 100
        for i in range(1, min(24, total)):
            c = c * 1.06 + 50
            if i >= current:
                cost += int(c)

    s = 24 if current < 24 else 466 if current > 466 else current
    e = 24 if total < 24 else 466 if total > 466 else total
    cost += (e - s) * (110 * (e + s) - 2445)

    s = 466 if current < 466 else current
    e = 466 if total < 466 else total
    cost += (e - s) * 100000
    return cost


def calculate_damage(selected_ability, armor, helmet, weapon, ring1, ring2, skill):
    """
    Calculate the damage range you can do with the selected ability and the given stats.

    Parameters:
    selected_ability (app_commands.Choice[str]): The selected ability.
    armor (int): The power of the armor.
    helmet (int): The power of the helmet.
    weapon (int): The power of the weapon.
    ring1 (int): The power of the first ring.
    ring2 (int): The power of the second ring.
    skill (int): The skill points you have.

    Returns:
    dict: A dictionary containing the damage range for each type of damage. (With/Without Enhanced/Non-Enhanced Inner Rage/Focus)
    """

    ability_multiplier = 1

    for ability in abilities:
        if ability["name"] == selected_ability.value:
            ability_multiplier = ability["multiplier"]

    dmg = int(weapon * (0.6597 + 0.013202 * skill) * (armor + helmet + ring1 + ring2) * 0.0028 * ability_multiplier)
    low = dmg * 0.95
    high = dmg * 1.05

    # Inner is 80%, so 1.8
    # E(nhanced) Inner is 90%, so 1.9

    low_inner = dmg * 1.8 * 0.95
    base_inner = dmg * 1.8
    high_inner = dmg * 1.8 * 1.05

    low_e_inner = dmg * 1.9 * 0.95
    base_e_inner = dmg * 1.9
    high_e_inner = dmg * 1.9 * 1.05

    low_damage = low
    base_damage = dmg
    high_damage = high

    low_inner_damage = low_inner
    base_inner_damage = base_inner
    high_inner_damage = high_inner

    low_e_inner_damage = low_e_inner
    base_e_inner_damage = base_e_inner
    high_e_inner_damage = high_e_inner

    return {
        "No Inner": {
            "Low Damage": low_damage,
            "Average": base_damage,
            "High Damage": high_damage
        },
        "With Inner": {
            "Low Damage": low_inner_damage,
            "Average": base_inner_damage,
            "High Damage": high_inner_damage
        },
        "With Enhanced Inner": {
            "Low Damage": low_e_inner_damage,
            "Average": base_e_inner_damage,
            "High Damage": high_e_inner_damage
        },
        f"Other Information": {
            "ability_multiplier": ability_multiplier,
            "dmg": dmg,
            "selected_ability": selected_ability
        }
    }


def calculate_xp(current_level, goal_level):
    """
    Calculate the XP required to go from current_level to goal_level.

    Parameters:
    current_level (int): The current level.
    goal_level (int): The goal level.

    Returns:
    int: The XP required to go from current_level to goal_level.
    """
    xp = 0
    for x in range(current_level, goal_level):
        xp += round(84 * (1.13 ** (x - 1)))
    return xp


def calculate_runs(current_level: int, goal_level: int, dungeon_name: str, event_active, booster_active, vip):
    """
    Calculcate the number of runs needed to reach the goal level given the selected dungeon.

    Parameters:
    current_level (int): The current level.
    goal_level (int): The goal level.
    dungeon_name (str): The name of the dungeon.
    event_active (bool): Whether the event is active.
    booster_active (bool): Whether the booster is active.
    vip (bool): Whether the VIP is active.

    Returns:
    dict: A dictionary containing the number of runs needed, the amount of VIP runs needed, and the dungeon name and difficulty.
    """    
    xp_needed = calculate_xp(current_level, goal_level)
    
    modifier = 1
    if event_active:
        modifier += 1
    if booster_active:
        modifier += 1
    
    runs_required = {}
    
    for difficulty, dungeon_exp in dungeons[dungeon_name].items():
        amount_of_runs = int((xp_needed / (modifier * dungeon_exp)) + 0.5)
        runs_required[difficulty.lower()] = amount_of_runs
    
    output = {
        "current_level": current_level,
        "goal_level": goal_level,
        "dungeon_name": dungeon_name,
        "xp_needed": xp_needed,
        "runs": runs_required
    }
    
    return output
