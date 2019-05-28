from utils.neural_network_utils import *
from utils.drafting_utils import *
import random

GAMES_PER_GENERATION = 1000
TRAINING_EPOCHS = 1


def record_nn_inputs_and_outputs(winning_nn_inputs, winning_nn_outputs, losing_nn_inputs, losing_nn_outputs,
                                 recorded_nn_inputs, recorded_nn_outputs):
    for nn_input in winning_nn_inputs:
        recorded_nn_inputs.append(nn_input)
    for nn_output in winning_nn_outputs:
        recorded_nn_outputs.append(nn_output)

    for nn_input in losing_nn_inputs:
        recorded_nn_inputs.append(nn_input)
    for nn_output in losing_nn_outputs:
        hero = nn_output_index_to_hero(nn_output)
        nn_output = hero_to_nn_output_index(random.choice(heroes_not_in([hero])))
        recorded_nn_outputs.append(nn_output)


def model_vs_model(radiant_model, dire_model):
    radiant = []
    dire = []
    banned = []
    for pick_index in range(len(CAPTAINS_MODE_ORDER)):
        radiant_turn, is_pick = get_turn_and_action(pick_index, CAPTAINS_MODE_ORDER)
        if radiant_turn:
            if is_pick:
                pick = get_model_best_pick(radiant_model, radiant, dire, banned)
                radiant.append(pick)
            else:
                ban = get_model_best_pick(radiant_model, dire, radiant, banned)
                banned.append(ban)
        else:
            if is_pick:
                pick = get_model_best_pick(dire_model, dire, radiant, banned)
                radiant.append(pick)
            else:
                ban = get_model_best_pick(dire_model, radiant, dire, banned)
                banned.append(ban)

    return predict(radiant, dire)


def model_vs_nbp(model, model_is_radiant):
    radiant = []
    dire = []
    banned = []
    for pick_index in range(len(CAPTAINS_MODE_ORDER)):
        radiant_turn, is_pick = get_turn_and_action(pick_index, CAPTAINS_MODE_ORDER)
        if radiant_turn:
            if is_pick:
                if model_is_radiant:
                    pick = get_model_best_pick(model, radiant, dire, banned)
                else:
                    pick = naive_best_pick(radiant, dire, banned)
                radiant.append(pick)
            else:
                if model_is_radiant:
                    ban = get_model_best_pick(model, dire, radiant, banned)
                else:
                    ban = naive_best_pick(dire, radiant, banned)
                banned.append(ban)
        else:
            if is_pick:
                if model_is_radiant:
                    pick = naive_best_pick(dire, radiant, banned)
                else:
                    pick = get_model_best_pick(model, dire, radiant, banned)
                dire.append(pick)
            else:
                if model_is_radiant:
                    ban = naive_best_pick(radiant, dire, banned)
                else:
                    ban = get_model_best_pick(model, radiant, dire, banned)
                banned.append(ban)

    radiant_score, dire_score = predict(radiant, dire)

    if model_is_radiant:
        print("Radiant (Model): " + str(radiant) + "; Score: " + str(radiant_score))
        print("Dire (NBP): " + str(dire) + "; Score: " + str(dire_score))
    else:
        print("Radiant (NBP): " + str(radiant) + "; Score: " + str(radiant_score))
        print("Dire (Model): " + str(dire) + "; Score: " + str(dire_score))

    return radiant_score, dire_score


def does_new_model_beat_old_model(model, old_model):
    new_radiant_score, old_dire_score = model_vs_model(model, old_model)
    new_dire_score, old_radiant_score = model_vs_model(old_model, model)
    return new_radiant_score + new_dire_score > old_radiant_score + old_dire_score


def does_model_beat_nbp(model):
    model_radiant_score, nbp_dire_score = model_vs_nbp(model, True)
    nbp_radiant_score, model_dire_score = model_vs_nbp(model, False)
    return model_radiant_score > nbp_dire_score and model_dire_score > nbp_radiant_score


