from __future__ import annotations
import sys
from datetime import date
from typing import List
import abc
import dataclasses
import math
import numpy as np
import curses


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, student: Student):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id) -> Student:
        raise NotImplementedError


class LocalRepository(AbstractRepository):
    def __init__(self, students):
        self._students = set(students)

    def add(self, student):
        self._students.add(student)

    def get(self, id):
        return next((s for s in self._students if s.id == id), None)

    def list(self):
        return self._students


class Student:
    def __init__(self, id: str, name: str, date_of_birth: date, courses: List[Course]):
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.courses = courses

    def gpa(self) -> float:
        total_credit = 0
        weighted_sum = 0
        for course in self.courses:
            total_credit = total_credit + course.credit
            weighted_sum = weighted_sum + course.credit * course.mark

        if total_credit == 0:
            return 0.0

        return round(weighted_sum / total_credit, 1)


class Course:
    def __init__(self, id: str, name: str, credit: int, mark: float = 0):
        self.id = id
        self.name = name
        self.credit = credit
        self.mark = mark


class Command:
    pass


class InvalidCourseId(Exception):
    pass


class InvalidStudentId(Exception):
    pass


@dataclasses.dataclass
class CreateStudent(Command):
    id: str
    name: str
    date_of_birth: date


@dataclasses.dataclass
class AddCourse(Command):
    id: str
    student_id: str
    name: str
    credit: int


@dataclasses.dataclass
class ListStudentCourses(Command):
    id: str


@dataclasses.dataclass
class UpdateCourseMark(Command):
    id: str
    student_id: str
    mark: float


@dataclasses.dataclass
class CalculateGPA(Command):
    id: str


def create_student(cmd: CreateStudent, repo: LocalRepository):
    repo.add(Student(cmd.id, cmd.name, cmd.date_of_birth, courses=[]))


def add_course(stdscr, cmd: AddCourse, repo: LocalRepository):
    student = repo.get(id=cmd.student_id)
    try:
        if student is not None:
            student.courses.append(Course(cmd.id, cmd.name, cmd.credit))
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.student_id}\n")
    except InvalidStudentId as e:
        stdscr.addstr(str(e))
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()


def list_student_courses(stdscr, cmd: ListStudentCourses, repo: LocalRepository):
    student = repo.get(id=cmd.id)
    try:
        if student is not None:
            for index, course in enumerate(student.courses, start=1):
                stdscr.addstr(
                    f"{index}. {course.id} {course.name} {course.credit} {course.mark}\n"
                )
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.id}\n")
    except InvalidStudentId as e:
        stdscr.addstr(str(e))
    stdscr.addstr("Press any key to continue...")
    stdscr.getch()


def list_students(stdscr, repo: LocalRepository):
    students = repo.list()
    sorted_students = np.array(
        sorted(
            np.array(list(students), dtype=object),
            key=lambda student: student.gpa(),
            reverse=True,
        ),
        dtype=object,
    )
    for index, student in enumerate(sorted_students, start=1):
        stdscr.addstr(
            f"{index}. {student.id} {student.name} {student.date_of_birth} {student.gpa()}\n"
        )
    stdscr.addstr("Press any key to continue...")
    stdscr.getch()


def update_course_mark(stdscr, cmd: UpdateCourseMark, repo: LocalRepository):
    student = repo.get(id=cmd.student_id)
    try:
        if student is not None:
            course = next((c for c in student.courses if c.id == cmd.id), None)
            if course is not None:
                course.mark = math.floor(cmd.mark)
            else:
                raise InvalidCourseId(f"Invalid course ID {cmd.id}\n")
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.course_id}\n")
    except (InvalidCourseId, InvalidStudentId) as e:
        stdscr.addstr(str(e))
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()


def calculate_gpa(stdscr, cmd: CalculateGPA, repo: LocalRepository):
    student = repo.get(id=cmd.id)
    try:
        if student is not None:
            stdscr.addstr(str(student.gpa()) + "\n")
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.id}\n")
    except InvalidStudentId as e:
        stdscr.addstr(str(e))
    stdscr.addstr("Press any key to continue...")
    stdscr.getch()


def end_program(stdscr):
    stdscr.addstr("Ending program...")
    stdscr.refresh()
    sys.exit()


def prompt(stdscr):
    stdscr.addstr(
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


def prompt_add_course(stdscr, repo):
    stdscr.addstr("Student ID:")
    stdscr.refresh()
    student_id = stdscr.getstr().decode("utf-8")

    stdscr.addstr("ID:")
    stdscr.refresh()
    id = stdscr.getstr().decode("utf-8")

    stdscr.addstr("Name:")
    stdscr.refresh()
    name = stdscr.getstr().decode("utf-8")

    stdscr.addstr("Credit:")
    stdscr.refresh()
    credit = int(stdscr.getstr().decode("utf-8"))

    add_course(stdscr, AddCourse(id, student_id, name, credit), repo)


def prompt_list_student_courses(stdscr, repo):
    stdscr.addstr("Student ID:")
    stdscr.refresh()
    id = stdscr.getstr().decode("utf-8")

    list_student_courses(stdscr, ListStudentCourses(id), repo)


def prompt_create_student(stdscr, repo):
    stdscr.addstr("Student ID:")
    stdscr.refresh()
    id = stdscr.getstr().decode("utf-8")

    stdscr.addstr("Student name:")
    stdscr.refresh()
    name = stdscr.getstr().decode("utf-8")

    stdscr.addstr("Date of Birth:")
    stdscr.refresh()
    date_of_birth = stdscr.getstr().decode("utf-8")

    create_student(CreateStudent(id, name, date_of_birth), repo)


def prompt_list_students(stdscr, repo):
    list_students(stdscr, repo)


def prompt_update_course_mark(stdscr, repo):
    stdscr.addstr("Student ID:")
    stdscr.refresh()
    student_id = stdscr.getstr().decode("utf-8")

    stdscr.addstr("ID:")
    stdscr.refresh()
    id = stdscr.getstr().decode("utf-8")

    stdscr.addstr("Mark:")
    stdscr.refresh()
    mark = float(stdscr.getstr().decode("utf-8"))

    update_course_mark(stdscr, UpdateCourseMark(id, student_id, mark), repo)


def prompt_calculate_gpa(stdscr, repo):
    stdscr.addstr("ID:")
    stdscr.refresh()
    id = stdscr.getstr().decode("utf-8")

    calculate_gpa(stdscr, CalculateGPA(id), repo)


def main(stdscr):
    repo = LocalRepository([])
    HANDLERS = {
        "0": end_program,
        "1": prompt_add_course,
        "2": prompt_list_student_courses,
        "3": prompt_create_student,
        "4": prompt_list_students,
        "5": prompt_update_course_mark,
        "6": prompt_calculate_gpa,
    }
    while True:
        stdscr.clear()
        prompt(stdscr)
        stdscr.refresh()
        curses.echo()

        handler = stdscr.getstr().decode("utf-8")
        if handler == "0":
            HANDLERS[handler](stdscr)
        if handler in HANDLERS:
            # stdscr.clear()
            HANDLERS[handler](stdscr, repo)
            stdscr.refresh()
        else:
            stdscr.addstr(f'Invalid option "{handler}". Press any key to continue...')
            stdscr.getch()
            # stdscr.clear()

        curses.noecho()


if __name__ == "__main__":
    curses.wrapper(main)
