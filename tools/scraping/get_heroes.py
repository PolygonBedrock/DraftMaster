import dota2api
import pymongo

DOTA2_DATABASE = "dota2"
HEROES_TABLE = "heroes"
STEAM_API_KEY = "E5E97D6166ADB1F6D5DB97D2F1284988"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

api = dota2api.Initialise(STEAM_API_KEY)
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DOTA2_DATABASE]
heroes_table = db[HEROES_TABLE]

heroes = api.get_heroes()['heroes']
heroes_table.remove({})
heroes_table.insert_many(heroes)

print(heroes)