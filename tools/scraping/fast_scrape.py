import dota2api
import time
import pymongo


DOTA2_DATABASE = "dota2"
MATCH_DETAILS_TABLE = "match_details"
STEAM_API_KEY = "E5E97D6166ADB1F6D5DB97D2F1284988"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

api = dota2api.Initialise(STEAM_API_KEY)
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DOTA2_DATABASE]
match_details_table = db[MATCH_DETAILS_TABLE]


def get_last_match_seq_num():
    got_last_match_id = False
    while not got_last_match_id:
        try:
            match_seq_num = api.get_match_history()['matches'][0]['match_seq_num']
            got_last_match_id = True
        except:
            pass
        time.sleep(1)
    return match_seq_num


def get_match_block_bounded_by(match_seq_num):
    matches = []
    while not matches:
        try:
            matches = api.get_match_history_by_seq_num(start_at_match_seq_num=match_seq_num)['matches']
        except:
            pass
        time.sleep(1)
    return matches


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


print("Commencing scraping...")
match_seq_num = get_last_match_seq_num()
while True:
    matches = get_match_block_bounded_by(match_seq_num)
    for match in matches:
        match_seq_num = match['match_seq_num']
        match_id = match['match_id']
        if not is_match_in_database(match_id):
            post_match_to_database(match)
            print("Scraped match: " + str(match_id))
        match_seq_num = max(match_seq_num, match_seq_num)

