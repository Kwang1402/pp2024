from student_mark.utils import io
from student_mark.utils.io import InvalidChoice
from student_mark.domains import commands
from student_mark.service_layer.handlers import list_students
from student_mark.service_layer.handlers import COMMANDS_HANDLERS
from student_mark.service_layer.handlers import InvalidCourseId, InvalidStudentId
from student_mark.adapters import repositories
import sys
import os

def end_program():
    files_to_compress = ['pw5/student_mark/data/students.txt', 'pw5/student_mark/data/courses.txt', 'pw5/student_mark/data/marks.txt']
    io.compress_files(files_to_compress, 'pw5/student_mark/data/student.dat')
    print("Ending program...")
    sys.exit()

def handle(
    command: commands.Command,
    repo: repositories.AbstractRepository,
    command_handlers=COMMANDS_HANDLERS,
):
    handler = command_handlers[type(command)]
    result = handler(command, repo)
    return result

def load_data(repo: repositories.AbstractRepository):
    if os.path.exists('pw5/student_mark/data/students.txt'):
        with open('pw5/student_mark/data/students.txt', 'r') as file:
            for line in file:
                data = line.strip().split(' ')
                body = {
                    'id': data[0],
                    'name': data[1],
                    'date_of_birth': data[2],
                }
                cmd = commands.CreateStudent(**body)
                handle(cmd, repo)

    if os.path.exists('pw5/student_mark/data/courses.txt'):
        with open('pw5/student_mark/data/courses.txt', 'r') as file:
            for line in file:
                data = line.strip().split(' ')
                body = {
                    'student_id': data[0],
                    'id': data[1],
                    'name': data[2],
                    'credit': int(data[3]),
                }
                cmd = commands.AddCourse(**body)
                handle(cmd, repo)
    
    if os.path.exists('pw5/student_mark/data/marks.txt'):
        with open('pw5/student_mark/data/marks.txt', 'r') as file:
            for line in file:
                data = line.strip().split(' ')
                body = {
                    'student_id': data[0],
                    'id': data[1],
                    'mark': float(data[2]),
                }
                cmd = commands.UpdateCourseMark(**body)
                handle(cmd, repo)

def main():
    repo = repositories.LocalRepository([])
    io.decompress_files('pw5/student_mark/data/student.dat', 'pw5/student_mark/data')
    load_data(repo)

    while True:
        try:
            choice = io.prompt()
        except InvalidChoice as e:
            print(e)
            continue

        if choice == "0":
            end_program()

        if choice == "1":
            try:
                body = io.prompt_add_course()
                cmd = commands.AddCourse(**body)
                handle(cmd, repo)
                io.write_to_file(body, f'pw5/student_mark/data/courses.txt')
            except InvalidStudentId as e:
                print(str(e))

        if choice == "2":
            try:
                body = io.prompt_list_student_courses()
                cmd = commands.ListStudentCourses(**body)
                handle(cmd, repo)
            except InvalidCourseId as e:
                print(str(e))

        if choice == "3":
            body = io.prompt_create_student()
            cmd = commands.CreateStudent(**body)
            handle(cmd, repo)
            io.write_to_file(body, f'pw5/student_mark/data/students.txt')

        if choice == "4":
            result = list_students(repo)
            for index, student in enumerate(result, start=1):
                print(
                    f"{index}. {student.id} {student.name} {student.date_of_birth} {student.gpa()}"
                )

        if choice == "5":
            try:
                body = io.prompt_update_course_mark()
                cmd = commands.UpdateCourseMark(**body)
                handle(cmd, repo)
                io.write_to_file(body, f'pw5/student_mark/data/marks.txt')
            except (InvalidStudentId, InvalidCourseId) as e:
                print(str(e))

        if choice == "6":
            try:
                body = io.prompt_calculate_gpa()
                cmd = commands.CalculateGPA(**body)
                result = handle(cmd, repo)
            except InvalidStudentId as e:
                print(str(e))
            print(result)


if __name__ == "__main__":
    main()
