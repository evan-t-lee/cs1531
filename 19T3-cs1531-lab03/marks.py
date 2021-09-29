students = [
    {
        "name": "Matt",
        "homework": [90.0, 97.0, 75.0, 92.0],
        "quizzes": [88.0, 40.0, 94.0],
        "tests": [75.0, 90.0],
    },
    {
        "name": "Mich",
        "homework": [100.0, 92.0, 98.0, 100.0],
        "quizzes": [82.0, 83.0, 91.0],
        "tests": [89.0, 97.0],
    },
    {
        "name": "Mark",
        "homework": [0.0, 87.0, 75.0, 22.0],
        "quizzes": [0.0, 75.0, 78.0],
        "tests": [100.0, 100.0],
    }
]

if __name__ == '__main__':
    def average(marks):
        return sum(marks)/len(marks)

    def total_average(field):
        student_marks = [average(student[field]) for student in students]
        return average(student_marks)

    print(f"Average homework mark: {total_average('homework')}")
    print(f"Average quiz mark: {total_average('quizzes')}")
    print(f"Average test mark: {total_average('tests')}")