# 判断一个数字是不是回文数
def is_palindrome(number):
    # 把数字转成字符串
    text = str(number)

    # 正着读和倒着读一样，就是回文
    return text == text[::-1]


# 寻找最大的回文乘积
def largest(max_factor, min_factor=0):
    # 范围不合法时抛出异常
    if min_factor > max_factor:
        raise ValueError("min must be <= max")

    # 当前找到的最大回文数
    largest_value = None

    # 最大回文数对应的全部因数对
    factors = []

    # 从大到小遍历第一个因数
    for first in range(max_factor, min_factor - 1, -1):

        # 如果 first * first 已经小于当前最大值
        # 后面更小的 first 更不可能产生更大的答案
        if largest_value is not None and first * first < largest_value:
            break

        # second 不超过 first，避免重复记录
        # 例如只记录 (9, 1)，不再记录 (1, 9)
        for second in range(first, min_factor - 1, -1):
            product = first * second

            # second 继续变小时，product 只会更小
            # 如果已经小于当前答案，就不必继续这一轮
            if largest_value is not None and product < largest_value:
                break

            # 如果不是回文数，检查下一个乘积
            if not is_palindrome(product):
                continue

            # 第一次找到回文数，或者找到了更大的回文数
            if largest_value is None or product > largest_value:
                largest_value = product

                # 找到更大的值后，之前的因数对全部作废
                factors = [(first, second)]

            # 如果和当前最大回文数相等
            # 就把另一组因数也保存下来
            elif product == largest_value:
                factors.append((first, second))

    # 没有找到任何回文乘积
    if largest_value is None:
        return None, []

    return largest_value, factors


# 寻找最小的回文乘积
def smallest(max_factor, min_factor=0):
    # 范围不合法时抛出异常
    if min_factor > max_factor:
        raise ValueError("min must be <= max")

    # 当前找到的最小回文数
    smallest_value = None

    # 最小回文数对应的全部因数对
    factors = []

    # 从小到大遍历第一个因数
    for first in range(min_factor, max_factor + 1):

        # 如果 first * first 已经大于当前最小值
        # 后面的 first 更大，不可能再得到相同或更小的答案
        if smallest_value is not None and first * first > smallest_value:
            break

        # 从 first 开始，避免同时记录 (1, 9) 和 (9, 1)
        for second in range(first, max_factor + 1):
            product = first * second

            # second 越来越大，乘积也越来越大
            # 已经超过当前最小值时，可以结束这一轮
            if smallest_value is not None and product > smallest_value:
                break

            # 如果不是回文数，继续检查
            if not is_palindrome(product):
                continue

            # 第一次找到回文数，或者找到了更小的回文数
            if smallest_value is None or product < smallest_value:
                smallest_value = product

                # 更换最小值后，之前保存的因数对作废
                factors = [(first, second)]

            # 如果等于当前最小回文数
            # 保存这组额外的因数
            elif product == smallest_value:
                factors.append((first, second))

    # 没有任何回文乘积
    if smallest_value is None:
        return None, []

    return smallest_value, factors