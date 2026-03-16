import io

import resvg_py
import svgutils.transform as st
from PIL import Image

import imagegen
import utils

# number of rows/columns of cards on a page
page_size = 3
cards_per_page = page_size ** 2

# get all cards and split into pages
cards = utils.get_all_cards()
pages = [cards[i:i+cards_per_page] for i in range(0, len(cards), cards_per_page)]

buffer = io.BytesIO()
imgs = []

for i in range(len(pages)):
    pngs = [imagegen.gen_png(card, 0) for card in pages[i]]
    img = Image.open(io.BytesIO(resvg_py.svg_to_bytes(st.fromfile("pdf-background.svg").to_str().decode())))

    for col in range(page_size):
        for row in range(page_size):
            i = row * 3 + col
            if i >= len(pngs):
                break
            img.paste(
                Image.open(io.BytesIO(pngs[i])),
                (int(img.width / 3 * col), int(img.height / 3 * row))
            )

    imgs.append(img)

imgs[0].save(buffer, format="PDF", save_all=True, append_images=imgs[1:])
with open("cards.pdf", "wb") as f:
    f.write(buffer.getvalue())
