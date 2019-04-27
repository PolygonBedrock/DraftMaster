from openers.hero_indexes import *
import copy
import os
import platform
from prettytable import PrettyTable


def scores_to_winrates(radiant_score, dire_score):
    return score_difference_to_winrate(radiant_score - dire_score)


def score_difference_to_winrate(difference):
    radiant_winrate = normalize(difference, PREDICTION_DIFFERENCE_SCALE, -1 * PREDICTION_DIFFERENCE_SCALE,
                                PERCENTAGE_MAX, PERCENTAGE_MIN)
    if radiant_winrate > PERCENTAGE_MAX:
        radiant_winrate = PERCENTAGE_MAX
        dire_winrate = PERCENTAGE_MIN
    else:
        dire_winrate = PERCENTAGE_MAX - radiant_winrate
    return radiant_winrate, dire_winrate


def new_line():
    print(MSG_EMPTY)


def show_table(table, align=ALIGN_LEFT):
    table.align = align
    table.left_padding_width = 0
    print(table)


def new_table():
    table = PrettyTable()
    table.border = False
    table.align = "l"
    return table


def get_len(in_list):
    if not in_list:
        return 0
    else:
        return len(in_list)


def get_last_from_list(from_list):
    if len(from_list) == 1:
        return from_list[0]
    else:
        return from_list[-1]


def normalize(num, in_max, in_min, out_max, out_min):
    return ((num - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min


def marry_dicts(dict1, dict2):
    out_dict = {}
    for key in dict1:
        if key in dict2:
            out_dict[key] = dict1[key] + dict2[key]
        else:
            out_dict[key] = dict1[key]
    for key in dict2:
        if key not in out_dict:
            out_dict[key] = dict2[key]
    return out_dict


def line_break():
    columns = 0
    try:
        columns, rows = os.get_terminal_size(0)
    except OSError:
        try:
            columns, rows = os.get_terminal_size(1)
        except OSError:
            pass
    if columns:
        out = MSG_LINE_BREAK * columns
        print(MSG_NEWLINE + out)


def format_num(num):
    return str(round(num, DECIMAL_ROUND))


def scrub_string(command, replacements):
    for replacement in replacements:
        command = command.replace(replacement, "")
    command = " ".join(command.split())
    return command.strip()


def heroes_not_in(heroes):
    out_heroes = []
    for hero in hero_indexes:
        if hero not in heroes:
            out_heroes.append(hero)
    return out_heroes


def copy_list_with_hero(in_list, hero):
    if not in_list:
        return [hero]
    return copy.deepcopy(in_list) + [hero]


def get_turn_and_action(pick_index, pick_order):
    pick = pick_order[pick_index]
    acting_team_key = pick[TEAM_KEY]
    action = pick[ACTION_KEY]
    radiant_turn = acting_team_key == RADIANT_KEY
    is_pick = action == PICK_KEY
    return radiant_turn, is_pick


def clear_screen():
    try:
        if PLATFORM_WINDOWS in platform.platform():
            os.system("cls")
        else:
            os.system("clear")
    except OSError:
        pass
