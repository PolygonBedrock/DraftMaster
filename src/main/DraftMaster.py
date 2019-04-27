import sys
import ctypes
from utils.monte_carlo import *
from openers.value_data import *
from utils.key_utils import *
from utils.misc_utils import *

# Welcome
print(MSG_STARTUP)


def get_action_and_team(index_offset=0):
    pick = pick_order[pick_index + index_offset]
    team = pick[TEAM_KEY]
    action = pick[ACTION_KEY]
    radiant_turn = team == RADIANT_KEY
    is_pick = action == PICK_KEY
    return radiant_turn, is_pick


def show_teams():
    table = new_table()
    field_names = [TEAM_KEY.title()]
    radiant_len = get_len(radiant)
    dire_len = get_len(dire)
    max_len = max(radiant_len, dire_len)
    for i in range(1, max_len + 1):
        field_names.append(i)
    table.field_names = field_names
    if radiant:
        table.add_row([RADIANT_KEY.title()] + radiant + [MSG_EMPTY] * (max_len - radiant_len))
    if dire:
        table.add_row([DIRE_KEY.title()] + dire + [MSG_EMPTY] * (max_len - dire_len))
    if radiant or dire:
        show_table(table, ALIGN_CENTER)
    if banned:
        print(BANNED_KEY.title() + MSG_COLON_INFIX + MSG_COMMA_SEPARATOR.join(banned))


def show_scores():
    if radiant or dire:
        new_line()
        table = new_table()
        table.field_names = [MSG_RADIANT_WINRATE, MSG_DIRE_WINRATE]
        radiant_score, dire_score = predict(radiant, dire)
        radiant_winrate, dire_winrate = scores_to_winrates(radiant_score, dire_score)
        table.add_row([format_num(radiant_winrate) + MSG_PERCENT, format_num(dire_winrate) + MSG_PERCENT])
        show_table(table, ALIGN_CENTER)


def show_display():
    line_break()
    if context == CONTEXT_MAIN:
        print(MSG_MAIN_MENU)
    elif context == CONTEXT_ALL_PICK_BANNING:
        show_teams()
        show_scores()
        print(MSG_NEWLINE + MSG_ALL_PICK_BANNING)
    elif context == CONTEXT_PICK_BAN:
        show_teams()
        show_scores()
        if pick_index < get_len(pick_order):
            radiant_turn, is_pick = get_action_and_team()
            if radiant_turn:
                if is_pick:
                    print(MSG_NEWLINE + MSG_RADIANT_TURN_TO_PICK)
                else:
                    print(MSG_NEWLINE + MSG_RADIANT_TURN_TO_BAN)
            else:
                if is_pick:
                    print(MSG_NEWLINE + MSG_DIRE_TURN_TO_PICK)
                else:
                    print(MSG_NEWLINE + MSG_DIRE_TURN_TO_BAN)
        else:
            print(MSG_NEWLINE + MSG_DRAFT_COMPLETE)


def get_context_commands(in_context):
    if in_context == CONTEXT_MAIN:
        return CONTEXT_MAIN_COMMANDS
    if in_context == CONTEXT_ALL_PICK_BANNING:
        return CONTEXT_ALL_PICK_BANNING_COMMANDS
    if in_context == CONTEXT_PICK_BAN:
        return CONTEXT_PICK_BAN_COMMANDS


def set_context(in_context):
    global context
    global context_commands
    context = in_context
    context_commands = get_context_commands(in_context)


def bad_command():
    print(MSG_BAD_COMMAND)


def context_valid(command):
    if CONTEXT_IMPLICIT_SEARCH[context] and search_hero(command):
        return True
    for context_command in context_commands:
        if context_command in command:
            return True
    return False


def search_hero(search):
    if not search:
        return None
    search = scrub_string(search, [])
    for nickname, hero in HERO_NICKNAMES.items():
        if nickname.lower() == search.lower():
            return hero
    for hero, index in hero_indexes.items():
        for hero_subname in hero.split(' '):
            if hero_subname.lower().startswith(search.lower()):
                return hero
    return None


