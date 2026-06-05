COLORS = [
    "black",
    "brown",
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "violet",
    "grey",
    "white",
]


def color_code(color):
    return COLORS.index(color)


def label(colors):
    num = 0
    result = ""

    for color in colors:
        num += 1

        if num <= 2:
            result += str(color_code(color))

        if num > 2:
            value = int(result) * (10 ** color_code(color))

            if value != 0 and value % 1_000_000_000 == 0:
                return f"{value // 1_000_000_000} gigaohms"

            if value != 0 and value % 1_000_000 == 0:
                return f"{value // 1_000_000} megaohms"

            if value != 0 and value % 1_000 == 0:
                return f"{value // 1_000} kiloohms"

            return f"{value} ohms"
