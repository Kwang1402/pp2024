from __future__ import annotations
from datetime import date
from typing import List


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
