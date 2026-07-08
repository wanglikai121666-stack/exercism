class Matrix:
    def __init__(self, matrix_string):
        self.matrix = []

        rows = matrix_string.splitlines()

        for row in rows:
            numbers = row.split()
            number_row = []

            for number in numbers:
                number_row.append(int(number))

            self.matrix.append(number_row)


    def row(self, index):
        return self.matrix[index - 1]

    def column(self, index):
        result = []

        for row in self.matrix:
            result.append(row[index - 1])

        return result
