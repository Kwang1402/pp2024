from __future__ import annotations
import sys
from datetime import datetime
from typing import Optional, List
import abc
from dataclasses import dataclass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, course: Course):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id) -> Course:
        raise NotImplementedError


class LocalRepository(AbstractRepository):
    def __init__(self, courses):
        self._courses = set(courses)

    def add(self, course):
        self._courses.add(course)

    def get(self, id):
        return next((c for c in self._courses if c.id == id), None)

    def list(self):
        return self._courses


class Course:
    def __init__(self, id: str, name: str, students: List[Student]):
        self.id = id
        self.name = name
        self.students = students


class Student:
    def __init__(self, id: str, name: str, date_of_birth: datetime, mark: float = None):
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.mark = mark


class Command:
    pass


class InvalidCourseId(Exception):
    pass


class InvalidStudentId(Exception):
    pass


@dataclass
class CreateCourse(Command):
    id: str
    name: str


@dataclass
class AddStudent(Command):
    id: str
    name: str
    date_of_birth: datetime
    course_id: str
    mark: Optional[float] = None


@dataclass
class ListCourseStudents(Command):
    id: str


@dataclass
class UpdateStudentMark(Command):
    id: str
    course_id: str
    mark: float


def create_course(cmd: CreateCourse, repo: LocalRepository):
    repo.add(Course(cmd.id, cmd.name, students=[]))


def add_student(cmd: AddStudent, repo: LocalRepository):
    course = repo.get(id=cmd.course_id)
    try:
        if course is not None:
            course.students.append(Student(cmd.id, cmd.name, cmd.date_of_birth, cmd.mark))
        else:
            raise InvalidCourseId(f"Invalid course ID {cmd.course_id}")
    except InvalidCourseId as e:
        print(e)

def list_course_student(cmd: ListCourseStudents, repo: LocalRepository):
    course = repo.get(id=cmd.id)
    try:
        if course is not None:
            for index, student in enumerate(course.students, start=1):
                print(
                    f"{index}. {student.id} {student.name} {student.date_of_birth} {student.mark}"
                )
        else:
            raise InvalidCourseId(f"Invalid course ID {cmd.id}")
    except InvalidCourseId as e:
        print(e)


def list_course(repo: LocalRepository):
    courses = repo.list()
    for index, course in enumerate(courses, start=1):
        print(f"{index}. {course.id} {course.name}")


def update_student_mark(cmd: UpdateStudentMark, repo: LocalRepository):
    course = repo.get(id=cmd.course_id)
    try:
        if course is not None:
            student = next((s for s in course.students if s.id == cmd.id), None)
            if student is not None:
                student.mark = cmd.mark
            else:
                raise InvalidStudentId(f"Invalid student ID {cmd.id}")
        else:
            raise InvalidCourseId(f"Invalid course ID {cmd.course_id}")
    except (InvalidCourseId, InvalidStudentId) as e:
        print(e)


def end_program():
    print("Ending program...")
    sys.exit()


def prompt():
    print(
        """
        Choose an option below
=======================================
0. Exit.
1. Add a new student to a course.
2. List student(s) in a course.
3. Add a new course.
4. List course(s).
5. Input student mark(s) for a course.
=======================================
        """
    )


def prompt_add_student(repo: LocalRepository):
    print("Course ID:")
    course_id = str(input())
    print("ID:")
    id = str(input())
    print("Name:")
    name = str(input())
    print("DoB:")
    date_of_birth = str(input())

    add_student(AddStudent(id, name, date_of_birth, course_id), repo)

def prompt_list_course_student(repo: LocalRepository):
    print("Course ID:")
    id = str(input())

    list_course_student(ListCourseStudents(id), repo)

def prompt_create_course(repo: LocalRepository):
    print("Course ID:")
    id = str(input())
    print("Course name:")
    name = str(input())

    create_course(CreateCourse(id, name), repo)

def prompt_list_course(repo: LocalRepository):
    list_course(repo)

def prompt_update_student_mark(repo: LocalRepository):
    print("Course ID: ")
    course_id = str(input())
    print("ID:")
    id = str(input())
    print("Mark:")
    mark = float(input())

    update_student_mark(UpdateStudentMark(id, course_id, mark), repo)

def main():
    repo = LocalRepository([])
    HANDLERS = {
        "0": end_program,
        "1": prompt_add_student,
        "2": prompt_list_course_student,
        "3": prompt_create_course,
        "4": prompt_list_course,
        "5": prompt_update_student_mark,
    }
    while True:
        prompt()
        try:
            handler = input()
            if handler == "0":
                HANDLERS[handler]()
            if handler in HANDLERS:
                HANDLERS[handler](repo)
            else:
                raise ValueError(f'Invalid option "{handler}".')
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
