def egg_count(display_value):
    binary = bin(display_value)
    count = 0
    for char in binary:
        if char == "1":
            count += 1
    return count