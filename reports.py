"""Report generation."""
import os
from datetime import datetime
import results


def report_card(s):
    lines = ["=" * 40, f"REPORT CARD - {s.name}", "=" * 40,
             f"ID: {s.student_id}   Class: {s.class_name}",
             f"Gender: {s.gender}   DOB: {s.dob}", "-" * 40]
    if not s.scores:
        lines.append("No scores recorded yet.")
    else:
        for sub, sc in s.scores.items():
            lines.append(f"{sub:<20}{sc:>6.1f}")
        lines += ["-" * 40,
                  f"{'Total':<20}{results.total(s):>6.1f}",
                  f"{'Average':<20}{results.average(s):>6.2f}",
                  f"{'Grade':<20}{results.grade(s):>6}",
                  f"Result entered: {s.date_entered}"]
    lines.append("=" * 40)
    return "\n".join(lines)


def sort_students(students, by="average"):
    """Sort by average (highest first) or by name."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=results.average, reverse=True)


def summary_table(students):
    lines = [f"{'ID':<9}{'Name':<22}{'Total':>8}{'Avg':>8}{'Grade':>7}", "-" * 54]
    for s in students:
        lines.append(f"{s.student_id:<9}{s.name[:20]:<22}{results.total(s):>8.1f}"
                     f"{results.average(s):>8.2f}{results.grade(s):>7}")
    return "\n".join(lines)


def stats_text(students):
    st = results.class_statistics(students)
    if st is None:
        return "No scores available for statistics."
    h, l = st["highest"], st["lowest"]
    return (f"Students with scores: {st['count']}\n"
            f"Highest score: {h[0]} ({h[1]}, {h[2]})\n"
            f"Lowest score:  {l[0]} ({l[1]}, {l[2]})\n"
            f"Class average: {st['class_average']:.2f}")


def save_report(students, filename="class_report.txt"):
    """Write a full class report to a text file and return its path."""
    ranked = sort_students(students)
    text = (f"CLASS RESULT REPORT - generated {datetime.now():%Y-%m-%d %H:%M}\n\n"
            f"{summary_table(ranked)}\n\n{stats_text(students)}\n")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
