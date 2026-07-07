def saddle_points(matrix):
    validate_matrix(matrix)
    result = []
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        row_max = max(row)
        for column_index in range(len(row)):
            value = row[column_index]
            if value == row_max and is_column_min(matrix, column_index, value):
                result.append({
                    "row": row_index + 1,
                    "column": column_index + 1
                })
    return result

def validate_matrix(matrix):
    if not matrix:
        return

    expected_length = len(matrix[0])

    for row in matrix:
        if len(row) != expected_length:
            raise ValueError("irregular matrix")

def is_column_min(matrix, column_index, value):
    for row in matrix:
        if row[column_index] < value:
            return False

    return True