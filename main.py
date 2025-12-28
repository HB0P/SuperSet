import tkinter as tk
import tksvg
from tksvg import SvgImage
from datetime import datetime as dt
import config
import imagegen
import engine
import utils
import config as conf
from functools import partial
# import vlc

### game state
deck = utils.create_deck() # the remaining deck
cards = [deck.pop() for _ in range(conf.num_cards)] # the face-up cards
selected_cards = [] # indexes of which cards are selected
twin_sets = [] # all twin sets in the currently face up cards
scores = [0] * conf.num_players
start_time = dt.now()
game_active = True

### gui state
imgs: list[SvgImage] = [None] * conf.num_cards
buttons: list[tk.Button] = [None] * conf.num_cards
submit_buttons: list[tk.Button] = [None] * conf.num_players
score_labels: list[tk.Label] = [None] * conf.num_players

music_player = None

### game functions
def is_twin_set_selected():
    if not conf.do_find_twin_sets:
        return True

    for twin_set in twin_sets:
        if len(selected_cards) != len(twin_set):
            continue
        valid = True
        i = 0
        for card_index in range(config.num_cards):
            if not card_index in selected_cards:
                continue
            if (cards[card_index] != twin_set[i]).any():
                valid = False
                break
            i += 1
        if valid:
            return True
    return False

### gui functions
def refresh_button(i):
    frame = int((dt.now() - start_time).total_seconds())
    svg = imagegen.gen_svg(cards[i], frame).to_str().decode()
    img = tksvg.SvgImage(data=svg).subsample(2)
    imgs[i] = img
    buttons[i]["image"] = imgs[i]

    if cards[i] is None:
        buttons[i].configure(activebackground="white")
    buttons[i]["background"] = "lightgray" if i in selected_cards else "white"

def refresh_cards():
    global twin_sets
    for i in range(conf.num_players):
        score_labels[i].configure(text=str(scores[i]))
    card_count_label.configure(text=str(len(deck)) + " remaining")

    if conf.do_find_twin_sets:
        twin_sets = engine.find_twin_sets([card for card in cards if card is not None])
        if len(twin_sets) == 1:
            game_over()

def click_card(i):
    if cards[i] is None:
        return
    if i in selected_cards:
        selected_cards.remove(i)
    else:
        selected_cards.append(i)
    refresh_button(i)

def submit(player):
    print("submit", player)
    submit_buttons[player]["background"] = "chartreuse3"
    def reset_color(plr):
        if game_active:
            submit_buttons[plr]["background"] = "chartreuse4"
    root.after(150, reset_color, player)

    valid = is_twin_set_selected()
    if valid:
        for i in range(conf.num_cards):
            if i in selected_cards:
                cards[i] = None if len(deck) == 0 else deck.pop()
        scores[player] += len(selected_cards)
        refresh_cards()

    prev_selected_cards = [i for i in selected_cards]
    selected_cards.clear()
    for i in prev_selected_cards:
        refresh_button(i)

def update_timer():
    elapsed_time = dt.now() - start_time
    timer_label.configure(text=str(elapsed_time)[2:-7])
    for i in range(len(cards)):
        refresh_button(i)
    if game_active:
        root.after(10, update_timer)

def game_over():
    global game_active
    game_active = False
    for btn in submit_buttons:
        btn.configure(
            text="GAME OVER",
            state="disabled",
            bg="red"
        )
    if conf.num_players == 1:
        utils.save_best_time(dt.now() - start_time)

#def on_card_hover_start(i):
#    global music_player
#    if conf.dim > 8 and conf.dim % 2 == 0:
#        music = cards[i][-1]
#        music_player = vlc.MediaPlayer("file:///music/music" + str(music) + ".mp3")
#        music_player.play()

#def on_card_hover_end():
#    global music_player
#    if music_player is not None:
#        music_player.stop()
#        music_player = None

### create gui
root = tk.Tk()
root.configure()
root.title("Superset")
root.resizable(False, False)

# create frames
cards_frame = tk.Frame(root, bg="white")
cards_frame.pack(side="top")
controls_frame = tk.Frame(root)
controls_frame.pack(
    side="bottom",
    fill="x",
    expand=True,
    padx=5,
    pady=5
)
for i in range(max(2, conf.num_players)):
    controls_frame.grid_columnconfigure(i, weight=1)

# card buttons
for i in range(conf.num_cards):
    button = tk.Button(
        cards_frame,
        bd=0,
        relief="sunken",
        command=lambda n=i: click_card(n)
    )
    #button.bind("<Enter>", lambda _, n=i: on_card_hover_start(n))
    #button.bind("<Leave>", lambda _: on_card_hover_end())
    buttons[i] = button

# give images to buttons
for i in range(conf.num_cards):
    refresh_button(i)

# place buttons on grid
for x in range(conf.grid_size[0]):
    for y in range(conf.grid_size[1]):
        i = x + y*conf.grid_size[0]
        if i >= len(buttons):
            break
        buttons[i].grid(column=x, row=y)

# submit buttons
for i in range(conf.num_players):
    submit_buttons[i] = tk.Button(
        controls_frame,
        text = "SUBMIT" if conf.num_players == 1 else "Player " + str(i+1) + "\nSUBMIT",
        bg="chartreuse4",
        activebackground="chartreuse3",
        disabledforeground="white",
        bd=0,
        relief="sunken",
        height=2,
        font=("helvetica", 24),
        command = partial(submit, i)
    )
    submit_buttons[i].grid(
        row=0,
        column=i,
        sticky="EW",
        padx=5,
        pady=5,
        columnspan = 2 if conf.num_players == 1 else 1
    )

# scores
for i in range(conf.num_players):
    score_labels[i] = tk.Label(
        controls_frame,
        font=("helvetica", 24)
    )
    if conf.num_players != 1:
        score_labels[i].grid(
            row=1,
            column=i
        )

# card count
card_count_label = tk.Label(
    controls_frame,
    font=("helvetica", 24)
)
if conf.num_players == 1:
    card_count_label.grid(
        row=1,
        column=0,
        sticky="W"
    )
else:
    card_count_label.grid(
        row=2,
        column=0,
        columnspan=conf.num_players
    )
refresh_cards()

# timer
if conf.num_players == 1:
    timer_label = tk.Label(
        controls_frame,
        font=("helvetica", 24)
    )
    timer_label.grid(
        row=1,
        column=1,
        sticky="E"
    )
    update_timer()

root.mainloop()
