import itertools
from utils.key_utils import *
from openers.value_data import *
from openers.costs import *


def get_score(heroes_subscore, matchup_subscore, combo_subscore, faction_subscore, cost_subscore, heroes_coefficient,
              matchup_coefficient, combo_coefficient, faction_coefficient, cost_coefficient):
    return heroes_subscore * heroes_coefficient + matchup_subscore * matchup_coefficient + \
           combo_subscore * combo_coefficient + faction_subscore * faction_coefficient + \
           abs(cost_subscore) * cost_coefficient


def predict(radiant, dire, heroes_coefficient=PREDICTION_HEROES_COEFFICIENT,
            matchup_coefficient=PREDICTION_MATCHUP_COEFFICIENT, combo_coefficient=PREDICTION_COMBO_COEFFICIENT,
            faction_coefficient=PREDICTION_FACTION_COEFFICIENT, cost_coefficient=PREDICTION_COST_COEFFICIENT):
    radiant_heroes_subscore = 0
    dire_heroes_subscore = 0
    radiant_matchup_subscore = 0
    dire_matchup_subscore = 0
    radiant_combo_subscore = 0
    dire_combo_subscore = 0
    radiant_faction_subscore = faction_values[RADIANT_KEY]
    dire_faction_subscore = faction_values[DIRE_KEY]
    radiant_cost_subscore = 0
    dire_cost_subscore = 0

    for hero in radiant:
        radiant_heroes_subscore += hero_values[hero]
        radiant_cost_subscore += costs[hero]

    for hero in dire:
        dire_heroes_subscore += hero_values[hero]
        dire_cost_subscore += costs[hero]

    for radiantHero in radiant:
        for direHero in dire:
            matchup_key = make_matchup_key(radiantHero, direHero)
            radiant_hero_value_key = make_value_key(radiantHero)
            dire_hero_value_key = make_value_key(direHero)
            radiant_matchup_subscore += matchup_values[matchup_key][radiant_hero_value_key]
            dire_matchup_subscore += matchup_values[matchup_key][dire_hero_value_key]

    for combo in itertools.combinations(radiant, 2):
        hero1 = combo[0]
        hero2 = combo[1]
        combo_key = make_combo_key(hero1, hero2)
        radiant_combo_subscore += combo_values[combo_key]

    for combo in itertools.combinations(dire, 2):
        hero1 = combo[0]
        hero2 = combo[1]
        combo_key = make_combo_key(hero1, hero2)
        dire_combo_subscore += combo_values[combo_key]

    radiant_score = get_score(radiant_heroes_subscore, radiant_matchup_subscore, radiant_combo_subscore,
                              radiant_faction_subscore, radiant_cost_subscore, heroes_coefficient, matchup_coefficient,
                              combo_coefficient, faction_coefficient, cost_coefficient)
    dire_score = get_score(dire_heroes_subscore, dire_matchup_subscore, dire_combo_subscore, dire_faction_subscore,
                           dire_cost_subscore, heroes_coefficient, matchup_coefficient, combo_coefficient,
                           faction_coefficient, cost_coefficient)
    return radiant_score, dire_score
