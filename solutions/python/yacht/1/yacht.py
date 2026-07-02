ONES = 1
TWOS = 2
THREES = 3
FOURS = 4
FIVES = 5
SIXES = 6

YACHT = "yacht"
FULL_HOUSE = "full_house"
FOUR_OF_A_KIND = "four_of_a_kind"
LITTLE_STRAIGHT = "little_straight"
BIG_STRAIGHT = "big_straight"
CHOICE = "choice"


def score(dice, category):
    counts = {}
    if category == ONES:
        return dice.count(1) * 1

    if category == TWOS:
        return dice.count(2) * 2

    if category == THREES:
        return dice.count(3) * 3

    if category == FOURS:
        return dice.count(4) * 4

    if category == FIVES:
        return dice.count(5) * 5

    if category == SIXES:
        return dice.count(6) * 6
    counts = {}

    for die in dice:
        counts[die] = counts.get(die, 0) + 1

    if category == FULL_HOUSE:
        if sorted(counts.values()) == [2, 3]:
            return sum(dice)
        return 0

    if category == FOUR_OF_A_KIND:
        for die, count in counts.items():
            if count >= 4:
                return die * 4
        return 0
    if category == YACHT:
        if len(counts) == 1:
            return 50
    if category == LITTLE_STRAIGHT:
        if sorted(dice) == [1, 2, 3, 4, 5]:
            return 30
        return 0

    if category == BIG_STRAIGHT:
        if sorted(dice) == [2, 3, 4, 5, 6]:
            return 30
        return 0

    if category == CHOICE:
        return sum(dice)
    return 0