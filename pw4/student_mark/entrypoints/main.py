from student_mark.utils import io
from student_mark.utils.io import InvalidChoice
from student_mark.domains import commands
from student_mark.service_layer.handlers import list_students
from student_mark.service_layer.handlers import COMMANDS_HANDLERS
from student_mark.service_layer.handlers import InvalidCourseId, InvalidStudentId
from student_mark.adapters import repositories
import sys


def end_program():
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


def main():
    repo = repositories.LocalRepository([])
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

        if choice == "4":
            result = list_students(repo)
            for index, student in enumerate(result, start=1):
                print(
                    f"{index}. {student.id} {student.name} {student.date_of_birth} {student.gpa()}\n"
                )

        if choice == "5":
            try:
                body = io.prompt_update_course_mark()
                cmd = commands.UpdateCourseMark(**body)
                handle(cmd, repo)
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
