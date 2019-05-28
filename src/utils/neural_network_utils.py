import tensorflow
from tensorflow import keras
from utils.drafting_utils import *
import numpy

indexes_to_heroes = {}
for hero in hero_indexes:
    indexes_to_heroes[hero_indexes[hero]] = hero


def load_model():
    model = new_model()
    model.load_weights(DRAFTING_MODEL_FILE)
    return model


def save_model(model):
    model.save_weights(DRAFTING_MODEL_FILE)


def new_model():
    input_length = len(NN_OFFSETS) * len(hero_indexes) + 2 * TEAM_SIZE
    output_length = len(hero_indexes)
    middle_hidden_length = int((input_length + output_length) / 2)
    upper_hidden_length = int(middle_hidden_length * 1.5)
    lower_hidden_length = int(middle_hidden_length * 0.5)

    model = keras.Sequential([
        keras.layers.Dense(upper_hidden_length, input_shape=(input_length,)),
        keras.layers.Dense(middle_hidden_length),
        keras.layers.Dense(lower_hidden_length),
        keras.layers.Dense(output_length, activation=tensorflow.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def train_model(model, inputs, outputs, epochs):
    model.fit(numpy.array(inputs), outputs, epochs=epochs)


def hero_to_nn_input_index(hero, offset):
    return hero_to_nn_output_index(hero) * len(NN_OFFSETS) + offset


def hero_to_nn_output_index(hero):
    return hero_indexes[hero]


def nn_output_index_to_hero(index):
    return indexes_to_heroes[index]


def roster_to_nn_input(ally_team, enemy_team, banned):
    nn_input = [0] * (len(NN_OFFSETS) * len(hero_indexes) + 2 * TEAM_SIZE)
    for hero in ally_team:
        nn_input[hero_to_nn_input_index(hero, ALLY_NN_OFFSET)] = 1
    for hero in enemy_team:
        nn_input[hero_to_nn_input_index(hero, ENEMY_NN_OFFSET)] = 1
    for hero in banned:
        nn_input[hero_to_nn_input_index(hero, BANNED_NN_OFFSET)] = 1

    nn_input[len(nn_input) - 1 - len(ally_team) - len(enemy_team)] = 1
    return nn_input


def nn_output_to_hero_scores(nn_output):
    hero_scores = {}
    for index in range(len(nn_output)):
        hero = nn_output_index_to_hero(index)
        score = nn_output[index]
        hero_scores[hero] = score
    return hero_scores


def get_model_hero_scores(model, ally_team, enemy_team, banned):
    nn_input = roster_to_nn_input(ally_team, enemy_team, banned)
    nn_output = get_nn_output(model, nn_input)
    hero_scores = nn_output_to_hero_scores(nn_output)
    return hero_scores


def get_model_hero_ranks(model, ally_team, enemy_team, banned):
    excluded = []
    rank = 1
    hero_ranks = {}
    while len(ally_team) + len(enemy_team) + len(banned) + len(excluded) < len(hero_indexes):
        hero = get_model_best_pick(model, ally_team, enemy_team, banned + excluded)
        hero_ranks[hero] = rank
        rank += 1
        excluded.append(hero)
    return hero_ranks


def get_model_best_pick(model, ally_team, enemy_team, banned):
    hero_scores = get_model_hero_scores(model, ally_team, enemy_team, banned)
    return best_scoring_hero(hero_scores, ally_team + enemy_team + banned)


def get_nn_output(model, nn_input):
    return model.predict(numpy.array([nn_input, ]))[0]


def get_nn_input_output_and_hero(model, ally_team, enemy_team, banned):
    nn_input = roster_to_nn_input(ally_team, enemy_team, banned)
    nn_output = get_nn_output(model, nn_input)
    hero_scores = nn_output_to_hero_scores(nn_output)
    hero = best_scoring_hero(hero_scores, ally_team + enemy_team + banned)
    nn_output = hero_to_nn_output_index(hero)
    return nn_input, nn_output, hero

