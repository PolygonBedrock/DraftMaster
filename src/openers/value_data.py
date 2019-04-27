import pickle
from main.constants import *

with open(VALUES_FILE, 'rb') as fp:
	values = pickle.load(fp)
	
hero_values = values[HEROES_KEY]
matchup_values = values[MATCHUPS_KEY]
combo_values = values[COMBOS_KEY]
faction_values = values[FACTIONS_KEY]