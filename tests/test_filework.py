import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import csv_files_to_objects, save_to_csv


def test_csv_parsing(tmp_path):
    test_file = tmp_path / "test.csv"
    test_data = (
        'Имя,Предмет,Учитель,Дата,Оценка\n'
        'Иван Петров,Математика,Анна Иванова,2025-09-25,5\n'
        'Петр Сидоров,Физика,Иван Петров,2025-09-26,4'
    )
    test_file.write_text(test_data)
    subjects, teachers, students, grades = csv_files_to_objects([test_file])
    for s in students:
        print(s)
    assert len(students) == 2
    assert len(teachers) == 2
    assert len(subjects) == 2
    assert len(grades) == 2


def test_save_to_csv(tmp_path):
    test_file = tmp_path / "output.csv"
    data = [
        ["Иван Петров", 4.5],
        ["Петр Сидоров", 5.0]
    ]
    headers = ["Имя", "Средний балл"]
    save_to_csv(data, headers, test_file)
    with open(test_file, 'r') as f:
        lines = f.readlines()
        assert lines[0].strip() == "Имя,Средний балл"
        assert lines[1].strip() == "Иван Петров,4.5"
        assert lines[2].strip() == "Петр Сидоров,5.0"
