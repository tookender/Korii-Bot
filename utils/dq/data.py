# --------------------------------------------- #
# Please view 'notice.md' for more information. #
# --------------------------------------------- #

abilities_ticks = [
	{"name": "Gravity Leap", "ticks": 1},
	{"name": "Unstable Warp (2 ticks)", "ticks": 2},
	{"name": "Mighty Cleave (fully charged, 2 ticks)", "ticks": 2},
	{"name": "Mighty Cleave (half charged)", "ticks": 1},
	{"name": "Sacrificial Orbs (fully charged)", "ticks": 1},
	{"name": "Sacrificial Orbs (half charged)", "ticks": 1},
	{"name": "Shatterstrike (6 ticks)", "ticks": 6},
	{"name": "Voidflames (5 ticks)", "ticks": 5},

	# YP
	{"name": "Spinning Blade Smash / Void Dragon", "ticks": 1},
	{"name": "Kunai Knives (3 ticks)", "ticks": 3},
	{"name": "Rift Beam (37 ticks)", "ticks": 37},
	{"name": "Triple Quake (3 ticks)", "ticks": 3},
	{"name": "Chain Storm (6 ticks)", "ticks": 6},

	# GS
	{"name": "Blade Barrage / God Spear / Amethyst Beams / Jade Rain", "ticks": 1},
	{"name": "Jade Roller", "ticks": 1},
	{"name": "Solar Beam (2 ticks)", "ticks": 2}
]

abilities = [
	# AV
	{"name": "Gravity Leap", "multiplier": 190},
	{"name": "Unstable Warp (2 ticks)", "multiplier": 180 / 2},
	{"name": "Mighty Cleave (fully charged, 2 ticks)", "multiplier": 280 / 2},
	{"name": "Mighty Cleave (half charged)", "multiplier": 120},
	{"name": "Sacrificial Orbs (fully charged)", "multiplier": 280},
	{"name": "Sacrificial Orbs (half charged)", "multiplier": 140},
	{"name": "Shatterstrike (6 ticks)", "multiplier": 186 / 6},
	{"name": "Voidflames (5 ticks)", "multiplier": 185 / 5},

	# YP
	{"name": "Spinning Blade Smash / Void Dragon", "multiplier": 148},
	{"name": "Kunai Knives (3 ticks)", "multiplier": 150 / 3},
	{"name": "Rift Beam (37 ticks)", "multiplier": 203 / 37},
	{"name": "Triple Quake (3 ticks)", "multiplier": 144 / 3},
	{"name": "Chain Storm (6 ticks)", "multiplier": 147 / 6},

	# GS
	{"name": "Blade Barrage / God Spear / Amethyst Beams / Jade Rain", "multiplier": 133},
	{"name": "Jade Roller", "multiplier": 126},
	{"name": "Solar Beam (2 ticks)", "multiplier": 126 / 2}
]


dungeons = {
	"Abyssal Void": {
		"Insane [210]": 1.07e12,
		"Nightmare [215]": 1.47e12,
		"Nightmare (with The Voidborn) [215]": 1.91e12
	},
	"Yokai Peak": {
		"Insane [200]": 192650000000,
		"Nightmare [205]": 350950000000
	},
	"Gilded Skies": {
		"Insane [190]": 63500000000,
		"Nightmare [195]": 115500000000
	},
	"Northern Lands": {
		"Insane [180]": 21820000000,
		"Nightmare [185]": 36600000000,
		"Nightmare (with Odin-R) [185]": 58600000000
	},
	"Enchanted Forest": {
		"Insane [170]": 6900000000,
		"Nightmare [175]": 11280000000
	},
	"Aquatic Temple": {
		"Insane [160]": 2034000000,
		"Nightmare [165]": 3564000000
	},
	"Volcanic Chambers": {
		"Insane [150]": 755000000,
		"Nightmare [155]": 1225000000
	},
	"Orbital Outpost": {
		"Insane [135]": 329000000,
		"Nightmare [140]": 506500000
	},
	"Steampunk Sewers": {
		"Insane [120]": 35700000,
		"Nightmare [125]": 59600000
	},
	"Ghastly Harbor": {
		"Insane [110]": 12840000,
		"Nightmare [115]": 24160000
	},
	"The Canals": {
		"Insane [100]": 4594000,
		"Nightmare [105]": 8005000
	},
	"Samurai Palace": {
		"Insane [90]": 1934000,
		"Nightmare [95]": 3500000
	},
	"The Underworld": {
		"Insane [80]": 546000,
		"Nightmare [85]": 924000
	},
	"King's Castle": {
		"Insane [70]": 135900,
		"Nightmare [75]": 271800
	},
	"Pirate Island": {
		"Insane [60]": 51150,
		"Nightmare [65]": 82200
	},
	"Winter Outpost (Current)": {
		"Easy [30]": 18800,
		"Medium [40]": 46800,
		"Hard [50]": 69000
	},
	"Winter Outpost (Legacy)": {
		"Easy [30]": 8340,
		"Medium [40]": 11300,
		"Hard [45]": 16140,
		"Insane [50]": 27840,
		"Nightmare [55]": 46180
	},
	"Desert Temple (Current)": {
		"Easy [1]": 490,
		"Medium [5]": 1296,
		"Hard [15]": 4789
	},
	"Desert Temple (Legacy)": {
		"Easy [1]": 253,
		"Medium [6]": 396,
		"Hard [12]": 785,
		"Insane [20]": 1307,
		"Nightmare [27]": 2669
	},
}