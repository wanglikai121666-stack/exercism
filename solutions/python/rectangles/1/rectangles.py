def rectangles(strings):
    # 空输入直接没有矩形
    if not strings:
        return 0
    rows = len(strings)
    cols = len(strings[0])
    count = 0
    # 枚举上边所在行
    for top in range(rows):
        # 枚举下边所在行，必须在 top 下面
        for bottom in range(top + 1, rows):
            # 枚举左边所在列
            for left in range(cols):
                # 枚举右边所在列，必须在 left 右边
                for right in range(left + 1, cols):
                    if is_rectangle(strings, top, bottom, left, right):
                        count += 1

    return count
def is_rectangle(strings, top, bottom, left, right):
    # 四个角必须都是 +
    if strings[top][left] != "+":
        return False

    if strings[top][right] != "+":
        return False

    if strings[bottom][left] != "+":
        return False

    if strings[bottom][right] != "+":
        return False

    # 上边和下边必须是连续横边
    if not is_horizontal_edge(strings, top, left, right):
        return False

    if not is_horizontal_edge(strings, bottom, left, right):
        return False

    # 左边和右边必须是连续竖边
    if not is_vertical_edge(strings, left, top, bottom):
        return False

    if not is_vertical_edge(strings, right, top, bottom):
        return False

    return True

def is_horizontal_edge(strings, row, left, right):
    # 横边上允许出现 + 或 -
    # + 可以是角，也可以是边上的交叉点
    for col in range(left, right + 1):
        if strings[row][col] not in "+-":
            return False

    return True


def is_vertical_edge(strings, col, top, bottom):
    # 竖边上允许出现 + 或 |
    # + 可以是角，也可以是边上的交叉点
    for row in range(top, bottom + 1):
        if strings[row][col] not in "+|":
            return False

    return True