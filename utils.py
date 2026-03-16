from datetime import timedelta
import config as conf
import random
import numpy as np
import json

def get_all_cards():
    deck = []
    for i in range(conf.base ** conf.dim):
        card = [int(i // (conf.base ** j)) % conf.base for j in range(conf.dim)]
        deck.append(np.array(card))
    return deck

def create_deck():
    deck = []
    for i in random.sample(range(conf.base ** conf.dim), conf.deck_size):
        card = [int(i // (conf.base ** j)) % conf.base for j in range(conf.dim)]
        deck.append(np.array(card))
    return deck

def save_best_time(time: timedelta):
    with open("data/best_times.json", "r") as f:
        data = json.load(f)
    data[str(conf.dim) + "-" + str(conf.num_cards)] = time.seconds
    with open("data/best_times.json", "w") as f:
        json.dump(data, f)
