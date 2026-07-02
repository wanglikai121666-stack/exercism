def transpose(text):
    rows = text.split("\n")

    row_count = len(rows)

    max_length = 0
    for row in rows:
        if len(row) > max_length:
            max_length = len(row)

    matrix = []

    for row_index in range(row_count):
        matrix_row = []

        for column_index in range(max_length):
            matrix_row.append(None)

        matrix.append(matrix_row)

    for row_index in range(row_count):
        row = rows[row_index]

        for column_index in range(len(row)):
            matrix[row_index][column_index] = row[column_index]

    result = []

    for column_index in range(max_length):
        new_row = []

        for row_index in range(row_count):
            new_row.append(matrix[row_index][column_index])

        while len(new_row) > 0 and new_row[-1] is None:
            new_row.pop()

        line = ""

        for value in new_row:
            if value is None:
                line += " "
            else:
                line += value

        result.append(line)

    return "\n".join(result)