import dataclasses
from datetime import date


class Command:
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