def extract_arg_team(command):
    if ARG_RADIANT in command:
        team = ARG_RADIANT
        command = scrub_string(command, [ARG_RADIANT])
    elif ARG_DIRE in command:
        team = ARG_DIRE
        command = scrub_string(command, [ARG_DIRE])
    else:
        team = None
    return team, command


def extract_arg_number(command):
    out_command = ""
    num_str = ""
    num = None
    for char in command:
        if char.isdigit():
            num_str += char
        else:
            out_command += char
    if num_str:
        num = float(num_str)
    return num, out_command


def execute_select(command):
    global pick_index
    if pick_index >= get_len(pick_order) and context != CONTEXT_ALL_PICK_BANNING:
        print(MSG_CANNOT_SELECT_DRAFT_COMPLETE)
        return
    search = scrub_string(command, [CMD_SELECT])
    hero = search_hero(search)
    if hero in radiant or hero in dire or hero in banned:
        print(MSG_HERO_UNAVAILABLE + hero)
    elif hero is None:
        print(MSG_HERO_NOT_FOUND + search)
    else:
        message = MSG_EMPTY
        if context == CONTEXT_ALL_PICK_BANNING:
            banned.append(hero)
            message = MSG_BAN + hero
        elif context == CONTEXT_PICK_BAN:
            radiant_turn, is_pick = get_action_and_team()
            if radiant_turn:
                if is_pick:
                    radiant.append(hero)
                    message = MSG_RADIANT_PICK + hero
                else:
                    banned.append(hero)
                    message = MSG_RADIANT_BAN + hero
            else:
                if is_pick:
                    dire.append(hero)
                    message = MSG_DIRE_PICK + hero
                else:
                    banned.append(hero)
                    message = MSG_DIRE_BAN + hero
            pick_index += 1
        print(message)
        history.append(message)


def execute_back():
    global radiant
    global dire
    global banned
    global history
    global pick_index
    message = MSG_EMPTY
    if not radiant and not dire and not banned or (pick_index == 0 and context != CONTEXT_ALL_PICK_BANNING):
        print(MSG_CANNOT_UNDO)
        return
    if context == CONTEXT_ALL_PICK_BANNING:
        hero = get_last_from_list(banned)
        banned = banned[:-1]
        history = history[:-1]
        message = MSG_UNDONE + hero.title() + MSG_SPACE + BAN_KEY
    elif context == CONTEXT_PICK_BAN:
        radiant_turn, is_pick = get_action_and_team(-1)
        if radiant_turn:
            team = RADIANT_KEY
            if is_pick:
                action = PICK_KEY
                hero = get_last_from_list(radiant)
                radiant = radiant[:-1]
            else:
                action = BAN_KEY
                hero = get_last_from_list(banned)
                banned = banned[:-1]
        else:
            team = DIRE_KEY
            if is_pick:
                action = PICK_KEY
                hero = get_last_from_list(dire)
                dire = dire[:-1]
            else:
                action = BAN_KEY
                hero = get_last_from_list(banned)
                banned = banned[:-1]
        history = history[:-1]
        message = MSG_UNDONE + team.title() + MSG_SPACE + action + MSG_SPACE + hero
        pick_index -= 1
    print(message)


def execute_history():
    print(MSG_HISTORY)
    for entry in history:
        print(MSG_INDENT + entry)


def explain_combos(team_name, team):
    if get_len(team) >= 2:
        table = new_table()
        table.field_names = [team_name.title() + MSG_SPACE + COMBOS_KEY.title()] + team
        for hero in team:
            row = [hero]
            for ally in team:
                if hero != ally:
                    combo_key = make_combo_key(hero, ally)
                    value = combo_values[combo_key]
                    row.append(format_num(value))
                else:
                    value = hero_values[hero]
                    row.append(format_num(value))
            table.add_row(row)
        show_table(table, ALIGN_CENTER)
        new_line()


