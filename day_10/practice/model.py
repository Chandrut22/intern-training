from Student import Student

class StudentService:

    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name, age):
        student = Student(student_id, name, age)
        self.students[student_id] = student
        return student.get_details()

    def get_students(self):
        return [student.get_details() for student in self.students.values()]

    def get_student(self, student_id):
        student = self.students.get(student_id)

        if not student:
            return None

        return student.get_details()

    def update_student(self, student_id, name, age):
        student = self.students.get(student_id)

        if not student:
            return None

        student.set_name(name)
        student.set_age(age)

        return student.get_details()

    def delete_student(self, student_id):
        return self.students.pop(student_id, None)