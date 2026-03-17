import subprocess
from PyPDF2 import PdfMerger

import imagegen
import utils

cards = utils.get_all_cards()
merger = PdfMerger()

for i in range(len(cards)):
    print(f"{i+1}/{len(cards)}")
    svg = imagegen.gen_svg(cards[i], 0)
    svg.save(f"temp/card{i}.svg")
    subprocess.run(rf'"C:\Program Files\Inkscape\bin\inkscape.com" temp\card{i}.svg --export-type=pdf --export-filename=temp\card{i}.pdf')
    merger.append(f"temp\card{i}.pdf")

merger.write("cards.pdf")
merger.close()
