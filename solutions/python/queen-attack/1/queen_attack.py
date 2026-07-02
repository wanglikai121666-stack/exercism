class Queen:
    def __init__(self, row, column):
        if row < 0:
            raise ValueError("row not positive")

        if row > 7:
            raise ValueError("row not on board")

        if column < 0:
            raise ValueError("column not positive")

        if column > 7:
            raise ValueError("column not on board")

        self.row = row
        self.column = column


    def can_attack(self, another_queen):
        if self.row == another_queen.row and self.column == another_queen.column:
            raise ValueError("Invalid queen position: both queens in the same square")
        board = []
        for row in range(8):
            line = []
            for column in range(8):
                line.append("")
            board.append(line)
        board[self.row][self.column] = "queen"
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        for row_step, column_step in directions:
            current_row = self.row + row_step
            current_column = self.column + column_step
            while 0 <= current_row < 8 and 0 <= current_column < 8:
                board[current_row][current_column] = "attack"

                current_row += row_step
                current_column += column_step
        return board[another_queen.row][another_queen.column] == "attack"
