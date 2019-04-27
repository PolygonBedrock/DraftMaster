from utils.advantage_utils import *
import itertools
from openers.games_data import *

print("Processing data...")
for game in games:
    radiant = game[RADIANT_KEY]
    dire = game[DIRE_KEY]
    radiantWin = game[WINNER_KEY] == RADIANT_KEY
    direWin = not radiantWin
    for hero in radiant:
        record_hero(hero, radiantWin)
    for hero in dire:
        record_hero(hero, direWin)
    for radiantHero in radiant:
        for direHero in dire:
            record_matchup(radiantHero, direHero, radiantWin)
    for combo in itertools.combinations(radiant, 2):
        record_combo(combo[0], combo[1], radiantWin)
    for combo in itertools.combinations(dire, 2):
        record_combo(combo[0], combo[1], direWin)
    record_faction(radiantWin)

print("Calculating winrates...")
calculate_winrates()

print("Calculating advantages...")
calculate_advantages()
    
print("Assigning values...")
assign_values()
    
print("Saving data...")
with open(VALUES_FILE, 'wb') as fp:
    pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
