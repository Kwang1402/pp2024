import abc
from student_mark.domains import models


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, student: models.Student):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id) -> models.Student:
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
