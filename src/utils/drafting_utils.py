from openers.hero_indexes import hero_indexes
from utils.misc_utils import *
from utils.prediction_utils import *


def is_draft_complete(pick_index, pick_order):
    return pick_index >= len(pick_order)


def get_hero_score_with_team(hero, team):
    score = hero_values[hero]
    for ally in team:
        if hero != ally:
            combo_key = make_combo_key(hero, ally)
            score += combo_values[combo_key]
    return score


def get_hero_score_against_team(hero, team):
    score = hero_values[hero]
    for enemy in team:
        if hero != enemy:
            matchup_key = make_matchup_key(hero, enemy)
            matchup = matchup_values[matchup_key]
            hero_value_key = make_value_key(hero)
            enemy_value_key = make_value_key(enemy)
            score += matchup[hero_value_key] - matchup[enemy_value_key]
    return score


def get_itemized_scores(radiant, dire):
    itemized_hero_scores = {}
    for hero in heroes_not_in(radiant + dire):
        itemized_hero_scores[hero] = {}
        itemized_hero_scores[hero][VALUE_WITH_RADIANT_KEY] = get_hero_score_with_team(hero, radiant)
        itemized_hero_scores[hero][VALUE_AGAINST_RADIANT_KEY] = get_hero_score_against_team(hero, radiant)
        itemized_hero_scores[hero][VALUE_WITH_DIRE_KEY] = get_hero_score_with_team(hero, dire)
        itemized_hero_scores[hero][VALUE_AGAINST_DIRE_KEY] = get_hero_score_against_team(hero, dire)

        itemized_hero_scores[hero][TOTAL_VALUE_TO_RADIANT_KEY] = itemized_hero_scores[hero][VALUE_WITH_RADIANT_KEY] + \
                                                      itemized_hero_scores[hero][VALUE_AGAINST_DIRE_KEY]
        itemized_hero_scores[hero][TOTAL_VALUE_TO_DIRE_KEY] = itemized_hero_scores[hero][VALUE_AGAINST_RADIANT_KEY] + \
                                                      itemized_hero_scores[hero][VALUE_WITH_DIRE_KEY]
        itemized_hero_scores[hero][TOTAL_VALUE_KEY] = itemized_hero_scores[hero][VALUE_WITH_RADIANT_KEY] + \
                                                      itemized_hero_scores[hero][VALUE_AGAINST_RADIANT_KEY] + \
                                                      itemized_hero_scores[hero][VALUE_WITH_DIRE_KEY] + \
                                                      itemized_hero_scores[hero][VALUE_AGAINST_DIRE_KEY]
    return itemized_hero_scores


def get_naive_scores(ally_team, enemy_team, banned):
    hero_scores = {}

    for hero in heroes_not_in(ally_team + enemy_team + banned):
        hero_scores[hero] = hero_values[hero]

        for ally in ally_team:
            if hero != ally:
                hero_scores[hero] += combo_values[make_combo_key(hero, ally)]

        for enemy in enemy_team:
            if hero != enemy:
                matchup_key = make_matchup_key(hero, enemy)
                hero_value_key = make_value_key(hero)
                enemy_value_key = make_value_key(enemy)
                hero_scores[hero] += matchup_values[matchup_key][hero_value_key]
                hero_scores[hero] -= matchup_values[matchup_key][enemy_value_key]
    return hero_scores


def naive_best_pick(ally_team, enemy_team, banned):
    return best_scoring_hero(get_naive_scores(ally_team, enemy_team, banned))


def naive_worst_pick(ally_team, enemy_team, banned):
    return worst_scoring_hero(get_naive_scores(ally_team, enemy_team, banned))


def best_scoring_hero(hero_scores, exclude=[]):
    best_hero = None
    best_score = NEGATIVE_INFINITY
    for hero in hero_scores:
        if best_score < hero_scores[hero] and hero not in exclude:
            best_hero = hero
            best_score = hero_scores[hero]
    return best_hero


def worst_scoring_hero(hero_scores):
    worst_hero = None
    worst_score = POSITIVE_INFINITY
    for hero in hero_scores:
        if worst_score > hero_scores[hero]:
            worst_hero = hero
            worst_score = hero_scores[hero]
    return worst_hero


def get_turn_and_action(pick_index, pick_order):
    pick = pick_order[pick_index]
    acting_team_key = pick[TEAM_KEY]
    action = pick[ACTION_KEY]
    radiant_turn = acting_team_key == RADIANT_KEY
    is_pick = action == PICK_KEY
    return radiant_turn, is_pick


def heroes_not_in(heroes):
    out_heroes = []
    for hero in hero_indexes:
        if hero not in heroes:
            out_heroes.append(hero)
    return out_heroes


def scores_to_winrates(radiant_score, dire_score):
    return score_difference_to_winrate(radiant_score - dire_score)


def score_difference_to_winrate(difference):
    radiant_winrate = normalize(difference, PREDICTION_DIFFERENCE_SCALE, -1 * PREDICTION_DIFFERENCE_SCALE,
                                PERCENTAGE_MAX, PERCENTAGE_MIN)
    if radiant_winrate > PERCENTAGE_MAX:
        radiant_winrate = PERCENTAGE_MAX
        dire_winrate = PERCENTAGE_MIN
    elif radiant_winrate < PERCENTAGE_MIN:
        radiant_winrate = PERCENTAGE_MIN
        dire_winrate = PERCENTAGE_MAX
    else:
        dire_winrate = PERCENTAGE_MAX - radiant_winrate
    return radiant_winrate, dire_winrate


def hero_scores_to_winrates(hero_scores, is_radiant):
    for hero in hero_scores:
        radiant_winrate, dire_winrate = score_difference_to_winrate(hero_scores[hero])
        if is_radiant:
            hero_scores[hero] = radiant_winrate
        else:
            hero_scores[hero] = dire_winrate
    return hero_scores

