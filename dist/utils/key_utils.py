from main.constants import *


def is_matchup_key(key):
    return len(split_matchup_key(key)) == 2


def is_combo_key(key):
    return len(split_combo_key(key)) == 2


def make_matchup_key_unordered(hero1, hero2):
    return hero1 + MATCHUP_INFIX + hero2


def make_combo_key_unordered(hero1, hero2):
    return hero1 + COMBO_INFIX + hero2


def make_matchup_key(hero1, hero2):
    return make_key(hero1, hero2, MATCHUP_INFIX)


def make_combo_key(hero1, hero2):
    return make_key(hero1, hero2, COMBO_INFIX)


def split_matchup_key(matchup_key):
    heroes = matchup_key.split(MATCHUP_INFIX)
    return heroes[0], heroes[1]


def split_combo_key(combo_key):
    heroes = combo_key.split(COMBO_INFIX)
    return heroes[0], heroes[1]


def make_wins_key(hero):
    return hero + WINS_SUFFIX


def make_winrate_key(hero):
    return hero + WINRATE_SUFFIX


def make_advantage_key(hero):
    return hero + ADVANTAGE_SUFFIX


def make_value_key(hero):
    return hero + VALUE_SUFFIX


def make_key(hero1, hero2, infix):
    if hero1 < hero2:
        return hero1 + infix + hero2
    else:
        return hero2 + infix + hero1
