def triplets_with_sum(number):
    result = []
    for a in range(1, number // 3 + 1):
        numerator = number * (number - 2 * a)
        denominator = 2 * (number - a)
        # b 必须是整数
        if numerator % denominator != 0:
            continue
        b = numerator // denominator
        c = number - a - b
        if a < b < c and a * a + b * b == c * c:
            result.append([a, b, c])

    return result