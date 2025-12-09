import svgutils.transform as st
import config as conf

def hex_string(x):
    return hex(x)[2:].rjust(6, '0')

def apply_number(_, num, __):
    return None, num

def apply_color(svg, color, _):
    return st.fromstring(svg.to_str().decode().replace(
        "stroke:#000000",
        "stroke:#" + hex_string(colors[color])
    )), color

def apply_shading(svg, shading, color):
    shade_color = int(colors[color] * (1-whiteness[shading]) + 0xffffff * whiteness[shading])
    return st.fromstring(svg.to_str().decode().replace(
        "fill:#808080",
        "fill:#" + hex_string(shade_color)
    )), None

def apply_shape(_, shape, number):
    return st.fromfile(template_dir + "base" + str(number) + str(shape) + ".svg"), None

def apply_border(svg, border, _):
    svg.append(st.fromfile(template_dir + "border" + str(border) + ".svg"))
    return svg, None

template_dir = "card-templates/"

# the 3 colors of cards
colors = [0xff0000, 0x00a000, 0x0000ff]

# whiteness to be applied for shaded cards
whiteness = [0, 128/255, 1]

# order in which properties are applied
# 1st element: function to use for applying
# 2nd element: index which the property is at in the card vector
# 3rd element: default value if property is not used
application_order = [
    (apply_number, 2, 0),
    (apply_shape, 1, 2),
    (apply_border, 4, 0),
    (apply_color, 0, 0),
    (apply_shading, 3, 2),
]

# generate svg for a card
def gen_svg(card):
    if card is None:
        return st.fromfile(template_dir + "blank.svg")

    svg, data = None, None
    for apply in application_order:
        value = card[apply[1]] if apply[1] < conf.dim else apply[2]
        svg, data = apply[0](svg, value, data)
    return svg
