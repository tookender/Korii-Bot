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
        