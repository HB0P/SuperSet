import tkinter as tk
import tksvg
from tksvg import SvgImage

import imagegen
import engine
import utils
import config as conf

### game state
deck = utils.create_deck() # the remaining deck
cards = [deck.pop() for _ in range(conf.num_cards)] # the face-up cards
selected_cards = [] # indexes of which cards are selected

### gui state
imgs: list[SvgImage] = [None] * conf.num_cards
buttons: list[tk.Button] = [None] * conf.num_cards

### gui functions
def refresh_button(i, refresh_image=False):
    if refresh_image:
        svg = imagegen.gen_svg(cards[i]).to_str().decode()
        img = tksvg.SvgImage(data=svg).subsample(2)
        imgs[i] = img
        buttons[i]["image"] = imgs[i]

    if cards[i] is None:
        buttons[i].configure(activebackground="white")
    buttons[i]["background"] = "lightgray" if i in selected_cards else "white"

def refresh_card_count():
    card_count_label.configure(text=str(len(deck)))

def click_card(i):
    if cards[i] is None:
        return
    if i in selected_cards:
        selected_cards.remove(i)
    else:
        selected_cards.append(i)
    refresh_button(i)

def submit():
    submit_button["background"] = "chartreuse3"
    def reset_color():
        submit_button["background"] = "chartreuse4"
    root.after(150, reset_color)

    trial_set = [cards[i] for i in selected_cards]
    valid = engine.is_twin_set(trial_set)
    if valid:
        for i in range(conf.num_cards):
            if i in selected_cards:
                cards[i] = None if len(deck) == 0 else deck.pop()
        refresh_card_count()

    prev_selected_cards = [i for i in selected_cards]
    selected_cards.clear()
    for i in prev_selected_cards:
        refresh_button(i, valid)

### create gui
root = tk.Tk()
root.configure()
root.title("Superset")
root.resizable(False, False)

cards_frame = tk.Frame(root, bg="white")
cards_frame.pack(side="top")
controls_frame = tk.Frame(root)
controls_frame.pack(side="bottom", fill="x", expand=True, padx=10, pady=10)

# create buttons
for i in range(conf.num_cards):
    button = tk.Button(
        cards_frame,
        bd=0,
        relief="sunken",
        command=lambda n=i: click_card(n)
    )
    buttons[i] = button

# give images to buttons
for i in range(conf.num_cards):
    refresh_button(i, True)

# place buttons on grid
for x in range(conf.grid_size[0]):
    for y in range(conf.grid_size[1]):
        i = x + y*conf.grid_size[0]
        if i >= len(buttons):
            break
        buttons[i].grid(column=x, row=y)

# submit button
submit_button = (tk.Button(
    controls_frame,
    text="SUBMIT",
    bg="chartreuse4",
    activebackground="chartreuse3",
    bd=0,
    relief="sunken",
    height=2,
    font=("helvetica", 24),
    command=submit
))
submit_button.pack(
    side="left",
    fill="x",
    expand=True,
)

# card count
card_count_label = tk.Label(
    controls_frame,
    width=3,
    font=("helvetica", 24)
)
card_count_label.pack(
    side="right",
    padx=(10, 0)
)
refresh_card_count()

root.mainloop()
