class Allergies:
    ALLERGENS = [
        "eggs",
        "peanuts",
        "shellfish",
        "strawberries",
        "tomatoes",
        "chocolate",
        "pollen",
        "cats",
    ]

    def __init__(self, score):
        self.score = score

    def allergic_to(self, item):
        return item in self.lst

    @property
    def lst(self):
        result = []

        bits = list(bin(self.score)[2:])
        index = 0

        while bits and index < len(self.ALLERGENS) :
            bit = bits.pop()

            if bit == "1":
                result.append(self.ALLERGENS[index])

            index += 1

        return result
