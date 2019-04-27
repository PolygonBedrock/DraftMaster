import math
from utils.key_utils import *

hero_results = {}
matchup_results = {}
combo_results = {}
faction_results = {RADIANT_KEY: 0, DIRE_KEY: 0}

hero_winrates = {}
matchup_winrates = {}
combo_winrates = {}
faction_winrates = {}

hero_advantages = {}
matchup_advantages = {}
combo_advantages = {}
faction_advantages = {}

hero_values = {}
matchup_values = {}
combo_values = {}
faction_values = {}

data = {HEROES_KEY: hero_values, MATCHUPS_KEY: matchup_values, COMBOS_KEY: combo_values, FACTIONS_KEY: faction_values}


def calculate_hero_winrates():
    for hero in hero_results:
        wins = hero_results[hero][WINS_KEY]
        games = hero_results[hero][GAMES_KEY]
        hero_winrates[hero] = wins / games


def calculate_matchup_winrates():
    for matchup_key in matchup_results:
        hero1, hero2 = split_matchup_key(matchup_key)
        hero1_wins_key = make_wins_key(hero1)
        hero2_wins_key = make_wins_key(hero2)
        hero1_winrate_key = make_winrate_key(hero1)
        hero2_winrate_key = make_winrate_key(hero2)
        hero1_wins = matchup_results[matchup_key][hero1_wins_key]
        hero2_wins = matchup_results[matchup_key][hero2_wins_key]
        games = matchup_results[matchup_key][GAMES_KEY]
        hero1_winrate = hero1_wins / games
        hero2_winrate = hero2_wins / games
        matchup_winrates[matchup_key] = {hero1_winrate_key: hero1_winrate, hero2_winrate_key: hero2_winrate}


def calculate_combo_winrates():
    for combo_key in combo_results:
        wins = combo_results[combo_key][WINS_KEY]
        games = combo_results[combo_key][GAMES_KEY]
        combo_winrates[combo_key] = wins / games


def calculate_faction_winrates():
    radiant_wins = faction_results[RADIANT_KEY]
    dire_wins = faction_results[DIRE_KEY]
    games = radiant_wins + dire_wins
    faction_winrates[RADIANT_KEY] = radiant_wins / games
    faction_winrates[DIRE_KEY] = dire_wins / games


def finalize_winrates():
    for hero in hero_results:
        if hero not in hero_winrates:
            hero_winrates[hero] = 0.5
    for hero in hero_results:
        for enemy in hero_results:
            if hero != enemy:
                matchup_key = make_matchup_key(hero, enemy)
                if matchup_key not in matchup_winrates:
                    hero_winrate = hero_winrates[hero]
                    enemy_winrate = hero_winrates[enemy]
                    hero_matchup_winrate = hero_winrate / (hero_winrate + enemy_winrate)
                    enemy_matchup_winrate = enemy_winrate / (hero_winrate + enemy_winrate)
                    hero_winrate_key = make_winrate_key(hero)
                    enemy_winrate_key = make_winrate_key(enemy)
                    matchup_winrates[matchup_key] = {hero_winrate_key: hero_matchup_winrate, enemy_winrate_key: enemy_matchup_winrate}
    for hero in hero_results:
        for ally in hero_results:
            if hero != ally:
                combo_key = make_combo_key(hero, ally)
                if combo_key not in combo_winrates:
                    combo_winrates[combo_key] = (hero_winrates[hero] + hero_winrates[ally]) / 2


def calculate_winrates():
    calculate_hero_winrates()
    calculate_matchup_winrates()
    calculate_combo_winrates()
    calculate_faction_winrates()
    finalize_winrates()


def calculate_hero_advantages():
    for hero in hero_winrates:
        hero_advantages[hero] = hero_winrates[hero] - 0.5


def calculate_matchup_advantages():
    for matchup_key in matchup_winrates:
        hero1, hero2 = split_matchup_key(matchup_key)
        hero1_winrate_key = make_winrate_key(hero1)
        hero2_winrate_key = make_winrate_key(hero2)
        hero1_advantage_key = make_advantage_key(hero1)
        hero2_advantage_key = make_advantage_key(hero2)
        hero1_base_winrate = hero_winrates[hero1]
        hero2_base_winrate = hero_winrates[hero2]
        hero1_matchup_winrate = matchup_winrates[matchup_key][hero1_winrate_key]
        hero2_matchup_winrate = matchup_winrates[matchup_key][hero2_winrate_key]
        hero1_advantage, hero2_advantage = get_matchup_advantage(hero1_base_winrate, hero2_base_winrate, hero1_matchup_winrate,
                                                                 hero2_matchup_winrate)
        matchup_advantages[matchup_key] = {hero1_advantage_key: hero1_advantage, hero2_advantage_key: hero2_advantage}


