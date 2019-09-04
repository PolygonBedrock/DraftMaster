from openers.games_data import games
from openers.hero_indexes import hero_indexes
from utils.file_utils import *
from utils.advantage_utils import *
import itertools

elements_to_games = {}

hero_values = {}
matchup_values = {}
combo_values = {}
faction_values = {}

category_keys = [FACTIONS_KEY, MATCHUPS_KEY, COMBOS_KEY, HEROES_KEY]


def init():
    for hero in hero_indexes:
        elements_to_games[hero] = []
        data[HEROES_KEY][hero] = 0

    for hero_pair in itertools.combinations(hero_indexes, 2):
        combo_key = make_combo_key(hero_pair[0], hero_pair[1])
        matchup_key = make_matchup_key(hero_pair[0], hero_pair[1])
        hero1_value_key = make_value_key(hero_pair[0])
        hero2_value_key = make_value_key(hero_pair[1])
        elements_to_games[combo_key] = []
        elements_to_games[matchup_key] = []
        data[COMBOS_KEY][combo_key] = 0
        data[MATCHUPS_KEY][matchup_key] = {hero1_value_key: 0, hero2_value_key: 0}

    elements_to_games[RADIANT_KEY] = []
    elements_to_games[DIRE_KEY] = []
    data[FACTIONS_KEY][RADIANT_KEY] = 0
    data[FACTIONS_KEY][DIRE_KEY] = 0

    for game in games:
        elements_to_games[RADIANT_KEY].append(game)
        elements_to_games[DIRE_KEY].append(game)
        radiant = game[RADIANT_KEY]
        dire = game[DIRE_KEY]
        for hero in radiant:
            elements_to_games[hero].append(game)
            for ally in radiant:
                if hero != ally:
                    combo_key = make_combo_key(hero, ally)
                    elements_to_games[combo_key].append(game)
            for enemy in dire:
                matchup_key = make_matchup_key(hero, enemy)
                elements_to_games[matchup_key].append(game)
        for hero in dire:
            elements_to_games[hero].append(game)
            for ally in dire:
                if hero != ally:
                    combo_key = make_combo_key(hero, ally)
                    elements_to_games[combo_key].append(game)

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


def get_roster_score(radiant, dire):
    hero_value = 0
    combo_value = 0
    matchup_value = 0
    faction_value = 0

    for hero in radiant:
        hero_value += data[HEROES_KEY][hero]
        for ally in radiant:
            if hero != ally:
                combo_key = make_combo_key(hero, ally)
                combo_value += data[COMBOS_KEY][combo_key]
        for enemy in dire:
            matchup_key = make_matchup_key(hero, enemy)
            hero_value_key = make_value_key(hero)
            matchup_value += data[MATCHUPS_KEY][matchup_key][hero_value_key]

    for hero in dire:
        hero_value -= data[HEROES_KEY][hero]
        for ally in dire:
            if hero != ally:
                combo_key = make_combo_key(hero, ally)
                combo_value -= data[COMBOS_KEY][combo_key]
        for enemy in radiant:
            matchup_key = make_matchup_key(hero, enemy)
            hero_value_key = make_value_key(hero)
            matchup_value -= data[MATCHUPS_KEY][matchup_key][hero_value_key]

    faction_value += data[FACTIONS_KEY][RADIANT_KEY]
    faction_value -= data[FACTIONS_KEY][DIRE_KEY]

    return hero_value + combo_value + matchup_value + faction_value


def predict(radiant, dire):
    score = get_roster_score(radiant, dire)
    if score > 0:
        return RADIANT_KEY
    elif score < 0:
        return DIRE_KEY
    else:
        return None


def get_total_accurately_predicted_games(selected_games=games):
    correct_prediction_count = 0
    for game in selected_games:
        radiant = game[RADIANT_KEY]
        dire = game[DIRE_KEY]
        winner = game[WINNER_KEY]
        if predict(radiant, dire) == winner:
            correct_prediction_count += 1
    return correct_prediction_count


def get_prediction_accuracy(selected_games=games):
    return get_total_accurately_predicted_games(selected_games) / len(selected_games)


def tune_single_value_one_direction(catagory_key, element_key, tune_value):
    element_games = elements_to_games[element_key]
    last_total_correct_games = get_total_accurately_predicted_games(element_games)
    improved = False

    if catagory_key == MATCHUPS_KEY:
        hero1, hero2 = split_matchup_key(element_key)
        hero1_value = make_value_key(hero1)
        hero2_value = make_value_key(hero2)
        tune_value = tune_value / 2

    while True:
        if catagory_key == MATCHUPS_KEY:
            data[catagory_key][element_key][hero1_value] += tune_value
            data[catagory_key][element_key][hero2_value] -= tune_value
        else:
            data[catagory_key][element_key] += tune_value

        current_total_correct_games = get_total_accurately_predicted_games(element_games)

        if current_total_correct_games > last_total_correct_games:
            last_total_correct_games = current_total_correct_games
            improved = True
        else:
            if catagory_key == MATCHUPS_KEY:
                data[catagory_key][element_key][hero1_value] -= tune_value
                data[catagory_key][element_key][hero2_value] += tune_value
            else:
                data[catagory_key][element_key] -= tune_value
            break
    return improved


def get_tune_value(element_key):
    element_games = elements_to_games[element_key]
    min_delta = POSITIVE_INFINITY
    for game in element_games:
        radiant = game[RADIANT_KEY]
        dire = game[DIRE_KEY]
        min_delta = min(abs(get_roster_score(radiant, dire)), min_delta)
        if min_delta == 0:
            break
    return min_delta + 1


def tune_single_value(category_key, element_key):
    improved = False
    tune_value = get_tune_value(element_key)
    if tune_single_value_one_direction(category_key, element_key, tune_value):
        improved |= True
    else:
        improved |= tune_single_value_one_direction(category_key, element_key, -tune_value)
    print(element_key + ": " + str(data[category_key][element_key]))
    return improved


def tune_all_values():
    improved = True
    while improved:
        improved = False
        for category_key in category_keys:
            for element_key in data[category_key]:
                improved |= tune_single_value(category_key, element_key)


def halve_values():
    for category_key in category_keys:
        for element_key in data[category_key]:
            if category_key == MATCHUPS_KEY:
                hero, enemy = split_matchup_key(element_key)
                hero_value_key = make_value_key(hero)
                enemy_value_key = make_value_key(enemy)
                data[category_key][element_key][hero_value_key] /= 2
                data[category_key][element_key][enemy_value_key] /= 2
            else:
                data[category_key][element_key] /= 2


print("Setting up...")
init()

print("Calculating winrates...")
calculate_winrates()

print("Calculating advantages...")
calculate_advantages()

print("Assigning values...")
assign_values()

print("Tuning values...")
tune_all_values()

print("Saving file...")
save_to_file(data, VALUES_FILE)

print("Final Accuracy: " + str(get_prediction_accuracy()))

