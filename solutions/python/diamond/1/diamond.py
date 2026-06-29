ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def rows(letter):
    if letter=="A":
        return ["A"]
    end_index = ALPHABET.index(letter)
    width = 2 * end_index + 1
    top_letters = ALPHABET[:end_index + 1]
    bottom_letters = ALPHABET[end_index - 1::-1]
    all_letters= top_letters + bottom_letters
    result =[]
    for char in all_letters:
        if char == "A":
            line = char.center(width)
        else:
            char_index = ALPHABET.index(char)
            outer_spaces = end_index - char_index
            inner_spaces = 2 * char_index - 1
            line = (
                " " * outer_spaces
                + char
                + " " * inner_spaces
                + char
                + " " * outer_spaces
            )
        result.append(line)
    return result