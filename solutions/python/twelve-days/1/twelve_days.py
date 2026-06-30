
def recite(start_verse, end_verse):
    days = [
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "eleventh",
        "twelfth",
    ]

    gifts = [
        "a Partridge in a Pear Tree",
        "two Turtle Doves",
        "three French Hens",
        "four Calling Birds",
        "five Gold Rings",
        "six Geese-a-Laying",
        "seven Swans-a-Swimming",
        "eight Maids-a-Milking",
        "nine Ladies Dancing",
        "ten Lords-a-Leaping",
        "eleven Pipers Piping",
        "twelve Drummers Drumming",
    ]
    result = []
    for verse_number in range(start_verse, end_verse + 1):
        day = days[verse_number - 1]
        verse = "On the " + day + " day of Christmas my true love gave to me: "
        gift_part = ""
        for gift_index in range(verse_number - 1, -1, -1):
            gift = gifts[gift_index]
            if gift_index == 0 and verse_number > 1:
                gift = "and " + gift
            if gift_part == "":
                gift_part = gift
            else:
                gift_part = gift_part + ", " + gift
        verse = verse + gift_part + "."
        result.append(verse)
    return result