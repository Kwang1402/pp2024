import sys

students = []
courses = []
nums_of_students = 0
nums_of_courses = 0

def list_student_marks_for_a_course():
    try:
        print("Which course?")
        course_name = input()
        if course_name not in [c["name"] for c in courses]:
            raise ValueError(f"Invalid course {course_name}")
        for i in range(0, len(students)):
            print(f'{i+1}. ID: {students[i]["id"]} Name: {students[i]["name"]} {course_name}: {students[i][course_name]}')
    except ValueError as e:
        print(e)

def input_student_marks_for_a_course():
    if(len(students) == 0):
        print("There aren't any student yet!")
        return
    try:
        print("Which course?")
        course_name = input()
        if course_name not in [c["name"] for c in courses]:
            raise ValueError(f"Invalid course {course_name}")
        for i in range(0, len(students)):
            print(f'{i+1}. ID: {students[i]["id"]} Name: {students[i]["name"]}')
            students[i][course_name] = float(input())
    except ValueError as e:
        print(e)

def list_students():
    if len(students) == 0:
        print("There aren't any student yet!")
        return

    print("List of student(s):")
    for i in range(0, len(students)):
        print(
            f'{i+1}. ID: {students[i]["id"]} Name: {students[i]["name"]} DoB: {students[i]["date_of_birth"]}'
        )

def list_course():
    if len(courses) == 0:
        print("There aren't any course yet!")
        return

    print("List of course(s):")
    for i in range(0, len(courses)):
        print(
            f'{i+1}. ID: {courses[i]["id"]} Name: {courses[i]["name"]}'
        )    

def add_new_student():
    print("ID:")
    id = str(input())
    print("Name:")
    name = str(input())
    print("DoB:")
    date_of_birth = str(input())
    student = {"id": id, "name": name, "date_of_birth": date_of_birth}
    students.append(student)

def add_new_course():
    print("ID:")
    id = str(input())
    print("Name:")
    name = str(input())
    course = {"id": id, "name": name}
    courses.append(course)

def get_number_of_students():
    global nums_of_students
    print("Input the number of student(s):")
    try:
        nums_of_students = int(input())
        if nums_of_students <= 0:
            print("Invalid input. The number of student(s) must be greater than 0.")
    except ValueError:
        print("The number of student(s) must be a valid integer.")


def get_number_of_courses():
    global nums_of_courses
    print("Input the number of course(s):")
    try:
        nums_of_courses = int(input())
        if nums_of_courses <= 0:
            print("Invalid input. The number of course(s) must be greater than 0.")
    except ValueError:
        print("The number of course(s) must be a valid integer.")


def end_program():
    print("Ending program...")
    sys.exit()


def prompt():
    print(
        """
        Choose an option below
=======================================
0. Exit.
1. Input the number of student(s).
2. Add a new student.
3. List student(s).
4. Input the number of course(s).
5. Add a new course.
6. List course(s).
7. Input student mark(s) for a course.
8. List student mark(s) for a course.
=======================================
        """
    )


def main():
    options = {
        "0": end_program,
        "1": get_number_of_students,
        "2": add_new_student,
        "3": list_students,
        "4": get_number_of_courses,
        "5": add_new_course,
        "6": list_course,
        "7": input_student_marks_for_a_course,
        "8": list_student_marks_for_a_course
    }
    while True:
        prompt()
        try:
            option = input()
            if option in options:
                options[option]()
            else:
                raise ValueError(f'Invalid option "{option}".')
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
