import config as conf
import random

def create_deck():
    deck = []
    for i in range(3 ** conf.dim):
        card = [int(i // (3 ** j)) % 3 for j in range(conf.dim)]
        deck.append(card)
    random.shuffle(deck)
    return deck