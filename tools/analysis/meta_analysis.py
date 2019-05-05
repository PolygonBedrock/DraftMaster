from utils.monte_carlo import *
from utils.time_utils import *
from openers.hero_indexes import *

radiant = []
dire = []
banned = []
depth = 1
pick_index = 1
pick_order = ALL_PICK_ORDER_RADIANT
best_score = 0
hero_num_picks = {}

print("Setting up...")
for hero in hero_indexes:
    hero_num_picks[hero] = 0

print("Processing...")
for first_pick_hero in hero_indexes:
    print("Running draft with first hero: " + first_pick_hero)
    radiant.clear()
    dire.clear()
    banned.clear()
    radiant.append(first_pick_hero)
    for current_pick_index in range(pick_index, len(pick_order)):
        pick = pick_order[current_pick_index]
        acting_team_key = pick[TEAM_KEY]
        radiant_turn = None
        if acting_team_key == RADIANT_KEY:
            radiant_turn = True
        elif acting_team_key == DIRE_KEY:
            radiant_turn = False
        start_time = current_time_ms()
        hero_scores_worst = monte_carlo(radiant, dire, banned, depth, current_pick_index, pick_order, False)
        hero_scores_best = monte_carlo(radiant, dire, banned, depth, current_pick_index, pick_order, True)
        stop_time = current_time_ms()
        think_time = stop_time - start_time
        best_score = NEGATIVE_INFINITY
        best_hero = None
        for hero in hero_scores_worst:
            score = hero_scores_worst[hero] + hero_scores_best[hero]
            if score > best_score:
                best_score = score
                best_hero = hero
        hero_num_picks[best_hero] += 1
        if radiant_turn:
                radiant.append(best_hero)
        else:
                dire.append(best_hero)

for hero in hero_num_picks:
    print(hero + ": " + str(hero_num_picks[hero]))
