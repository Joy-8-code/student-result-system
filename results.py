"""Score calculation and grading logic."""
MIN_SUBJECTS = 5


def total(student):
    return sum(student.scores.values())


def average(student):
    if not student.scores:
        return 0.0
    return total(student) / len(student.scores)


def grade_for(avg):
    """Convert an average score into a letter grade."""
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    return "F"


def grade(student):
    return grade_for(average(student))


def class_statistics(students):
    """Return highest/lowest individual score and class average, or None."""
    graded = [s for s in students if s.scores]
    if not graded:
        return None
    all_scores = [(sc, sub, s.name) for s in graded for sub, sc in s.scores.items()]
    highest = max(all_scores)
    lowest = min(all_scores)
    class_avg = sum(average(s) for s in graded) / len(graded)
    return {"highest": highest, "lowest": lowest,
            "class_average": class_avg, "count": len(graded)}
