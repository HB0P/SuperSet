dim = 18

# number of cards in the deck
deck_size = 3 ** dim
deck_size = 100

# number of cards displayed at a time
num_cards = dim + 2

# num cols, num rows
grid_size = ((num_cards + 1) // 2, 2)
grid_size = (5, 4)

num_players = 1

# whether twin sets should be found automatically
# removes valid set checking if disabled
do_find_twin_sets = False