from main.constants import *
import pickle

with open(GAMES_FILE, 'rb') as fp:
	games = pickle.load(fp)