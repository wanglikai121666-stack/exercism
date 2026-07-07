DIGITS = {
    (
        " _ ",
        "| |",
        "|_|",
        "   ",
    ): "0",

    (
        "   ",
        "  |",
        "  |",
        "   ",
    ): "1",

    (
        " _ ",
        " _|",
        "|_ ",
        "   ",
    ): "2",

    (
        " _ ",
        " _|",
        " _|",
        "   ",
    ): "3",

    (
        "   ",
        "|_|",
        "  |",
        "   ",
    ): "4",

    (
        " _ ",
        "|_ ",
        " _|",
        "   ",
    ): "5",

    (
        " _ ",
        "|_ ",
        "|_|",
        "   ",
    ): "6",

    (
        " _ ",
        "  |",
        "  |",
        "   ",
    ): "7",

    (
        " _ ",
        "|_|",
        "|_|",
        "   ",
    ): "8",

    (
        " _ ",
        "|_|",
        " _|",
        "   ",
    ): "9",
}
def convert(input_grid):
    validate_grid(input_grid)
    result_rows = []
    for row_start in range(0, len(input_grid), 4):
        four_rows = input_grid[row_start:row_start + 4]
        result_rows.append(convert_four_rows(four_rows))

    return ",".join(result_rows)



def validate_grid(input_grid):
    if len(input_grid) % 4 != 0:
        raise ValueError("Number of input lines is not a multiple of four")

    if not input_grid:
        return

    expected_width = len(input_grid[0])

    for row in input_grid:
        if len(row) % 3 != 0:
            raise ValueError("Number of input columns is not a multiple of three")

        if len(row) != expected_width:
            raise ValueError("Number of input columns is not a multiple of three")


def convert_four_rows(four_rows):
    digits = []

    width = len(four_rows[0])

    for column_start in range(0, width, 3):
        digit_pattern = get_digit_pattern(four_rows, column_start)
        digit = DIGITS.get(digit_pattern, "?")
        digits.append(digit)

    return "".join(digits)

def get_digit_pattern(four_rows, column_start):
    return (
        four_rows[0][column_start:column_start + 3],
        four_rows[1][column_start:column_start + 3],
        four_rows[2][column_start:column_start + 3],
        four_rows[3][column_start:column_start + 3],
    )
    

