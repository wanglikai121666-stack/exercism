class ConnectGame:
    def __init__(self, board):
        # board 是一个多行字符串，例如：
        #
        # """. . .
        #     . O .
        #      . . ."""
        #
        # splitlines() 会把多行字符串拆成：
        #
        # [
        #     ". . .",
        #     "    . O .",
        #     "     . . ."
        # ]

        lines = board.splitlines()

        # 每一行去掉空格
        # 同时忽略可能存在的空行
        self.board = [
            line.replace(" ", "")
            for line in lines
            if line.strip()
        ]

        # 棋盘行数
        self.rows = len(self.board)

        # 棋盘列数
        self.cols = len(self.board[0]) if self.rows > 0 else 0

        # 六边形棋盘的六个相邻方向
        self.directions = [
            (-1, 0),   # 上
            (1, 0),    # 下
            (0, -1),   # 左
            (0, 1),    # 右
            (-1, 1),   # 右上
            (1, -1),   # 左下
        ]

    def get_winner(self):
        # O 的目标是从最上面连到最下面
        if self._has_connection("O"):
            return "O"

        # X 的目标是从最左边连到最右边
        if self._has_connection("X"):
            return "X"

        # 两个人都没有形成完整连接
        return ""

    def _has_connection(self, player):
        # visited 保存已经访问过的坐标
        #
        # 例如：
        # {(0, 1), (1, 1), (2, 0)}
        #
        # 防止同一个位置被重复搜索，
        # 也防止在两个相邻棋子之间无限来回递归。
        visited = set()

        # O 和 X 的起点不同
        if player == "O":
            # O 从最上面一行开始
            #
            # 找出第 0 行里所有 O 的坐标
            start_positions = []

            for col in range(self.cols):
                if self.board[0][col] == "O":
                    start_positions.append((0, col))

        else:
            # X 从最左边一列开始
            #
            # 找出第 0 列里所有 X 的坐标
            start_positions = []

            for row in range(self.rows):
                if self.board[row][0] == "X":
                    start_positions.append((row, 0))

        # 起始边上可能有多个属于当前玩家的棋子
        # 每个起点都尝试搜索一次
        for start_row, start_col in start_positions:
            if self._dfs(start_row, start_col, player, visited):
                return True

        # 所有起点都走不通
        return False

    def _dfs(self, row, col, player, visited):
        # 如果这个坐标已经访问过，就不要重复搜索
        if (row, col) in visited:
            return False

        # 把当前位置标记为已访问
        visited.add((row, col))

        # 判断是否已经到达玩家的目标边界

        # O 从上往下走
        # 如果 O 已经到达最后一行，就说明 O 获胜
        if player == "O" and row == self.rows - 1:
            return True

        # X 从左往右走
        # 如果 X 已经到达最后一列，就说明 X 获胜
        if player == "X" and col == self.cols - 1:
            return True

        # 遍历当前位置的六个邻居
        for row_change, col_change in self.directions:
            # 计算邻居坐标
            new_row = row + row_change
            new_col = col + col_change

            # 如果邻居超出棋盘范围，就跳过
            if not self._is_inside(new_row, new_col):
                continue

            # 如果邻居不是当前玩家的棋子，也不能继续走
            if self.board[new_row][new_col] != player:
                continue

            # 如果邻居合法并且颜色相同，
            # 就递归进入这个邻居继续搜索
            if self._dfs(new_row, new_col, player, visited):
                return True

        # 六个方向全部走不通
        return False

    def _is_inside(self, row, col):
        # 判断坐标是否在棋盘范围内
        #
        # 行下标必须在 0 到 rows - 1 之间
        # 列下标必须在 0 到 cols - 1 之间
        return 0 <= row < self.rows and 0 <= col < self.cols