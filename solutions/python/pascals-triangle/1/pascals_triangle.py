def rows(row_count):
    # 如果传入负数，按题目要求抛出 ValueError
    if row_count < 0:
        raise ValueError("number of rows is negative")

    # 递归的基础情况：
    # 如果要求 0 行，就返回空列表
    if row_count == 0:
        return []

    # 如果要求 1 行，帕斯卡三角只有第一行 [1]
    if row_count == 1:
        return [[1]]

    # 先递归生成前 row_count - 1 行
    # 例如 rows(5) 会先计算 rows(4)
    triangle = rows(row_count - 1)

    # 取出当前三角形的最后一行
    # 后面要根据这一行计算新的一行
    previous_row = triangle[-1]

    # 计算上一行中所有相邻数字的和
    #
    # 例如上一行是：
    # [1, 3, 3, 1]
    #
    # 会计算：
    # 1 + 3 = 4
    # 3 + 3 = 6
    # 3 + 1 = 4
    #
    # 最终得到：
    # [4, 6, 4]
    middle_values = [
        previous_row[index] + previous_row[index + 1]
        for index in range(len(previous_row) - 1)
    ]

    # 帕斯卡三角每一行的最左边和最右边都是 1
    #
    # 所以把左右两个 1 加到中间数字两侧
    # [1] + [4, 6, 4] + [1]
    # 得到 [1, 4, 6, 4, 1]
    new_row = [1] + middle_values + [1]

    # 把新的一行添加到之前生成的三角形中
    #
    # 注意这里要写 [new_row]
    # 因为 triangle 是一个“行列表组成的列表”
    return triangle + [new_row]