def calculate_combo_advantages():
    for combo_key in combo_winrates:
        hero1, hero2 = split_combo_key(combo_key)
        hero1_base_winrate = hero_winrates[hero1]
        hero2_base_winrate = hero_winrates[hero2]
        combo_winrate = combo_winrates[combo_key]
        combo_advantages[combo_key] = get_combo_advantage(hero1_base_winrate, hero2_base_winrate, combo_winrate)


def calculate_faction_advantages():
    faction_advantages[RADIANT_KEY] = faction_winrates[RADIANT_KEY] - 0.5
    faction_advantages[DIRE_KEY] = faction_winrates[DIRE_KEY] - 0.5


def calculate_advantages():
    calculate_hero_advantages()
    calculate_matchup_advantages()
    calculate_combo_advantages()
    calculate_faction_advantages()


def assign_hero_values():
    for hero in hero_advantages:
        hero_values[hero] = hero_advantages[hero]


def assign_matchup_values():
    for matchup_key in matchup_advantages:
        hero1, hero2 = split_matchup_key(matchup_key)
        hero1_value_key = make_value_key(hero1)
        hero2_value_key = make_value_key(hero2)
        hero1_advantage_key = make_advantage_key(hero1)
        hero2_advantage_key = make_advantage_key(hero2)
        hero1_advantage = matchup_advantages[matchup_key][hero1_advantage_key]
        hero2_advantage = matchup_advantages[matchup_key][hero2_advantage_key]
        games = 0
        if matchup_key in matchup_results and GAMES_KEY in matchup_results[matchup_key]:
            games = matchup_results[matchup_key][GAMES_KEY]
        hero1_value = get_value(hero1_advantage, games)
        hero2_value = get_value(hero2_advantage, games)
        matchup_values[matchup_key] = {hero1_value_key: hero1_value, hero2_value_key: hero2_value}


def assign_combo_values():
    for combo_key in combo_advantages:
        advantage = combo_advantages[combo_key]
        games = 0
        if combo_key in combo_results and GAMES_KEY in combo_results[combo_key]:
            games = combo_results[combo_key][GAMES_KEY]
        value = get_value(advantage, games)
        combo_values[combo_key] = value


def assign_faction_values():
    faction_values[RADIANT_KEY] = faction_advantages[RADIANT_KEY]
    faction_values[DIRE_KEY] = faction_advantages[DIRE_KEY]


def assign_values():
    assign_hero_values()
    assign_matchup_values()
    assign_combo_values()
    assign_faction_values()


def record_hero(hero, win):
    if hero not in hero_results:
        hero_results[hero] = {WINS_KEY: 0, GAMES_KEY: 0}
    if win:
        hero_results[hero][WINS_KEY] += 1
    hero_results[hero][GAMES_KEY] += 1


def record_matchup(hero1, hero2, hero1_win):
    matchup_key = make_matchup_key(hero1, hero2)
    hero1_wins_key = make_wins_key(hero1)
    hero2_wins_key = make_wins_key(hero2)
    if matchup_key not in matchup_results:
        matchup_results[matchup_key] = {hero1_wins_key: 0, hero2_wins_key: 0, GAMES_KEY: 0}
    if hero1_win:
        matchup_results[matchup_key][hero1_wins_key] += 1
    else:
        matchup_results[matchup_key][hero2_wins_key] += 1
    matchup_results[matchup_key][GAMES_KEY] += 1


def record_combo(hero1, hero2, win):
    combo_key = make_combo_key(hero1, hero2)
    if combo_key not in combo_results:
        combo_results[combo_key] = {WINS_KEY: 0, GAMES_KEY: 0}
    if win:
        combo_results[combo_key][WINS_KEY] += 1
    combo_results[combo_key][GAMES_KEY] += 1


def record_faction(radiant_win):
    if radiant_win:
        faction_results[RADIANT_KEY] += 1
    else:
        faction_results[DIRE_KEY] += 1


def get_matchup_advantage(base_winrate1, base_winrate2, matchup_winrate1, matchup_winrate2):
    advantage1 = matchup_winrate1 - base_winrate1
    advantage2 = matchup_winrate2 - base_winrate2
    return advantage1, advantage2


def get_combo_advantage(base_winrate1, base_winrate2, combo_winrate):
    return 2 * combo_winrate - base_winrate1 - base_winrate2


def get_value(advantage, num_games):
    return advantage * get_confidence(num_games)


def get_confidence(num_games):
    if num_games == 0:
        return math.log(1)
    else:
        return math.log(num_games)
