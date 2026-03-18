import io

import resvg_py
import svgutils.transform as st
from PIL import Image
from PyPDF2 import PdfMerger
import svgutils.compose as sc
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pathlib import Path
from playwright.sync_api import sync_playwright

import imagegen
import utils

# number of rows/columns of cards on a page
page_size = 3
cards_per_page = page_size ** 2

def gen_pdf_from_pngs():
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

def gen_pdf_from_svgs():
    # get all cards and split into pages
    cards = utils.get_all_cards()
    pages = [cards[i:i + cards_per_page] for i in range(0, len(cards), cards_per_page)]

    merger = PdfMerger()
    for i in range(len(pages)):
        svgs = [sc.Element(imagegen.gen_svg(card, 0).getroot().root) for card in pages[i]]

        grid_fig = sc.Figure(297.5 * 3, 421 * 3, *svgs)
        grid_fig.tile(page_size, page_size)
        fig = sc.Figure(
            297.5 * 3, 421 * 3,
            sc.Element(st.fromstring(grid_fig.tostr().decode()).getroot().root),
            sc.SVG("pdf-background.svg")
        )
        fig.save("temp/page" + str(i) + ".svg")

        svg_file = Path("temp/page" + str(i) + ".svg").resolve()
        pdf_file = Path("temp/page" + str(i) + ".pdf").resolve()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{svg_file}")
            page.pdf(path=str(pdf_file), width=f"{fig.width}", height=f"{fig.height}")
            browser.close()

        merger.append("temp/page" + str(i) + ".pdf")

    merger.write("cards.pdf")
    merger.close()


def gen_pdf_new():
    cards = utils.get_all_cards()
    pages_html = ""

    for card in cards:
        svg = imagegen.gen_svg(card, 0)
        svg_str = svg.to_str().decode()

        pages_html += f"""
            <div class="page">
            {svg_str}
            </div>
        """

    html = f"""
        <html>
        <head>
        <style>
        @page {{
          margin: 0;
        }}
        body {{
          margin: 0;
        }}
        .page {{
          page-break-after: always;
        }}
        svg {{
          display: block;
          width: 100%;
          height: auto;
        }}
        </style>
        </head>
        <body>
        {pages_html}
        </body>
        </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html)
        page.pdf(path="cards.pdf")
        browser.close()

gen_pdf_new()
