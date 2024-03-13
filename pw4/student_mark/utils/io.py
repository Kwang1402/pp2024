class InvalidChoice(Exception):
    pass


def prompt():
    print(
        """
    Choose an option below
=======================================
0. Exit.
1. Add a new course for a student.
2. List course(s) of a student.
3. Create a new student.
4. List student(s).
5. Update course mark for a student.
6. Calculate GPA of a student
=======================================
"""
    )
    VALID_CHOICES = ["0", "1", "2", "3", "4", "5", "6"]
    choice = input()
    if choice in VALID_CHOICES:
        return choice
    else:
        raise InvalidChoice(f'Invalid option "{choice}".')


def prompt_add_course():
    print("Student ID:")
    student_id = str(input())
    print("ID:")
    id = str(input())
    print("Name:")
    name = str(input())
    print("Credit:")
    credit = int(input())

    return {"student_id": student_id, "id": id, "name": name, "credit": credit}


def prompt_list_student_courses():
    print("Student ID:")
    id = str(input())
    return {"id": id}


def prompt_create_student():
    print("Student ID:")
    id = str(input())
    print("Student name:")
    name = str(input())
    print("Date of Birth: ")
    date_of_birth = str(input())
    return {"id": id, "name": name, "date_of_birth": date_of_birth}


def prompt_update_course_mark():
    print("Student ID: ")
    student_id = str(input())
    print("ID:")
    id = str(input())
    print("Mark:")
    mark = float(input())
    return {"student_id": student_id, "id": id, "mark": mark}


def prompt_calculate_gpa():
    print("ID:")
    id = str(input)

    return {"id": id}
