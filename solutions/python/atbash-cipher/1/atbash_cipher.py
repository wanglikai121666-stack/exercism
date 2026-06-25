ALPHABET = "abcdefghijklmnopqrstuvwxyz"
REVERSED_ALPHABET = ALPHABET[::-1]
def convert(text):
    result=""
    for char in text.lower():
        if char in ALPHABET:
            index = ALPHABET.index(char)
            result += REVERSED_ALPHABET[index]
        elif char.isdigit():
             result += char
    return result

def encode(plain_text):
    converted = convert(plain_text)
    groups = []
    for index in range(0, len(converted), 5):
        groups.append(converted[index:index + 5])
    return " ".join(groups)


def decode(ciphered_text):
    converted = convert(ciphered_text)
    return converted
