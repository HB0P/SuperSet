import svgutils.transform as st
import utils

cache = {}

def hex_string(x):
    return hex(x)[2:].rjust(6, '0')

def apply_background_color(svg, background_color, __):
    if background_color is not None:
        svg.append(st.fromstring(st.fromfile(template_dir + "background.svg").to_str().decode().replace(
            "fill:#ffffff",
            "fill:#" + hex_string(background_colors[background_color])
        )))
    return svg, None

def apply_number(svg, number, __):
    if number is None:
        number = 0
    return svg, number

def apply_shape(svg, shape, number):
    if shape is None:
        shape = 2
    svg.append(st.fromfile(template_dir + "base" + str(number) + str(shape) + ".svg"))
    return svg, None

def apply_border_number(svg, border_number, _):
    if border_number is None:
        border_number = 0
    return svg, border_number

def apply_border_style(svg, border_style, border_number):
    if border_style is not None:
        svg.append(st.fromfile(template_dir + "border" + str(border_number) + str(border_style) + ".svg"))
    return svg, None

def apply_color(svg, color, _):
    return st.fromstring(svg.to_str().decode().replace(
        "stroke:#000000",
        "stroke:#" + hex_string(colors[color])
    )), color

def apply_border_color(svg, border_color, color):
    if border_color is None:
        hex_code = colors[color]
    else:
        hex_code = border_colors[border_color]
    return st.fromstring(svg.to_str().decode().replace(
        "stroke:#ff00ff",
        "stroke:#" + hex_string(hex_code)
    )), color

def apply_shading(svg, shading, color):
    if shading is None:
        shading = 2
    shade_color = int(colors[color] * (1-whiteness[shading]) + 0xffffff * whiteness[shading])
    fill_opacity = 0 if shade_color == 0xffffff else 1
    return st.fromstring(svg.to_str().decode().replace(
        "fill:#808080;fill-opacity:1",
        "fill:#" + hex_string(shade_color) + ";fill-opacity:" + str(fill_opacity)
    )), None

template_dir = "card-templates/"

# the 3 colors of cards and borders
colors = [0xff0000, 0x00a000, 0x0000ff]
border_colors = [0x00e0ff, 0xff00ff, 0xffa000]
background_colors = [0xffffff, 0xa0a0a0, 0x404040]

# whiteness to be applied for shaded cards
whiteness = [1, 128/255, 0]

# order in which properties are applied
# 1st element: function to use for applying
# 2nd element: index which the property is at in the card vector
# 3rd element: default value if property is not used
application_order = [
    (apply_background_color, 7),
    (apply_number, 2),
    (apply_shape, 1),
    (apply_border_number, 6),
    (apply_border_style, 4),
    (apply_color, 0),
    (apply_border_color, 5),
    (apply_shading, 3),
]

# generate svg for a card
def gen_svg_frame(card):
    card_hash = utils.hash_card(card)
    if card_hash in cache:
        return cache[card_hash]

    svg, data = st.fromfile(template_dir + "blank.svg"), None
    if card is None:
        cache[card_hash] = svg
        return svg

    for apply in application_order:
        value = card[apply[1]] if apply[1] < len(card) else None
        svg, data = apply[0](svg, value, data)

    cache[card_hash] = svg
    return svg

def gen_svg(card, frame):
    if len(card) <= 8:
        return gen_svg_frame(card)

    if len(card) % 2 == 0:
        rate = card[-2]
        first = card[: len(card) // 2 - 1]
        second = card[len(card) // 2 - 1 : -2]
    else:
        rate = card[-1]
        first = card[: len(card) // 2]
        second = card[len(card) // 2 : -1]

    if (frame & (1 << rate)) == 0:
        return gen_svg_frame(first)
    else:
        return gen_svg_frame(second)

