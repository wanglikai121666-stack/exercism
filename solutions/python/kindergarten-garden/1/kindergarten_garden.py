class Garden:
    DEFAULT_STUDENTS = [
        "Alice",
        "Bob",
        "Charlie",
        "David",
        "Eve",
        "Fred",
        "Ginny",
        "Harriet",
        "Ileana",
        "Joseph",
        "Kincaid",
        "Larry",
    ]

    PLANTS = {
        "G": "Grass",
        "C": "Clover",
        "R": "Radishes",
        "V": "Violets",
    }
    def __init__(self, diagram, students=None):
        self.rows = diagram.splitlines()
        if students is None:
            self.students = self.DEFAULT_STUDENTS
        else:
            self.students = sorted(students)
    def plants(self, student):
        student_index = self.students.index(student)
        start = student_index * 2
        end = start + 2
        plant_codes = self.rows[0][start:end] + self.rows[1][start:end]

        result = []
        for code in plant_codes:
            result.append(self.PLANTS[code])

        return result


