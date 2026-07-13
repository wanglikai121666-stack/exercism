def annotate(garden):
    # 空棋盘直接返回空列表
    if not garden:
        return []

    row_count = len(garden)
    column_count = len(garden[0])

    # 检查输入是否合法
    for row in garden:
        # 每一行长度必须相同
        if len(row) != column_count:
            raise ValueError("The board is invalid with current input.")

        # 只能包含空格和 *
        for cell in row:
            if cell not in (" ", "*"):
                raise ValueError("The board is invalid with current input.")

    # 周围 8 个方向
    directions = [
        (-1, -1),  # 左上
        (-1, 0),   # 上
        (-1, 1),   # 右上
        (0, -1),   # 左
        (0, 1),    # 右
        (1, -1),   # 左下
        (1, 0),    # 下
        (1, 1),    # 右下
    ]

    result = []

    # 遍历每一个格子
    for row_index in range(row_count):
        new_row = []

        for column_index in range(column_count):
            current_cell = garden[row_index][column_index]

            # 当前格本身是花，直接保留
            if current_cell == "*":
                new_row.append("*")
                continue

            flower_count = 0

            # 检查周围 8 个位置
            for row_change, column_change in directions:
                nearby_row = row_index + row_change
                nearby_column = column_index + column_change

                # 先判断有没有越界，再判断是不是花
                if (
                    0 <= nearby_row < row_count
                    and 0 <= nearby_column < column_count
                    and garden[nearby_row][nearby_column] == "*"
                ):
                    flower_count += 1

            # 周围没有花，保留空格
            if flower_count == 0:
                new_row.append(" ")
            else:
                new_row.append(str(flower_count))

        result.append("".join(new_row))

    return result