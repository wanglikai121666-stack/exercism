import random
import string

class Cipher:
    def __init__(self, key=None):
        if key is None:
            self.key = "".join(
                random.choice(string.ascii_lowercase) for _ in range(100)
            )
        else:
            self.key = key
            

    def encode(self, text):
        result = []
        base = ord("a")
        for index, char in enumerate(text):
            key_char = self.key[index % len(self.key)]

            char_index = ord(char) - base
            key_shift = ord(key_char) - base

            new_index = (char_index + key_shift) % 26
            new_char = chr(base + new_index)

            result.append(new_char)

        return "".join(result)
            

    def decode(self, text):
        result = []
        base = ord("a")
        for index, char in enumerate(text):
            key_char = self.key[index % len(self.key)]

            char_index = ord(char) - base
            key_shift = ord(key_char) - base

            new_index = (char_index - key_shift) % 26
            new_char = chr(base + new_index)

            result.append(new_char)

        return "".join(result)
