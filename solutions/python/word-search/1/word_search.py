class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class WordSearch:
    def __init__(self, puzzle):
        # puzzle 是字母网格，例如：
        # ["abc", "def", "ghi"]
        self.puzzle = puzzle

        # 网格的行数
        self.height = len(puzzle)

        # 网格的列数；题目通常保证每一行一样长
        self.width = len(puzzle[0]) if puzzle else 0

    def search(self, word):
        # 8 个方向。
        # 每组数字是 (x 的变化量, y 的变化量)：
        # (1, 0)  向右
        # (-1, 0) 向左
        # (0, 1)  向下
        # (0, -1) 向上
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]

        # 依次把网格中的每个位置当作单词起点
        for start_y in range(self.height):
            for start_x in range(self.width):

                # 起点的字母都不一样，就不用再试 8 个方向
                if self.puzzle[start_y][start_x] != word[0]:
                    continue

                # 从这个起点尝试八个方向
                for dx, dy in directions:
                    # 根据单词长度，算出最后一个字母的位置。
                    # len(word) - 1 是因为起点已经算第一个字母。
                    end_x = start_x + dx * (len(word) - 1)
                    end_y = start_y + dy * (len(word) - 1)

                    # 终点超出网格，说明这个方向放不下完整单词
                    if not (0 <= end_x < self.width and
                            0 <= end_y < self.height):
                        continue

                    # 假设该方向匹配；逐个字母检查
                    matches = True

                    for index in range(len(word)):
                        # 当前要检查的网格坐标
                        current_x = start_x + dx * index
                        current_y = start_y + dy * index

                        # 网格里对应位置的字母不相同，就失败
                        if self.puzzle[current_y][current_x] != word[index]:
                            matches = False
                            break

                    # 所有字母都匹配，返回起点与终点
                    if matches:
                        return (
                            Point(start_x, start_y),
                            Point(end_x, end_y),
                        )

        # 全部位置和方向都找完，仍未找到单词
        return None