import svgutils.transform as st
import resvg_py
import config as conf

def hex_string(x):
    return hex(x)[2:].rjust(6, '0')

blank_file = "card-templates/blank.svg"
template_dir_3 = "card-templates/base_3/"
template_dir_4 = "card-templates/base_4/"

# the colors of shapes and borders
colors = [0xff0000, 0x00a000, 0x0000ff, 0xa000ff, 0x000000] # the last element is the default color
border_colors = [0x00e0ff, 0xff00ff, 0xffa000]
background_colors = [0xffffff, 0xa0a0a0, 0x404040]

# whiteness to be applied for shaded cards
whiteness = [1, 128/255, 0]

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
        shade_color = int(colors[color] * (1 - whiteness[shading]) + 0xffffff * whiteness[shading])
        fill_opacity = 0 if shade_color == 0xffffff else 1
        svg.append(
            st.fromstring(
                st.fromfile(
                    template_dir_3 + "base" + str(number) + str(shape) + ".svg"
                ).to_str().decode().replace(
                    "stroke:#000000",
                    "stroke:#" + hex_string(colors[color])
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
            hex_code = colors[color]
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
    svg = st.fromfile(blank_file)

    color = values[0]
    shape = values[1]
    number = values[2]
    pattern = values[3]

    if number is None:
        number = 0
    if shape is None:
        shape = 2
    if color is None:
        color = -1

    if pattern == 0:
        fill_string = "#ffffff"
    elif pattern == 1:
        fill_string = "url(#pattern_stripes)"
    elif pattern == 2:
        fill_string = "url(#pattern_spots)"
    else:
        fill_string = "#" + hex_string(colors[color])

    svg.append(
        st.fromstring(
            st.fromfile(
                template_dir_4 + "test_" + str(number+1) + ".svg"
            ).to_str().decode().replace(
                "stroke:#000000",
                "stroke:#" + hex_string(colors[color])
            ).replace(
                "fill:#808080",
                "fill:" + fill_string
            ).replace(
                "fill:#000000",
                "fill:#" + hex_string(colors[color])
            )
        )
    )

    return svg

# generate svg for a card at a given frame in time
def gen_svg(card, frame):
    if card is None:
        return st.fromfile(blank_file)

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
    svg = gen_svg(card, frame)
    return resvg_py.svg_to_bytes(svg.to_str().decode())