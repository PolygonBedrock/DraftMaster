import pymongo
import pickle
from main.constants import *

print("Setting up...")

client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DOTA2_DATABASE]
heroes_table = db[HEROES_TABLE]

index = 0
hero_ids = {}

for hero in heroes_table.find({}):
    name = hero['localized_name']
    hero_ids[name] = index
    index += 1

print(hero_ids)

print("Saving data...")

print(HERO_INDEX_FILE)
with open(HERO_INDEX_FILE, 'wb') as fp:
    pickle.dump(hero_ids, fp, protocol=pickle.HIGHEST_PROTOCOL)