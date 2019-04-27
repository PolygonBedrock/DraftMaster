from utils.prediction_utils import *
from utils.misc_utils import *


def best_naive_radiant_pick(radiant, dire, banned):
    best_score = float("-inf")
    best_hero = None
    for hero in heroes_not_in(radiant + dire + banned):
        new_radiant = copy_list_with_hero(radiant, hero)
        radiant_score, dire_score = predict(new_radiant, dire)
        if radiant_score > best_score:
            best_score = radiant_score
            best_hero = hero
    return best_hero


def best_naive_dire_pick(radiant, dire, banned):
    best_score = float("-inf")
    best_hero = None
    for hero in heroes_not_in(radiant + dire + banned):
        new_dire = copy_list_with_hero(dire, hero)
        radiant_score, dire_score = predict(radiant, new_dire)
        if dire_score > best_score:
            best_score = radiant_score
            best_hero = hero
    return best_hero


def worst_naive_radiant_pick(radiant, dire, banned):
    worst_score = float("inf")
    worst_hero = None
    for hero in heroes_not_in(radiant + dire + banned):
        new_radiant = copy_list_with_hero(radiant, hero)
        radiant_score, dire_score = predict(new_radiant, dire)
        if radiant_score < worst_score:
            worst_score = radiant_score
            worst_hero = hero
    return worst_hero


def worst_naive_dire_pick(radiant, dire, banned):
    worst_score = float("inf")
    worst_hero = None
    for hero in heroes_not_in(radiant + dire + banned):
        new_dire = copy_list_with_hero(dire, hero)
        radiant_score, dire_score = predict(radiant, new_dire)
        if dire_score < worst_score:
            worst_score = radiant_score
            worst_hero = hero
    return worst_hero


def best_naive_radiant_ban(radiant, dire, banned):
    return best_naive_dire_pick(radiant, dire, banned)


def best_naive_dire_ban(radiant, dire, banned):
    return best_naive_radiant_pick(radiant, dire, banned)


def worst_naive_radiant_ban(radiant, dire, banned):
    return worst_naive_dire_pick(radiant, dire, banned)


def worst_naive_dire_ban(radiant, dire, banned):
    return worst_naive_radiant_pick(radiant, dire, banned)


def finish_draft(radiant, dire, banned, pick_index, pick_order, best_radiant):
    new_radiant = copy.deepcopy(radiant)
    new_dire = copy.deepcopy(dire)
    new_banned = copy.deepcopy(banned)
    for currentPickIndex in range(pick_index, len(pick_order)):
        radiant_turn, is_pick = get_turn_and_action(currentPickIndex, pick_order)
        if best_radiant:
            if radiant_turn:
                if is_pick:
                    pick = best_naive_radiant_pick(new_radiant, new_dire, new_banned)
                    new_radiant.append(pick)
                else:
                    ban = best_naive_radiant_ban(new_radiant, new_dire, new_banned)
                    new_banned.append(ban)
            else:
                if is_pick:
                    pick = worst_naive_dire_pick(new_radiant, new_dire, new_banned)
                    new_dire.append(pick)
                else:
                    ban = worst_naive_dire_ban(new_radiant, new_dire, new_banned)
                    new_banned.append(ban)
        else:
            if radiant_turn:
                if is_pick:
                    pick = worst_naive_radiant_pick(new_radiant, new_dire, new_banned)
                    new_radiant.append(pick)
                else:
                    ban = worst_naive_radiant_ban(new_radiant, new_dire, new_banned)
                    new_banned.append(ban)
            else:
                if is_pick:
                    pick = worst_naive_dire_pick(new_radiant, new_dire, new_banned)
                    new_dire.append(pick)
                else:
                    ban = worst_naive_dire_ban(new_radiant, new_dire, new_banned)
                    new_banned.append(ban)

    return predict(new_radiant, new_dire)


def monte_carlo_subsearch(radiant, dire, banned, depth, pick_index, pick_order, best_radiant):
    if pick_index >= len(pick_order):
        return predict(radiant, dire)
    radiant_turn, is_pick = get_turn_and_action(pick_index, pick_order)
    if depth > 0:
        radiant_score = 0
        dire_score = 0
        for hero in heroes_not_in(radiant + dire + banned):
            if is_pick:
                if radiant_turn:
                    new_radiant = copy_list_with_hero(radiant, hero)
                    radiant_hero_score, dire_hero_score = monte_carlo_subsearch(new_radiant, dire, banned, depth - 1,
                                                                                pick_index + 1, pick_order,
                                                                                best_radiant)
                else:
                    new_dire = copy_list_with_hero(dire, hero)
                    radiant_hero_score, dire_hero_score = monte_carlo_subsearch(radiant, new_dire, banned, depth - 1,
                                                                                pick_index + 1, pick_order,
                                                                                best_radiant)
            else:
                new_banned = copy_list_with_hero(banned, hero)
                radiant_hero_score, dire_hero_score = monte_carlo_subsearch(radiant, dire, new_banned, depth - 1,
                                                                            pick_index + 1, pick_order, best_radiant)
            radiant_score += radiant_hero_score
            dire_score += dire_hero_score
        return radiant_score, dire_score
    else:
        return finish_draft(radiant, dire, banned, pick_index, pick_order, best_radiant)


def monte_carlo(radiant, dire, banned, depth, pick_index, pick_order, best_radiant):
    if depth <= 0:
        print(MSG_BAD_MONTE_CARLO_DEPTH)
        return
    if pick_index >= len(pick_order):
        print(MSG_BAD_MONTE_CARLO_COMPLETE)
        return
    hero_scores = {}
    radiant_turn, is_pick = get_turn_and_action(pick_index, pick_order)
    for hero in heroes_not_in(radiant + dire + banned):
        if is_pick:
            if radiant_turn:
                new_radiant = copy_list_with_hero(radiant, hero)
                radiant_score, dire_score = monte_carlo_subsearch(new_radiant, dire, banned, depth - 1, pick_index + 1,
                                                                  pick_order, best_radiant)
            else:
                new_dire = copy_list_with_hero(dire, hero)
                radiant_score, dire_score = monte_carlo_subsearch(radiant, new_dire, banned, depth - 1, pick_index + 1,
                                                                  pick_order, best_radiant)
        else:
            new_banned = copy_list_with_hero(banned, hero)
            radiant_score, dire_score = monte_carlo_subsearch(radiant, dire, new_banned, depth - 1, pick_index + 1,
                                                              pick_order, best_radiant)
        if radiant_turn:
            hero_score = radiant_score - dire_score
        else:
            hero_score = dire_score - radiant_score
        hero_scores[hero] = hero_score
    return hero_scores
