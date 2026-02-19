
class student_record:
    def __init__(self, name):
        self.Name = name
        self.grades = []

    def addGrade(self, grade):
        self.grades.append(grade)

    def get_average(self):
        total = 0
        for g in self.grades:
            total += g
        return total / len(self.grades)

def get_top_student(students):
    top_student = None
    highest_avg = float('-inf')
    for student in students:
        if student.get_average() > highest_avg:
            highest_avg = student.get_average()
            top_student = student
    return top_student

def main():
    s1 = student_record("Alice")
    s1.addGrade(90)
    s1.addGrade(85)

    s2 = student_record("Bob")
    s2.addGrade(75)
    s2.addGrade(80)

    student_list = [s1, s2]
    best = get_top_student(student_list)

    print("Top student is: " + best.Name)

if __name__ == "__main__":
    main()
