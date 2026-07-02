def tick(matrix):
    if matrix == []:
        return []

    row_count = len(matrix)
    column_count = len(matrix[0])

    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    new_matrix = []

    for row_index in range(row_count):
        new_row = []

        for column_index in range(column_count):
            live_neighbors = 0

            for row_step, column_step in directions:
                neighbor_row = row_index + row_step
                neighbor_column = column_index + column_step

                if 0 <= neighbor_row < row_count and 0 <= neighbor_column < column_count:
                    if matrix[neighbor_row][neighbor_column] == 1:
                        live_neighbors += 1

            current_cell = matrix[row_index][column_index]

            if current_cell == 1:
                if live_neighbors == 2 or live_neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)
            else:
                if live_neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)

        new_matrix.append(new_row)

    return new_matrix