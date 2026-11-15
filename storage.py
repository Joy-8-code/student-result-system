"""Load and save data as JSON."""
import json
import os
from student import Student

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.json")


def load_students():
    """Return {student_id: Student}. Handles missing or corrupted file."""
    students = {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for d in raw:
            s = Student.from_dict(d)
            students[s.student_id] = s
    except FileNotFoundError:
        print("No data file found. Starting with an empty system.")
    except (json.JSONDecodeError, KeyError):
        print("Warning: data file is damaged. Starting empty.")
    return students


def save_students(students):
    """Write all students to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as e:
        print(f"Could not save data: {e}")
