from utils.advantage_utils import *
import itertools
from openers.games_data import *

print("Processing data...")
for game in games:
    radiant = game[RADIANT_KEY]
    dire = game[DIRE_KEY]
    radiant_win = game[WINNER_KEY] == RADIANT_KEY
    dire_win = not radiant_win
    for hero in radiant:
        record_hero(hero, radiant_win)
    for hero in dire:
        record_hero(hero, dire_win)
    for radiant_hero in radiant:
        for dire_hero in dire:
            record_matchup(radiant_hero, dire_hero, radiant_win)
    for combo in itertools.combinations(radiant, 2):
        record_combo(combo[0], combo[1], radiant_win)
    for combo in itertools.combinations(dire, 2):
        record_combo(combo[0], combo[1], dire_win)
    record_faction(radiant_win)

print("Calculating winrates...")
calculate_winrates()

print("Calculating advantages...")
calculate_advantages()

print("Assigning values...")
assign_values()

print("Saving data...")
save_to_file(data, VALUES_FILE)