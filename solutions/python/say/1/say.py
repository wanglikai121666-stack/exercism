SMALL = {
    0: "zero",
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
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}
TENS = {
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}
def say_under_1000(number):
    if number < 20:
        return SMALL[number]
    if number < 100:
        tens = number // 10 * 10
        ones = number % 10
        if ones == 0:
            return TENS[tens]
        return TENS[tens] + "-" + SMALL[ones]
    hundreds = number // 100
    rest = number % 100
    if rest == 0:
        return SMALL[hundreds] + " hundred"
    return SMALL[hundreds] + " hundred " + say_under_1000(rest)
def say(number):
    if number < 0 or number > 999_999_999_999:
        raise ValueError("input out of range")
    if number == 0:
        return "zero"
    chunks = [
        (1_000_000_000, "billion"),
        (1_000_000, "million"),
        (1_000, "thousand"),
        (1, ""),
    ]
    result = []
    for value, name in chunks:
        chunk = number // value
        number = number % value
        if chunk == 0:
            continue
        words = say_under_1000(chunk)
        if name:
            words = words + " " + name
        result.append(words)
    return " ".join(result)
