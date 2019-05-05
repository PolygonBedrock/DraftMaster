from main.constants import *
from utils.file_utils import *

values_from_file = open_file(VALUES_FILE)

hero_values = values_from_file[HEROES_KEY]
matchup_values = values_from_file[MATCHUPS_KEY]
combo_values = values_from_file[COMBOS_KEY]
faction_values = values_from_file[FACTIONS_KEY]