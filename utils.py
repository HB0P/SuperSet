import config as conf
import random

def get_all_cards():
    deck = []
    for i in range(3 ** conf.dim):
        card = [int(i // (3 ** j)) % 3 for j in range(conf.dim)]
        deck.append(card)
    return deck

def create_deck():
    deck = get_all_cards()
    random.shuffle(deck)
    return deck