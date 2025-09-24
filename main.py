"""Accept csv-files with student scores and generate the average scores."""
import argparse
import csv
from tabulate import tabulate
from typing import Any, Dict, List

# Length of data in csv files.
CSV_DATA_LENGTH = 5


class GradesMixin:
    """Mixin for grades."""

    def __init__(self):
        """Initialize object."""
        self.grades: List[int] = []

    def add_grade(self, grade: int):
        """Add a grade."""
        if isinstance(grade, int) and 1 <= grade <= 5:
            self.grades.append(grade)
        else:
            raise ValueError("The grade must be in range from 1 to 5.")

    def average_grade(self) -> float:
        """Return average grade."""
        if not self.grades:
            return 0.0
        return round(sum(self.grades) / len(self.grades), 1)


class Subject(GradesMixin):
    """Subject class."""

    def __init__(self, name: str):
        """Initialize subject."""
        super().__init__()
        self.name = name


class Teacher(GradesMixin):
    """Teacher class."""

    def __init__(self, name: str):
        """Initialize teacher."""
        super().__init__()
        self.name = name


class Student(GradesMixin):
    """Student class."""

    def __init__(self, name: str):
        """Initialize student."""
        super().__init__()
        self.name = name


class Grade:
    """Grade class."""

    def __init__(
        self,
        student: Student,
        subject: Subject,
        teacher: Teacher,
        date: str,
        grade: int,
    ):
        """Initialize grade."""
        self.student = student
        self.subject = subject
        self.teacher = teacher
        self.date = date
        self.grade = grade


def parse_arguments():
    """Accept command arguments."""
    arg_parser = argparse.ArgumentParser(
        description='Accept file names for input and output.'
    )
    arg_parser.add_argument(
        '--files',
        nargs='+',
        required=True,
    )
    arg_parser.add_argument(
        '--report',
        required=True,
    )
    return arg_parser.parse_args()


def csv_files_to_objects(file_list):
    """Load data and create objects."""
    students: Dict[str, Student] = {}
    teachers: Dict[str, Teacher] = {}
    subjects: Dict[str, Subject] = {}
    grades: List[Grade] = []

    for file_name in file_list:
        try:
            with open(file_name, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    student_name, subject_name, teacher_name, date, grade = row

                    if student_name not in students:
                        students[student_name] = Student(student_name)
                    student = students[student_name]

                    if subject_name not in subjects:
                        subjects[subject_name] = Subject(subject_name)
                    subject = subjects[subject_name]

                    if teacher_name not in teachers:
                        teachers[teacher_name] = Teacher(teacher_name)
                    teacher = teachers[teacher_name]

                    grade_value = int(grade)
                    grades.append(
                        Grade(student, subject, teacher, date, grade_value)
                    )
                    student.add_grade(grade=grade_value)
                    subject.add_grade(grade=grade_value)
                    teacher.add_grade(grade=grade_value)

        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {str(e)}")

    return subjects, teachers, students, grades


def save_to_csv(
    data: List[Any],
    headers: List[str],
    filename: str,
):
    """Save result to csv-file."""
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def main():
    """Run the main part."""
    args = parse_arguments()
    subjects, teachers, students, grades = csv_files_to_objects(args.files)

    # === Здесь устанавливаем по какой модели группировка оценок.===========
    model = subjects  # subjects / teachers / students

    sorted_model = sorted(
        model.values(),
        key=lambda s: s.average_grade(),
        reverse=True
    )
    table_data = [
        (
            index, model.name, model.average_grade()
        ) for index, model in enumerate(sorted_model, start=1)
    ]
    headers = ["№", "name", "average_grade"]
    print(tabulate(
        tabular_data=table_data,
        headers=headers,
        tablefmt="grid",
        floatfmt=".1f",
    ))
    save_to_csv(data=table_data, headers=headers, filename=args.report)


if __name__ == '__main__':
    main()
