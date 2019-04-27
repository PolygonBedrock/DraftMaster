import dota2api
import time
import pymongo
from threading import Thread

DOTA2_DATABASE = "dota2"
MATCH_DETAILS_TABLE = "match_details"
STEAM_API_KEY = "E5E97D6166ADB1F6D5DB97D2F1284988"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

api = dota2api.Initialise(STEAM_API_KEY)
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DOTA2_DATABASE]
match_details_table = db[MATCH_DETAILS_TABLE]

first_match_id = 2


def get_last_match_id():
	got_last_match_id = False
	while (not got_last_match_id):
		try:
			match_id = api.get_match_history()['matches'][0]['match_id']
			got_last_match_id = True
		except:
			pass
		time.sleep(1)
	return match_id


def get_match_details(match_id):
	try:
		return api.get_match_details(match_id=match_id)
	except:
		return None																																																																	


def is_match_in_database(match_id):
	try:
		return match_details_table.find_one({"match_id": match_id}) is not None
	except:
		return False


def post_match_to_database(match):
	try:
		match_details_table.insert_one(match)
	except:
		pass


def scrape_game(match_id):
	if not is_match_in_database(match_id):
			match = get_match_details(match_id)
			if match is not None:
				post_match_to_database(match)
				print("Scraped match: " + str(match_id))


def scrape_game_in_background(match_id):
	thread = Thread(target=scrape_game, args=(match_id,))
	thread.setDaemon(True)
	thread.start()


print("Commencing scraping...")
while True:
	last_match_id = get_last_match_id()
	for match_id in range(last_match_id, first_match_id - 1, -1):
		scrape_game_in_background(match_id)
	print("Restarting scrape from current latests match...")