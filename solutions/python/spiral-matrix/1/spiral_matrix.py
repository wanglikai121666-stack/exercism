def rotate_counterclockwise(matrix):
    """把矩阵逆时针旋转 90 度。"""
    size = len(matrix)
    rotated = [[0] * size for _ in range(size)]

    for row in range(size):
        for column in range(size):
            rotated[size - 1 - column][row] = matrix[row][column]

    return rotated


def rotate_clockwise(matrix):
    """把矩阵顺时针旋转 90 度。"""
    size = len(matrix)
    rotated = [[0] * size for _ in range(size)]

    for row in range(size):
        for column in range(size):
            rotated[column][size - 1 - row] = matrix[row][column]

    return rotated


def spiral_matrix(size):
    if size == 0:
        return []

    matrix = [[0] * size for _ in range(size)]

    row = 0
    column = 0

    rotation_count = 0

    for number in range(1, size * size + 1):
        # 填写当前格子
        matrix[row][column] = number

        # 最后一个数字填完后，不再寻找下一格
        if number == size * size:
            break

        next_column = column + 1

        # 右边没有越界，而且还是空位
        if (
            next_column < size
            and matrix[row][next_column] == 0
        ):
            column = next_column

        else:
            # 记录旋转前的当前位置
            old_row = row
            old_column = column

            # 矩阵逆时针旋转
            matrix = rotate_counterclockwise(matrix)
            rotation_count += 1

            # 当前格子旋转后的新位置
            row = size - 1 - old_column
            column = old_row

            # 旋转以后继续向右走一格
            column += 1

    # 把矩阵恢复到最开始的方向
    for _ in range(rotation_count % 4):
        matrix = rotate_clockwise(matrix)

    return matrix