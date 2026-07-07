def gamestate(board):
    x_count = count_marks(board, "X")
    o_count = count_marks(board, "O")
    validate_turn_order(x_count, o_count)
    x_wins = has_won(board, "X")
    o_wins = has_won(board, "O")
    validate_win_state(x_wins, o_wins, x_count, o_count)
    if x_wins or o_wins:
        return "win"

    if is_full(board):
        return "draw"

    return "ongoing"





def count_marks(board, mark):
    count = 0

    for row in board:
        count += row.count(mark)

    return count

def validate_turn_order(x_count, o_count):
    if o_count > x_count:
        raise ValueError("Wrong turn order: O started")

    if x_count > o_count + 1:
        raise ValueError("Wrong turn order: X went twice")

def has_won(board, mark):
    winning_lines = get_winning_lines(board)

    for line in winning_lines:
        if line == [mark, mark, mark]:
            return True

    return False
def get_winning_lines(board):
    rows = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
    ]

    columns = [
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
    ]

    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return rows + columns + diagonals
def is_full(board):
    for row in board:
        if " " in row:
            return False

    return True

    
def validate_win_state(x_wins, o_wins, x_count, o_count):
    if x_wins and o_wins:
        raise ValueError("Impossible board: game should have ended after the game was won")

    if x_wins and x_count != o_count + 1:
        raise ValueError("Impossible board: game should have ended after the game was won")

    if o_wins and x_count != o_count:
        raise ValueError("Impossible board: game should have ended after the game was won")

