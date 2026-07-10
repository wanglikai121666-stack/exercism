def rebase(input_base, digits, output_base):
    # 输入进制必须至少是 2
    #
    # 因为一进制、零进制和负数进制
    # 不属于这道题要求处理的普通进制
    if input_base < 2:
        raise ValueError("input base must be >= 2")

    # 输出进制也必须至少是 2
    if output_base < 2:
        raise ValueError("output base must be >= 2")

    # 检查 digits 中的每一位是否合法
    #
    # 例如：
    # 二进制中，每一位只能是 0 或 1
    # 三进制中，每一位只能是 0、1 或 2
    for digit in digits:
        if digit < 0 or digit >= input_base:
            raise ValueError(
                "all digits must satisfy 0 <= d < input base"
            )
     # 第一步：
    # 把 input_base 进制的数字转换成普通整数
    decimal_value = 0

    for digit in digits:
        # 每读入一位：
        # 先把当前结果乘以 input_base
        # 再加上当前这一位
        #
        # 例如二进制 101：
        # 0 × 2 + 1 = 1
        # 1 × 2 + 0 = 2
        # 2 × 2 + 1 = 5
        decimal_value = decimal_value * input_base + digit
     # 如果原数字是 0，
    # 目标进制下仍然应该表示为 [0]
    #
    # 例如：
    # rebase(10, [0], 2)
    # 应该返回 [0]
    if decimal_value == 0:
        return [0]

    # 第二步：
    # 把普通整数转换成 output_base 进制
    result = []

    while decimal_value > 0:
        # % 得到除法余数
        remainder = decimal_value % output_base

        # 余数就是目标进制中的一位
        result.append(remainder)

        # // 是整除，只保留整数商
        decimal_value = decimal_value // output_base

    # 余数是从最低位开始得到的，
    # 所以当前 result 顺序是反的
    #
    # reverse() 会直接把列表反转
    result.reverse()

    return result