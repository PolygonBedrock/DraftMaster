import pickle
from main.constants import *

with open(HERO_INDEX_FILE, 'rb') as fp:
    hero_indexes = pickle.load(fp)
