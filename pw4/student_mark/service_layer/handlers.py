from student_mark.domains import models, commands
from student_mark.adapters import repositories
import numpy as np
import math


class InvalidCourseId(Exception):
    pass


class InvalidStudentId(Exception):
    pass


def create_student(cmd: commands.CreateStudent, repo: repositories.LocalRepository):
    repo.add(models.Student(cmd.id, cmd.name, cmd.date_of_birth, courses=[]))


def add_course(cmd: commands.AddCourse, repo: repositories.LocalRepository):
    student = repo.get(id=cmd.student_id)
    if student is not None:
        student.courses.append(models.Course(cmd.id, cmd.name, cmd.credit))
    else:
        raise InvalidStudentId(f"Invalid student ID {cmd.student_id}")


def list_student_courses(
    cmd: commands.ListStudentCourses, repo: repositories.LocalRepository
):
    student = repo.get(id=cmd.id)
    if student is not None:
        return student.courses
    else:
        raise InvalidStudentId(f"Invalid student ID {cmd.id}")


def list_students(repo: repositories.LocalRepository):
    students = repo.list()
    sorted_students = np.array(
        sorted(
            np.array(list(students), dtype=object),
            key=lambda student: student.gpa(),
            reverse=True,
        ),
        dtype=object,
    )
    return sorted_students


def update_course_mark(
    cmd: commands.UpdateCourseMark, repo: repositories.LocalRepository
):
    student = repo.get(id=cmd.student_id)
    if student is not None:
        course = next((c for c in student.courses if c.id == cmd.id), None)
        if course is not None:
            course.mark = math.floor(cmd.mark)
        else:
            raise InvalidCourseId(f"Invalid course ID {cmd.id}")
    else:
        raise InvalidStudentId(f"Invalid student ID {cmd.course_id}")


def calculate_gpa(cmd: commands.CalculateGPA, repo: repositories.LocalRepository):
    student = repo.get(id=cmd.id)
    if student is not None:
        return student.gpa()
    else:
        raise InvalidStudentId(f"Invalid student ID {cmd.id}")


COMMANDS_HANDLERS = {
    commands.CreateStudent: create_student,
    commands.AddCourse: add_course,
    commands.ListStudentCourses: list_student_courses,
    commands.UpdateCourseMark: update_course_mark,
    commands.CalculateGPA: calculate_gpa,
}