def main():
    vs_nbp_wins = 0
    vs_nbp_losses = 0

    try:
        model = load_model()
    except:
        model = new_model()

    generation = 0

    while True:
        generation += 1
        for game in range(GAMES_PER_GENERATION):
            print("Generation " + str(generation) + " Game " + str(game + 1) + "/" + str(GAMES_PER_GENERATION))

            radiant = []
            dire = []
            banned = []
            radiant_nn_inputs = []
            radiant_nn_outputs = []
            dire_nn_inputs = []
            dire_nn_outputs = []
            nn_inputs = []
            nn_outputs = []

            if vs_nbp_wins > vs_nbp_losses:
                model_playing_as = None  # radiant, dire, or none if playing as both
            else:
                model_playing_as = random.choice([RADIANT_KEY, DIRE_KEY])

            for pick_index in range(len(CAPTAINS_MODE_ORDER)):
                radiant_turn, is_pick = get_turn_and_action(pick_index, CAPTAINS_MODE_ORDER)

                if radiant_turn:
                    if is_pick:
                        if model_playing_as == RADIANT_KEY or model_playing_as is None:
                            nn_input, nn_output, hero = get_nn_input_output_and_hero(model, radiant, dire, banned)
                        else:
                            nn_input = roster_to_nn_input(radiant, dire, banned)
                            hero = naive_best_pick(radiant, dire, banned)
                            nn_output = hero_to_nn_output_index(hero)

                        radiant.append(hero)

                    else:
                        if model_playing_as == RADIANT_KEY or model_playing_as is None:
                            nn_input, nn_output, hero = get_nn_input_output_and_hero(model, dire, radiant, banned)
                        else:
                            nn_input = roster_to_nn_input(dire, radiant, banned)
                            hero = naive_best_pick(dire, radiant, banned)
                            nn_output = hero_to_nn_output_index(hero)

                        banned.append(hero)
                    radiant_nn_inputs.append(nn_input)
                    radiant_nn_outputs.append(nn_output)

                else:
                    if is_pick:
                        if model_playing_as == DIRE_KEY or model_playing_as is None:
                            nn_input, nn_output, hero = get_nn_input_output_and_hero(model, dire, radiant, banned)
                        else:
                            nn_input = roster_to_nn_input(dire, radiant, banned)
                            hero = naive_best_pick(dire, radiant, banned)
                            nn_output = hero_to_nn_output_index(hero)

                        dire.append(hero)

                    else:
                        if model_playing_as == DIRE_KEY or model_playing_as is None:
                            nn_input, nn_output, hero = get_nn_input_output_and_hero(model, radiant, dire, banned)
                        else:
                            nn_input = roster_to_nn_input(radiant, dire, banned)
                            hero = naive_best_pick(radiant, dire, banned)
                            nn_output = hero_to_nn_output_index(hero)

                        banned.append(hero)
                    dire_nn_inputs.append(nn_input)
                    dire_nn_outputs.append(nn_output)

            radiant_score, dire_score = predict(radiant, dire)

            if radiant_score > dire_score:
                record_nn_inputs_and_outputs(radiant_nn_inputs, radiant_nn_outputs,
                                             dire_nn_inputs, dire_nn_outputs, nn_inputs, nn_outputs)
            else:
                record_nn_inputs_and_outputs(dire_nn_inputs, dire_nn_outputs,
                                             radiant_nn_inputs, radiant_nn_outputs, nn_inputs, nn_outputs)

            train_model(model, nn_inputs, nn_outputs, TRAINING_EPOCHS)

        try:
            old_model = load_model()
            if does_new_model_beat_old_model(model, old_model):
                print("New model beat old model, saving...")
                save_model(model)
                del old_model
            else:
                print("Old model beat new model, continuing...")
        except:
            save_model(model)

        if does_model_beat_nbp(model):
            vs_nbp_wins += 1
            print("Model beats Naive Best Pick, continuing...")
        else:
            vs_nbp_losses += 1
            print("Model does not beat Naive Best Pick, continuing...")
        print("Model vs NBP W/L: " + str(vs_nbp_wins) + "/" + str(vs_nbp_losses))

main()

