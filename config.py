# how many versions of each dimension are enabled
# 0 is disabled
# 1 is enabled normally
# >1 cycles between dimensions
enabled_dimensions = [
    0, # shape color
    0, # shape
    0, # number of shapes
    0, # shading
    1, # border style
    1, # border color
    1, # number of borders
    1, # background shading
]

# dimension of the game
dim = sum(enabled_dimensions)

# number of cards in the deck
deck_size = 3 ** dim

# number of cards displayed at a time
num_cards = dim + 2

# num cols, num rows
grid_size = ((num_cards + 1) // 2, 2)

num_players = 1

# whether twin sets should be found automatically
# removes valid set checking if disabled
do_find_twin_sets = True