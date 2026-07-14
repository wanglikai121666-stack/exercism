def largest_product(series, size):
    # 如果 size 是负数，输入无效
    if size < 0:
        raise ValueError("span must not be negative")

    # 如果 size 比数字字符串还长，无法截取
    if size > len(series):
        raise ValueError("span must not exceed string length")

    # 如果字符串中存在非数字字符，输入无效
    if not series.isdigit() and series != "":
        raise ValueError("digits input must only contain digits")

    # 长度为 0 的序列，乘积规定为 1
    if size == 0:
        return 1

    # 保存目前找到的最大乘积
    largest = 0

    # 依次确定每个连续片段的开始位置
    for start in range(len(series) - size + 1):
        # 截取长度为 size 的连续数字
        current_series = series[start:start + size]

        # 当前连续片段的乘积，初始值必须是 1
        product = 1

        # 遍历当前片段中的每个字符
        for digit in current_series:
            # digit 是字符串，需要转成整数再相乘
            product *= int(digit)

        # 如果当前乘积更大，就更新 largest
        if product > largest:
            largest = product

    # 返回最大的乘积
    return largest