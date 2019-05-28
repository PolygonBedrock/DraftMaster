from openers.value_data import *
from utils.key_utils import *

output_values = {}

print("HERO VALUES")
for hero in hero_values:
    output_values[hero] = hero_values[hero]
    for other_hero in hero_values:
        if hero != other_hero:
            matchup_key = make_matchup_key(hero, other_hero)
            matchup = matchup_values[matchup_key]
            hero_value_key = make_value_key(hero)
            other_hero_value_key = make_value_key(other_hero)
            combo_key = make_combo_key(hero, other_hero)

            output_values[hero] += combo_values[combo_key]
            output_values[hero] += matchup[hero_value_key] - matchup[other_hero_value_key]

    print(hero + "\t" + str(output_values[hero]))

