NUMBERS = {
    0: "no",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}
def bottle_phrase(number):
    bottle_word = "bottle" if number == 1 else "bottles"
    return f"{NUMBERS[number]} green {bottle_word}"
def capitalize_first(text):
    return text[0].upper() + text[1:]
def recite(start, take=1):
    lyrics = []
    for i in range(take):
        current = start - i
        next_count = current - 1

        current_phrase = capitalize_first(bottle_phrase(current))
        next_phrase = bottle_phrase(next_count)

        lyrics.append(f"{current_phrase} hanging on the wall,")
        lyrics.append(f"{current_phrase} hanging on the wall,")
        lyrics.append("And if one green bottle should accidentally fall,")
        lyrics.append(f"There'll be {next_phrase} hanging on the wall.")

        if i != take - 1:
            lyrics.append("")

    return lyrics
