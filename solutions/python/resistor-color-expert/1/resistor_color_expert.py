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

TOLERANCES = {
    "grey": "0.05",
    "violet": "0.1",
    "blue": "0.25",
    "green": "0.5",
    "brown": "1",
    "red": "2",
    "gold": "5",
    "silver": "10",
}


def color_code(color):
    return COLORS.index(color)


def format_value(value):
    if value >= 1_000_000_000:
        number = value / 1_000_000_000
        unit = "gigaohms"
    elif value >= 1_000_000:
        number = value / 1_000_000
        unit = "megaohms"
    elif value >= 1_000:
        number = value / 1_000
        unit = "kiloohms"
    else:
        number = value
        unit = "ohms"

    if number == int(number):
        number = int(number)

    return f"{number} {unit}"

def resistor_label(colors):
    if len(colors) == 1:
        return "0 ohms"
    if len(colors) == 4:
        main = color_code(colors[0]) * 10 + color_code(colors[1])
        multiplier = color_code(colors[2])
        tolerance = TOLERANCES[colors[3]]
    else:
        main = color_code(colors[0]) * 100 + color_code(colors[1]) * 10 + color_code(colors[2])
        multiplier = color_code(colors[3])
        tolerance = TOLERANCES[colors[4]]
    value = main * (10 ** multiplier)
    return f"{format_value(value)} ±{tolerance}%"
