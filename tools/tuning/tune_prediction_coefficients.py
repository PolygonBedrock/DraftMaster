from utils.prediction_utils import *
from openers.games_data import *
from openers.value_data import *

print("Setting up...")

heroes_coefficient = 10
matchup_coefficient = 10
combo_coefficient = 10
faction_coefficient = 10
cost_coefficient = 10
coefficients = [heroes_coefficient, matchup_coefficient, combo_coefficient, faction_coefficient, cost_coefficient]
average = sum(coefficients) / len(coefficients)
tune_value = average / 2


def get_accuracy():
    total_predictions = 0
    correct_predictions = 0
    for game in games:
        radiant = game[RADIANT_KEY]
        dire = game[DIRE_KEY]
        winner = game[WINNER_KEY]
        radiant_score, dire_score = predict(radiant, dire, heroes_coefficient, matchup_coefficient, combo_coefficient,
                                            faction_coefficient, cost_coefficient)
        difference = radiant_score - dire_score
        differences.append(difference)
        if radiant_score > dire_score and winner == RADIANT_KEY or dire_score > radiant_score and winner == DIRE_KEY:
            correct_predictions += 1
        total_predictions += 1
    return correct_predictions / total_predictions


def tune_heroes():
    global heroes_coefficient
    global current_accuracy
    old_coefficient = heroes_coefficient
    heroes_coefficient = old_coefficient + tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    heroes_coefficient = old_coefficient - tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    heroes_coefficient = old_coefficient


def tune_matchup():
    global matchup_coefficient
    global current_accuracy
    old_coefficient = matchup_coefficient
    matchup_coefficient = old_coefficient + tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    matchup_coefficient = old_coefficient - tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    matchup_coefficient = old_coefficient


def tune_combo():
    global combo_coefficient
    global current_accuracy
    old_coefficient = combo_coefficient
    combo_coefficient = old_coefficient + tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    combo_coefficient = old_coefficient - tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    combo_coefficient = old_coefficient


def tune_faction():
    global faction_coefficient
    global current_accuracy
    old_coefficient = faction_coefficient
    faction_coefficient = old_coefficient + tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    faction_coefficient = old_coefficient - tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    faction_coefficient = old_coefficient


def tune_cost():
    global cost_coefficient
    global current_accuracy
    old_coefficient = cost_coefficient
    cost_coefficient = old_coefficient + tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    cost_coefficient = old_coefficient - tune_value
    new_current_accuracy = get_accuracy()
    if new_current_accuracy > current_accuracy:
        current_accuracy = new_current_accuracy
        return
    cost_coefficient = old_coefficient


improved_fine = True
improved_gross = True

differences = []
current_accuracy = get_accuracy()
best_fine_accuracy = current_accuracy
best_gross_accuracy = current_accuracy

while improved_gross:
    while improved_fine:
        print("current heroes coefficient: " + str(heroes_coefficient))
        print("current matchup coefficient: " + str(matchup_coefficient))
        print("current combo coefficient: " + str(combo_coefficient))
        print("current faction coefficient: " + str(faction_coefficient))
        print("current cost coefficient: " + str(cost_coefficient))
        print("current accuracy: " + str(current_accuracy))
        print("")
        del differences[:]
        tune_heroes()
        tune_matchup()
        tune_combo()
        tune_faction()
        tune_cost()
        if current_accuracy > best_fine_accuracy:
            print("improved fine accuracy")
            improved_fine = True
            best_fine_accuracy = current_accuracy
        else:
            print("did not improve fine accuracy")
            improved_fine = False
        tune_value /= 2
        print("fine tune value="+str(tune_value))
    if best_fine_accuracy > best_gross_accuracy:
        print("improved gross accuracy")
        improved_gross = True
        improved_fine = True
        best_gross_accuracy = best_fine_accuracy
    else:
        print("did not improve gross accuracy")
        improved_gross = False
    coefficients = [heroes_coefficient, matchup_coefficient, combo_coefficient, faction_coefficient]
    average = sum(coefficients) / len(coefficients)
    tune_value = average / 2
    print("gross tune value="+str(tune_value))

print("best heroes coefficient: " + str(heroes_coefficient))
print("best matchup coefficient: " + str(matchup_coefficient))
print("best combo coefficient: " + str(combo_coefficient))
print("best faction coefficient: " + str(faction_coefficient))
print("best cost coefficient: " + str(cost_coefficient))
print("best accuracy: " + str(current_accuracy))
print("")
print("max diff: " + str(max(max(differences), abs(min(differences)))))
