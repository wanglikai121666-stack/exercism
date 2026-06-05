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
def value(colors):
    num=0
    sum=""
    for color in colors :
        num+=1
        if num>2: return int(sum)     
        sum+=str(color_code(color))
    return int(sum)
