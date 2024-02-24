from __future__ import annotations
import sys
from datetime import date
from typing import List
import abc
from dataclasses import dataclass
import math
import numpy

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
        
        return round(weighted_sum/total_credit, 1)

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

@dataclass
class CreateStudent(Command):
    id: str
    name: str
    date_of_birth: date

@dataclass
class AddCourse(Command):
    id: str
    student_id: str
    name: str
    credit: int

@dataclass
class ListStudentCourses(Command):
    id: str


@dataclass
class UpdateCourseMark(Command):
    id: str
    student_id: str
    mark: float

@dataclass
class CalculateGPA(Command):
    id: str

def create_student(cmd: CreateStudent, repo: LocalRepository):
    repo.add(Student(cmd.id, cmd.name, cmd.date_of_birth, courses=[]))


def add_course(cmd: AddCourse, repo: LocalRepository):
    student = repo.get(id=cmd.student_id)
    try:
        if student is not None:
            student.courses.append(Course(cmd.id, cmd.name, cmd.credit))
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.student_id}")
    except InvalidStudentId as e:
        print(e)

def list_student_courses(cmd: ListStudentCourses, repo: LocalRepository):
    student = repo.get(id=cmd.id)
    try:
        if student is not None:
            for index, course in enumerate(student.courses, start=1):
                print(
                    f"{index}. {course.id} {course.name} {course.credit} {course.mark}"
                )
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.id}")
    except InvalidStudentId as e:
        print(e)


def list_students(repo: LocalRepository):
    students = repo.list()
    for index, student in enumerate(students, start=1):
        print(f"{index}. {student.id} {student.name} {student.date_of_birth}")


def update_course_mark(cmd: UpdateCourseMark, repo: LocalRepository):
    student = repo.get(id=cmd.student_id)
    try:
        if student is not None:
            course = next((c for c in student.courses if c.id == cmd.id), None)
            if course is not None:
                course.mark = math.floor(cmd.mark)
            else:
                raise InvalidCourseId(f"Invalid course ID {cmd.id}")
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.course_id}")
    except (InvalidCourseId, InvalidStudentId) as e:
        print(e)

def calculate_gpa(cmd: CalculateGPA, repo: LocalRepository):
    student = repo.get(id=cmd.id)
    try:
        if student is not None:
            print(student.gpa())
        else:
            raise InvalidStudentId(f"Invalid student ID {cmd.id}")
    except InvalidStudentId as e:
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
1. Add a new course for a student.
2. List course(s) of a student.
3. Create a new student.
4. List student(s).
5. Update course mark for a student.
6. Calculate GPA of a student
=======================================
        """
    )


def prompt_add_course(repo: LocalRepository):
    print("Student ID:")
    student_id = str(input())
    print("ID:")
    id = str(input())
    print("Name:")
    name = str(input())
    print("Credit:")
    credit = int(input())

    add_course(AddCourse(id, student_id, name, credit), repo)

def prompt_list_student_courses(repo: LocalRepository):
    print("Student ID:")
    id = str(input())

    list_student_courses(ListStudentCourses(id), repo)

def prompt_create_student(repo: LocalRepository):
    print("Student ID:")
    id = str(input())
    print("Student name:")
    name = str(input())
    print("Date of Birth: ")
    date_of_birth = str(input())
    create_student(CreateStudent(id, name, date_of_birth), repo)

def prompt_list_students(repo: LocalRepository):
    list_students(repo)

def prompt_update_course_mark(repo: LocalRepository):
    print("Student ID: ")
    student_id = str(input())
    print("ID:")
    id = str(input())
    print("Mark:")
    mark = float(input())

    update_course_mark(UpdateCourseMark(id, student_id, mark), repo)

def prompt_calculate_gpa(repo: LocalRepository):
    print("ID: ")
    id = str(input())

    calculate_gpa(CalculateGPA(id), repo)

def main():
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
