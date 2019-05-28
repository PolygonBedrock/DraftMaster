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
gpm_data = {}

for hero in heroes:
    hero_id = hero['id']
    name = hero['localized_name']
    hero_translation[hero_id] = name

games = []

print("Formatting data...")
for game in valid_games:
    radiant = []
    dire = []
    winner = None
    for player in game[API_PLAYERS]:
        heroId = player[API_HERO_ID]
        heroName = hero_translation[heroId]
        if is_player_radiant(player):
            radiant.append(heroName)
        else:
            dire.append(heroName)
    if game[API_RADIANT_WIN]:
        winner = RADIANT_KEY
    else:
        winner = DIRE_KEY
    game_data = {RADIANT_KEY: radiant, DIRE_KEY: dire, WINNER_KEY: winner}
    games.append(game_data)

costs = {}
max_cost = NEGATIVE_INFINITY
min_cost = POSITIVE_INFINITY

for hero in costs:
    costs[hero] = normalize(costs[hero], max_cost, min_cost, 1, -1)

print("Saving data...")

save_to_file(games, GAMES_FILE)

print("Games saved: " + str(len(games)))