def explain_matchups():
    if radiant and dire:
        table = new_table()
        table.field_names = [MATCHUPS_KEY.title()] + dire

        for radiant_hero in radiant:
            row = [radiant_hero]
            for dire_hero in dire:
                matchup_key = make_matchup_key(radiant_hero, dire_hero)
                radiant_value_key = make_value_key(radiant_hero)
                dire_value_key = make_value_key(dire_hero)
                matchup = matchup_values[matchup_key]
                radiant_value = matchup[radiant_value_key]
                dire_value = matchup[dire_value_key]
                value = format_num(radiant_value - dire_value)
                row.append(value)
            table.add_row(row)
        show_table(table, ALIGN_CENTER)
        print(MSG_MATCHUPS_HINT)
        new_line()


def execute_explain():
    print(MSG_EXPLAIN_VALUES)
    explain_combos(ARG_RADIANT, radiant)
    explain_combos(ARG_DIRE, dire)
    explain_matchups()


def execute_counters(command):
    num_options, command = extract_arg_number(command)
    search = scrub_string(command, [CMD_COUNTERS])
    hero = search_hero(search)
    matchup_scores = {}
    if hero is not None:
        for enemy in hero_indexes:
            if enemy != hero:
                matchup_key = make_matchup_key(hero, enemy)
                hero_value_key = make_value_key(hero)
                enemy_value_key = make_value_key(enemy)
                matchup = matchup_values[matchup_key]
                hero_value = matchup[hero_value_key]
                enemy_value = matchup[enemy_value_key]
                matchup_scores[matchup_key] = (hero_value - enemy_value) * -1
        if num_options:
            show_options(matchup_scores, num_options)
        else:
            show_options(matchup_scores)
    else:
        print(MSG_HERO_NOT_FOUND + hero)


def execute_combos(command):
    num_options, command = extract_arg_number(command)
    search = scrub_string(command, [CMD_COMBOS])
    hero = search_hero(search)
    combo_scores = {}
    if hero is not None:
        for ally in hero_indexes:
            if ally != hero:
                combo_key = make_combo_key(hero, ally)
                combo_value = combo_values[combo_key]
                combo_scores[combo_key] = combo_value
        if num_options:
            show_options(combo_scores, num_options)
        else:
            show_options(combo_scores)
    else:
        print(MSG_HERO_NOT_FOUND + hero)


def execute_done(command):
    global pick_order
    team, command = extract_arg_team(command)
    if team is None:
        print(MSG_BAD_DONE)
        return
    elif team == ARG_RADIANT:
        pick_order = ALL_PICK_ORDER_RADIANT
    elif team == ARG_DIRE:
        pick_order = ALL_PICK_ORDER_DIRE
    set_context(CONTEXT_PICK_BAN)
    print(MSG_BANNING_COMPLETE)


def parse_new(command):
    if ARG_ALL_PICK in command:
        return ARG_ALL_PICK
    elif ARG_CAPTAINS_MODE in command:
        return ARG_CAPTAINS_MODE


def execute_new(command):
    global context
    global pick_order
    global pick_index
    mode = parse_new(command)
    if mode == ARG_ALL_PICK:
        set_context(CONTEXT_ALL_PICK_BANNING)
        print(MSG_NEW_ALL_PICK)
    elif mode == ARG_CAPTAINS_MODE:
        pick_order = CAPTAINS_MODE_ORDER
        set_context(CONTEXT_PICK_BAN)
        print(MSG_NEW_CAPTAINS)
    else:
        print(MSG_BAD_NEW)
        return
    del radiant[:]
    del dire[:]
    del banned[:]
    del history[:]
    pick_index = 0


def parse_options(command):
    worst_case = False
    best_case = False
    if ARG_GREEDY in command:
        best_case = True
    if ARG_ROBUST in command:
        worst_case = True
        best_case = True
    if ARG_SAFE in command:
        worst_case = True
    if not worst_case and not best_case:
        worst_case = True
        best_case = True
    return best_case, worst_case


