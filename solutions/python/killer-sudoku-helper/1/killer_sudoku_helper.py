from itertools import combinations as digit_combinations


def combinations(target, size, exclude):
    # 1 到 9 中，排除不能使用的数字
    available_digits = [
        digit
        for digit in range(1, 10)
        if digit not in exclude
    ]

    # 保存所有合法组合
    result = []

    # 使用别名 digit_combinations，避免和本函数重名
    for group in digit_combinations(available_digits, size):

        # group 例如是 (2, 8)
        # 只有总和等于 target 才能加入结果
        if sum(group) == target:

            # 转成列表： (2, 8) -> [2, 8]
            result.append(list(group))

    # 组合本身已经按从小到大生成；再排序保证结果稳定
    return sorted(result)