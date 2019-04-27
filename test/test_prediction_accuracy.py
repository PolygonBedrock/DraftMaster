from utils.prediction_utils import *
from utils.time_utils import *
from openers.games_data import *
from openers.value_data import *

print("Setting up...")

total_predictions = 0
correct_predictions = 0

print("Predicting games...")
start_time = current_time_ms()
for game in games:
	radiant = game[RADIANT_KEY]
	dire = game[DIRE_KEY]
	winner = game[WINNER_KEY]
	radiant_score, dire_score = predict(radiant, dire)
	if radiant_score > dire_score and winner == RADIANT_KEY or dire_score > radiant_score and winner == DIRE_KEY:
		correct_predictions += 1
	total_predictions += 1
stop_time = current_time_ms()

total_time = stop_time - start_time
	
print("Accuracy: " + str(correct_predictions / total_predictions) + "(" + str(correct_predictions) + "/" + str(total_predictions) + ")")
print("Ms per prediction: " + str(total_time / total_predictions))