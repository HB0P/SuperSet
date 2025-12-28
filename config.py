# how many versions of each dimension are enabled
# 0 is disabled
# 1 is enabled normally
# >1 cycles between dimensions
enabled_dimensions = [
    1, # shape color
    1, # shape
    1, # number of shapes
    1, # shading
    0, # border style
    0, # border color
    0, # number of borders
    0, # background shading
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