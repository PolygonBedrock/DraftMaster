from openers.value_data import *
from utils.key_utils import *

print("HERO VALUES")
for hero in hero_values:
    print(hero + "\t" + str(hero_values[hero]))
print("\n")

print("MATCHUP VALUES")
for matchup in matchup_values:
    hero1, hero2 = split_matchup_key(matchup)
    hero1_value_key = make_value_key(hero1)
    hero2_value_key = make_value_key(hero2)
    hero1_value = matchup_values[matchup][hero1_value_key]
    hero2_value = matchup_values[matchup][hero2_value_key]
    print(matchup + "\t" + str(hero1_value - hero2_value))
print("\n")

print("COMBO VALUES")
for combo in combo_values:
    print(combo + "\t" + str(combo_values[combo]))
print("\n")

print("FACTION VALUES")
for faction in faction_values:
    print(faction + "\t" + str(faction_values[faction]))
print("\n")
