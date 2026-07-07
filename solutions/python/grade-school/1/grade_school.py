class School:
    def __init__(self):
        self.students_by_grade = {}
        self.all_students = set()
        self.added_status = []

    def add_student(self, name, grade):
        if name in self.all_students:
            self.added_status.append(False)
            return
        if grade not in self.students_by_grade:
            self.students_by_grade[grade] = []
        self.students_by_grade[grade].append(name)
        self.all_students.add(name)
        self.added_status.append(True)

    def roster(self):
        result = []
        for grade in sorted(self.students_by_grade):
            students = self.students_by_grade[grade]
            result.extend(sorted(students))
        return result

    def grade(self, grade_number):
        if grade_number not in self.students_by_grade:
            return []

        return sorted(self.students_by_grade[grade_number])
    def added(self):
        return self.added_status
