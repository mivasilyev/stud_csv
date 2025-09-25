import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Grade, GradesMixin, Student, Subject, Teacher


def test_grades_mixin():
    mixin = GradesMixin()
    mixin.add_grade(4)
    mixin.add_grade(5)
    assert mixin.grades == [4, 5]
    assert mixin.average_grade() == 4.5
    with pytest.raises(ValueError):
        mixin.add_grade(6)
    with pytest.raises(ValueError):
        mixin.add_grade(0)


def test_object_creation():
    student = Student("Иван Петров")
    teacher = Teacher("Анна Иванова")
    subject = Subject("Математика")
    assert student.name == "Иван Петров"
    assert teacher.name == "Анна Иванова"
    assert subject.name == "Математика"


def test_grade_creation():
    student = Student("Иван Петров")
    teacher = Teacher("Анна Иванова")
    subject = Subject("Математика")
    grade = Grade(student, subject, teacher, "2025-09-25", 5)
    assert grade.student == student
    assert grade.subject == subject
    assert grade.teacher == teacher
    assert grade.date == "2025-09-25"
    assert grade.grade == 5
