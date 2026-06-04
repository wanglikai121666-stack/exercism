def is_valid(isbn):
    cleaned = isbn.replace("-", "")

    if len(cleaned) != 10:
        return False

    total = 0

    for index in range(10):
        char = cleaned[index]
        weight = 10 - index

        if char == "X":
            if index != 9:
                return False
            value = 10
        elif char.isdigit():
            value = int(char)
        else:
            return False

        total += value * weight

    return total % 11 == 0
