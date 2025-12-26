import svgutils.compose as sc
import svgutils.transform as st
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfMerger

import imagegen
import utils

# number of rows/columns of cards on a page
page_size = 3
cards_per_page = page_size ** 2

# get all cards and split into pages
cards = utils.get_all_cards()
pages = [cards[i:i+cards_per_page] for i in range(0, len(cards), cards_per_page)]

merger = PdfMerger()
for i in range(len(pages)):
    svgs = [sc.Element(imagegen.gen_svg_frame(card).getroot().root) for card in pages[i]]
    grid_fig = sc.Figure(297.5 * 3, 421 * 3, *svgs)
    grid_fig.tile(page_size, page_size)
    fig = sc.Figure(
        297.5 * 3, 421 * 3,
        sc.Element(st.fromstring(grid_fig.tostr().decode()).getroot().root),
        sc.SVG("pdf-background.svg")
    )
    fig.save("temp/page" + str(i) + ".svg")
    renderPDF.drawToFile(svg2rlg("temp/page" + str(i) + ".svg"), "temp/page" + str(i) + ".pdf")
    merger.append("temp/page" + str(i) + ".pdf")

merger.write("cards.pdf")
merger.close()
