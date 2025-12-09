import svgutils.transform as st
import config as conf

def apply_number(_, num, __):
    return None, num

def apply_color(svg, color, _):
    return st.fromstring(svg.to_str().decode().replace(
        "stroke:#000000",
        "stroke:#" + colors[color][2]
    )), color

def apply_shading(svg, shading, color):
    return st.fromstring(svg.to_str().decode().replace(
        "fill:#808080",
        "fill:#" + colors[color][shading]
    )), None

def apply_shape(_, shape, number):
    return st.fromfile(template_dir + "base" + str(number) + str(shape) + ".svg"), None

def apply_border(svg, border, _):
    svg.append(st.fromfile(template_dir + "border" + str(border) + ".svg"))
    return svg, None

template_dir = "card-templates/"

# color and shading
# each array is a color, with elements for empty, shaded, filled
colors = [
    ["ffffff", "808080", "000000"],
    ["ffffff", "ff8080", "ff0000"],
    ["ffffff", "8080ff", "0000ff"]
]

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
