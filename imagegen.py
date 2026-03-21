import math

import svgutils.transform as st
import resvg_py
import config as conf

def hex_string(x):
    return hex(x)[2:].rjust(6, '0')

blank_file = "card-templates/blank.svg"
template_dir_3 = "card-templates/base_3/"
template_dir_4 = "card-templates/base_4/"

# the colors of shapes and borders
colors_3 = [0xff0000, 0x00a000, 0x0000ff, 0x000000] # the last element is the default color
colors_4 = [0xeb0c0c, 0x79de14, 0x27d6d6, 0x8000ff, 0x000000]
border_colors = [0x00e0ff, 0xff00ff, 0xffa000]
background_colors = [0xffffff, 0xa0a0a0, 0x404040]

# whiteness to be applied for shaded cards
whiteness = [1, 128/255, 0]

# cache previously generated pngs
cache = {}

# the number of frames after which all cards will be back to their original state
full_cycle_frames = math.lcm(*[i for i in conf.enabled_dimensions if i != 0])

# generate svg for a given set of properties
def gen_svg_frame_base3(values):
    svg = st.fromfile(blank_file)

    color = values[0]
    shape = values[1]
    number = values[2]
    shading = values[3]
    border_style = values[4]
    border_color = values[5]
    border_number = values[6]
    background_color = values[7]

    # background color
    if background_color is not None:
        svg.append(st.fromstring(st.fromfile(template_dir_3 + "background.svg").to_str().decode().replace(
            "fill:#ffffff",
            "fill:#" + hex_string(background_colors[background_color])
        )))

    # central shape properties
    if color is not None or shape is not None or number is not None or shading is not None:
        if number is None:
            number = 0
        if shape is None:
            shape = 2
        if color is None:
            color = -1
        if shading is None:
            shading = 2
        shade_color = int(colors_3[color] * (1 - whiteness[shading]) + 0xffffff * whiteness[shading])
        fill_opacity = 0 if shade_color == 0xffffff else 1
        svg.append(
            st.fromstring(
                st.fromfile(
                    template_dir_3 + "base" + str(number) + str(shape) + ".svg"
                ).to_str().decode().replace(
                    "stroke:#000000",
                    "stroke:#" + hex_string(colors_3[color])
                ).replace(
                    "fill:#808080;fill-opacity:1",
                    "fill:#" + hex_string(shade_color) + ";fill-opacity:" + str(fill_opacity)
                )
            )
        )

    # border properties
    if border_style is not None or border_color is not None or border_number is not None:
        if border_number is None:
            border_number = 0
        if border_style is None:
            border_style = 0
        if color is None:
            color = -1
        if border_color is None:
            hex_code = colors_3[color]
        else:
            hex_code = border_colors[border_color]
        svg.append(
            st.fromstring(
                st.fromfile(
                    template_dir_3 + "border" + str(border_number) + str(border_style) + ".svg"
                ).to_str().decode().replace(
                    "stroke:#ff00ff",
                    "stroke:#" + hex_string(hex_code)
                )
            )
        )

    return svg

def gen_svg_frame_base4(values):
    color = values[0]
    shape = values[1]
    number = values[2]
    pattern = values[3]

    if number is None:
        number = 0
    if shape is None:
        shape = 0
    if color is None:
        color = -1
    if pattern is None:
        pattern = 3

    with open(template_dir_4 + str(pattern) + "/" + str(number) + str(shape) + ".svg") as f:
        svg_str = f.read().replace(
            "#000000",
            "#" + hex_string(colors_4[color])
        )

    return st.fromstring(svg_str)

# generate svg for a card at a given frame in time
def gen_svg(card, frame):
    values = [None] * len(conf.enabled_dimensions)
    j = 0
    for i in range(len(values)):
        n = conf.enabled_dimensions[i]
        if n == 0:
            continue
        values[i] = card[j + (frame % n)]
        j += n

    if conf.base == 3:
        return gen_svg_frame_base3(values)
    elif conf.base == 4:
        return gen_svg_frame_base4(values)
    return st.fromfile(blank_file)

# generate png for a card at a given frame in time
def gen_png(card, frame):
    if card is None:
        svg = st.fromfile(blank_file)
        png = resvg_py.svg_to_bytes(svg.to_str().decode())
        return png

    frame = frame % full_cycle_frames
    card_id = 0
    for i in range(len(card)):
        card_id += card[i] * (conf.base ** i)

    if card_id in cache:
        if frame in cache[card_id]:
            return cache[card_id][frame]
        else:
            svg = gen_svg(card, frame)
            png = resvg_py.svg_to_bytes(svg.to_str().decode())
            cache[card_id][frame] = png
            return png
    else:
        svg = gen_svg(card, frame)
        png = resvg_py.svg_to_bytes(svg.to_str().decode())
        cache[card_id] = {frame: png}
        return png
