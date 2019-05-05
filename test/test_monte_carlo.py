from utils.monte_carlo import *
from main.constants import *
from utils.time_utils import *

radiant = []
dire = []
banned = []
depth = 2
pick_index = 0
pick_order = CAPTAINS_MODE_ORDER
best_score = 0

print("Processing...")
for current_pick_index in range(pick_index, len(pick_order)):
    pick = pick_order[current_pick_index]
    acting_team_key = pick[TEAM_KEY]
    action = pick[ACTION_KEY]
    radiant_turn = None
    is_pick = None
    if acting_team_key == RADIANT_KEY:
        radiant_turn = True
    elif acting_team_key == DIRE_KEY:
        radiant_turn = False
    if action == PICK_KEY:
        is_pick = True
    elif action == BAN_KEY:
        is_pick = False
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
    if radiant_turn:
        if is_pick:
            radiant.append(best_hero)
            print("Radiant picks: " + best_hero + "; Time: " + str(think_time))
        else:
            banned.append(best_hero)
            print("Radiant bans: " + best_hero + "; Time: " + str(think_time))
    else:
        if is_pick:
            dire.append(best_hero)
            print("Dire picks: " + best_hero + "; Time: " + str(think_time))
        else:
            banned.append(best_hero)
            print("Dire bans: " + best_hero + "; Time: " + str(think_time))

print("Radiant: ", radiant)
print("Dire: ", dire)
print("Banned: ", banned)
