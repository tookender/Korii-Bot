def calculate_potential(power, current, total):
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
    abilities = [
        {"name": "Spinning Blade Smash / Void Dragon", "multiplier": 148},
        {"name": "Kunai Knives (3 ticks)", "multiplier": 150 / 3},
        {"name": "Rift Beam (37 ticks)", "multiplier": 203 / 37},
        {"name": "Triple Quake (3 ticks)", "multiplier": 144 / 3},
        {"name": "Chain Storm (6 ticks)", "multiplier": 147 / 6},
        {"name": "Blade Barrage / God Spear / Amethyst Beams / Jade Rain", "multiplier": 133},
        {"name": "Jade Roller", "multiplier": 126},
        {"name": "Solar Beam (2 ticks)", "multiplier": 126 / 2}
    ]
    
    ability_multiplier = abilities[selected_ability]["multiplier"]

    dmg = (weapon + armor + helmet + ring1 + ring2) * skill * ability_multiplier
    
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

    low_damage = int(low)
    base_damage = int(dmg)
    high_damage = int(high)

    low_inner_damage = int(low_inner)
    base_inner_damage = int(base_inner)
    high_inner_damage = int(high_inner)

    low_e_inner_damage = int(low_e_inner)
    base_e_inner_damage = int(base_e_inner)
    high_e_inner_damage = int(high_e_inner)

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
        }
    }
