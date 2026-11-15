import re
from datetime import datetime, date

# Student ID format: 2 digits / SCI + 2 digits / 1-4 digits
# e.g. 24/SCI01/121
ID_PATTERN = re.compile(r"^\d{2}/SCI\d{2}/\d{1,4}$")


def valid_id(student_id):
    """Return True if the ID looks like 24/SCI01/121 (regular expression check)."""
    return bool(ID_PATTERN.match(student_id))


def valid_date(text):
    """Return True if text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}  # {subject: score}
        self.date_entered = date_entered  # when scores were last recorded

    def set_scores(self, scores):
        """Store scores and record today's date."""
        self.scores = scores
        self.date_entered = date.today().isoformat()

    def to_dict(self):
        return {
            "student_id": self.student_id, "name": self.name,
            "class_name": self.class_name, "gender": self.gender,
            "dob": self.dob, "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["student_id"], d["name"], d["class_name"], d["gender"],
                   d["dob"], d.get("scores", {}), d.get("date_entered"))

    def __str__(self):
        return f"{self.student_id} | {self.name} | {self.class_name} | {self.gender} | {self.dob}"
