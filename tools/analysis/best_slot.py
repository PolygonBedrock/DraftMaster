import pymongo
from utils.misc_utils import *
from pymongo import MongoClient
from utils.file_utils import *
from main.constants import *

print("Setting up...")

client: MongoClient = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DOTA2_DATABASE]
match_details_table = db[MATCH_DETAILS_TABLE]
heroes_table = db[HEROES_TABLE]


def is_player_radiant(player):
    return 0 <= player['player_slot'] <= 4


def get_hero_slot(hero, team):
    hero_last_hits = team[hero]
    slot = 1
    for ally in team:
        if ally != hero:
            ally_last_hits = team[ally]
            if ally_last_hits > hero_last_hits:
                slot += 1
    return slot


radiant_win_exists = {
    "radiant_win": {
        "$exists": True
    }
}
ten_players_filter = {
    "human_players": 10
}
no_leavers_filter = {
    "players.leaver_status": {
        "$not": {
            "$gt": 0
        }
    }
}
valid_lobby_type_filter = {
    "$or": [
        {"lobby_type": 0},
        {"lobby_type": 2},
        {"lobby_type": 5},
        {"lobby_type": 6},
        {"lobby_type": 7}
    ]
}
valid_game_mode_filter = {
    "$or": [
        {"game_mode": 1},
        {"game_mode": 2},
        {"game_mode": 16},
        {"game_mode": 22}
    ]
}
valid_game_filter = {
    "$and": [
        ten_players_filter,
        no_leavers_filter,
        valid_lobby_type_filter,
        valid_game_mode_filter,
        radiant_win_exists
    ]
}

print("Querying valid games...")
valid_games = match_details_table.find(valid_game_filter)
heroes = heroes_table.find({})
hero_translation = {}
win_loss_by_slot = {}

for hero in heroes:
    hero_id = hero['id']
    name = hero['localized_name']
    hero_translation[hero_id] = name
    win_loss_by_slot[name] = {
        1: {WINS_KEY: 0, LOSSES_KEY: 0},
        2: {WINS_KEY: 0, LOSSES_KEY: 0},
        3: {WINS_KEY: 0, LOSSES_KEY: 0},
        4: {WINS_KEY: 0, LOSSES_KEY: 0},
        5: {WINS_KEY: 0, LOSSES_KEY: 0}
    }

games = []


print("Formatting data...")
for game in valid_games:
    winner = None
    radiant = {}
    dire = {}
    if game[API_RADIANT_WIN]:
        winner = RADIANT_KEY
    else:
        winner = DIRE_KEY
    for player in game[API_PLAYERS]:
        hero_id = player[API_HERO_ID]
        last_hits = player[API_LAST_HITS]
        hero_name = hero_translation[hero_id]
        if is_player_radiant(player):
            radiant[hero_name] = last_hits
        else:
            dire[hero_name] = last_hits
    for hero in radiant:
        slot = get_hero_slot(hero, radiant)
        if winner == RADIANT_KEY:
            win_loss_by_slot[hero][slot][WINS_KEY] += 1
        else:
            win_loss_by_slot[hero][slot][LOSSES_KEY] += 1
    for hero in dire:
        slot = get_hero_slot(hero, dire)
        if winner == DIRE_KEY:
            win_loss_by_slot[hero][slot][WINS_KEY] += 1
        else:
            win_loss_by_slot[hero][slot][LOSSES_KEY] += 1

winrate_by_slot = {}

for hero in win_loss_by_slot:
    winrate_by_slot[hero] = {}
    for slot in win_loss_by_slot[hero]:
        wins = win_loss_by_slot[hero][slot][WINS_KEY]
        losses = win_loss_by_slot[hero][slot][LOSSES_KEY]
        if losses == 0:
            winrate_by_slot[hero][slot] = 1
        else:
            winrate_by_slot[hero][slot] = wins / (wins + losses)

print(winrate_by_slot)

