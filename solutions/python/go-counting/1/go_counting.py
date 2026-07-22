from collections import deque


# 测试要求导出的三个领地所有者常量。
BLACK = "B"
WHITE = "W"
NONE = ""

# deque 是双端队列。
#
# BFS 需要：
# 从队列右边加入新位置 append()
# 从队列左边取出旧位置 popleft()
from collections import deque


class Board:
    """计算围棋棋盘上每位玩家的领地。

    Args:
        board (list[str]): 二维围棋棋盘。
                          "B" 表示黑棋。
                          "W" 表示白棋。
                          " " 表示空交叉点。
    """

    def __init__(self, board):
        # 保存完整棋盘。
        #
        # board 中的每个字符串代表棋盘的一行。
        self.board = board

    def territory(self, x, y):
        """查询指定坐标所在的领地。

        Args:
            x (int): 列坐标。
            y (int): 行坐标。

        Returns:
            tuple[str, set]:
                第一个元素是领地所有者："B"、"W" 或 ""。
                第二个元素是该区域包含的所有空白坐标。
        """

        # 首先判断行坐标 y 是否超出棋盘范围。
        if y < 0 or y >= len(self.board):
            raise ValueError("Invalid coordinate")

        # 然后判断列坐标 x 是否超出当前行的范围。
        if x < 0 or x >= len(self.board[y]):
            raise ValueError("Invalid coordinate")

        # 领地只能由空白交叉点组成。
        #
        # 如果指定坐标上是黑棋或白棋，
        # 就没有可以从这里开始搜索的领地。
        if self.board[y][x] != " ":
            return "", set()

        # area 保存这次洪水填充到达的所有空格。
        #
        # 它还可以防止同一个空格被重复加入队列。
        area = {(x, y)}

        # borders 保存这片空地碰到的棋子颜色。
        #
        # 最终可能是：
        # {"B"}      → 黑方领地
        # {"W"}      → 白方领地
        # {"B", "W"} → 中立区域
        # set()      → 中立区域
        borders = set()

        # 创建 BFS 队列，并把起始空格放进去。
        #
        # 可以把它理解为：
        # 第一滴水已经落在坐标 (x, y) 上。
        queue = deque([(x, y)])

        # 队列不为空，说明还有水刚刚到达的位置需要继续扩散。
        while queue:
            # 从队列最左边取出最早加入的位置。
            #
            # 这保证了水会一层一层向外扩散，
            # 而不是沿着某个方向一直走到底。
            current_x, current_y = queue.popleft()

            # 当前空格的四个相邻位置。
            #
            # 只允许上下左右扩散，不允许斜着扩散。
            neighbors = [
                (current_x - 1, current_y),  # 左
                (current_x + 1, current_y),  # 右
                (current_x, current_y - 1),  # 上
                (current_x, current_y + 1),  # 下
            ]

            # 检查当前空格四周的每个位置。
            for neighbor_x, neighbor_y in neighbors:
                # 如果 y 超出了棋盘范围，
                # 说明水碰到了棋盘的上边缘或下边缘。
                #
                # 棋盘边缘只让水停止，不记录任何颜色。
                if neighbor_y < 0 or neighbor_y >= len(self.board):
                    continue

                # 如果 x 超出了当前行的范围，
                # 说明水碰到了棋盘的左边缘或右边缘。
                if (
                    neighbor_x < 0
                    or neighbor_x >= len(self.board[neighbor_y])
                ):
                    continue

                # 读取相邻位置上的内容。
                neighbor_value = self.board[neighbor_y][neighbor_x]
                neighbor_coordinate = (neighbor_x, neighbor_y)

                # 如果相邻位置是空格，水可以继续流过去。
                if neighbor_value == " ":
                    # 只有尚未到达的空格才需要加入队列。
                    #
                    # 如果不检查，两个相邻空格可能不断把彼此
                    # 加回队列，造成重复搜索。
                    if neighbor_coordinate not in area:
                        # 在加入队列时立即记录这个坐标，
                        # 防止其他方向再次把它加入队列。
                        area.add(neighbor_coordinate)

                        # 把新空格放到队列末尾。
                        #
                        # 等前面这一层处理完，再从这里继续扩散。
                        queue.append(neighbor_coordinate)

                # 如果碰到黑棋或白棋，水不能继续前进，
                # 但需要记录这块棋子的颜色。
                elif neighbor_value in {"B", "W"}:
                    borders.add(neighbor_value)

        # BFS 完成后：
        #
        # area 保存水覆盖的整片空地；
        # borders 保存这片空地接触到的棋子颜色。

        # 只有当边界棋子的颜色集合里恰好有一种颜色时，
        # 这片区域才属于某位玩家。
        if len(borders) == 1:
            # borders 中只有一个元素，
            # 使用 next(iter(...)) 取出这个颜色。
            owner = next(iter(borders))

        else:
            # 如果同时碰到 B 和 W，这片区域是中立区域。
            #
            # 如果没有碰到任何棋子，只有棋盘边缘，
            # 这片区域同样是中立区域。
            owner = ""

        return owner, area

    def territories(self):
        """计算整个棋盘的所有领地。

        Returns:
            dict[str, set]:
                "B" 保存所有黑方领地坐标。
                "W" 保存所有白方领地坐标。
                "" 保存所有中立区域坐标。
        """

        # 创建最终结果字典。
        #
        # 即使某一类没有任何坐标，
        # 也要保留对应的空集合。
        result = {
            "B": set(),
            "W": set(),
            "": set(),
        }

        # visited 保存已经被某次 BFS 搜索过的空格。
        #
        # 同一片连通区域只需要搜索一次。
        visited = set()

        # 按照从上到下的顺序遍历棋盘。
        for y, row in enumerate(self.board):
            # 按照从左到右的顺序遍历当前行。
            for x, value in enumerate(row):
                coordinate = (x, y)

                # 黑棋和白棋本身不是领地。
                #
                # 只有空格才需要进行洪水填充。
                if value != " ":
                    continue

                # 如果这个空格已经在之前找到的区域中，
                # 就不需要再次搜索。
                if coordinate in visited:
                    continue

                # 从当前空格开始进行一次 BFS 洪水填充。
                owner, area = self.territory(x, y)

                # 将整片区域标记为已经处理。
                visited.update(area)

                # 按照区域所有者，把所有坐标放进相应集合。
                #
                # owner 可能是 "B"、"W" 或 ""。
                result[owner].update(area)

        return result