def show_options(hero_scores, num_options=DEFAULT_OPTIONS_COUNT, reverse_sort=True):
    max_score = max(hero_scores.values())
    min_score = min(hero_scores.values())
    for hero in hero_scores:
        score = hero_scores[hero]
        hero_scores[hero] = normalize(score, max_score, min_score, 1, -1)
    current_num = 0
    table = new_table()
    table.field_names = [HERO_KEY.title(), VALUE_KEY.title()]
    for hero, score in sorted(hero_scores.items(), key=lambda kv: kv[1], reverse=reverse_sort):
        current_num += 1
        if current_num > num_options:
            break
        table.add_row([hero, format_num(score)])
    show_table(table)
    new_line()


def execute_options(command):
    if pick_index >= get_len(pick_order):
        print(MSG_DRAFT_COMPLETE)
        return
    print(MSG_THINKING)
    num_options, command = extract_arg_number(command)
    radiant_turn, is_pick = get_action_and_team()
    best_case, worst_case = parse_options(command)
    hero_scores = {}
    if best_case:
        best_case_hero_scores = monte_carlo(radiant, dire, banned, MONTE_CARLO_DEPTH, pick_index, pick_order,
                                            radiant_turn)
        hero_scores = marry_dicts(hero_scores, best_case_hero_scores)
    if worst_case:
        worst_case_hero_scores = monte_carlo(radiant, dire, banned, MONTE_CARLO_DEPTH, pick_index, pick_order,
                                             not radiant_turn)
        hero_scores = marry_dicts(hero_scores, worst_case_hero_scores)
    if num_options:
        show_options(hero_scores, num_options)
    else:
        show_options(hero_scores)


def execute_search(command):
    search = scrub_string(command, [CMD_SEARCH])
    print(MSG_SEARCH_FOR + search)
    for nickname, hero in HERO_NICKNAMES.items():
        if search.lower() == nickname.lower():
            print(hero)
    for hero, index in hero_indexes.items():
        for hero_subname in hero.split(' '):
            if hero_subname.lower().startswith(search.lower()):
                print(hero)


def execute_help():
    print(HELP_HINT)
    table = new_table()
    table.field_names = [MSG_COMMAND, MSG_DESCRIPTION]
    for cmd in context_commands:
        if cmd:
            table.add_row([cmd, HELP_MAP[cmd]])
    show_table(table)
    new_line()


def execute_quit():
    print(MSG_QUIT)
    sys.exit()


def run_command(command):
    clear_screen()
    print(PROMPT + command + MSG_NEWLINE)
    if context_valid(command):
        if CMD_SELECT in command:
            execute_select(command)
        elif CMD_BACK in command:
            execute_back()
        elif CMD_HISTORY in command:
            execute_history()
        elif CMD_EXPLAIN in command:
            execute_explain()
        elif CMD_COUNTERS in command:
            execute_counters(command)
        elif CMD_COMBOS in command:
            execute_combos(command)
        elif CMD_DONE in command:
            execute_done(command)
        elif CMD_NEW in command:
            execute_new(command)
        elif CMD_OPTIONS in command:
            execute_options(command)
        elif CMD_SEARCH in command:
            execute_search(command)
        elif CMD_HELP in command:
            execute_help()
        elif CMD_QUIT in command:
            execute_quit()
        else:
            if CMD_SELECT in context_commands:
                execute_select(command)
            else:
                print(MSG_BAD_COMMAND)
    else:
        print(MSG_BAD_CONTEXT)


def main():
    command = CMD_EMPTY
    while True:
        if command != CMD_EMPTY:
            show_display()
        command = input(PROMPT)
        if command == CMD_EMPTY:
            pass
        else:
            run_command(command)


def startup():
    ctypes.windll.kernel32.SetConsoleTitleW(APP_FULL_NAME)
    user32 = ctypes.WinDLL(WIN_DLL)
    user32.ShowWindow(user32.GetForegroundWindow(), WIN_MAXIMIZE)


# Globals
radiant = []
dire = []
banned = []
history = []
pick_index = 0
pick_order = None
context = CONTEXT_MAIN
context_commands = CONTEXT_MAIN_COMMANDS

# Start
startup()
clear_screen()
print(MSG_WELCOME)
main()
