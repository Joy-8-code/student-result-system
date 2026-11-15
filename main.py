"""Student Result Management System - entry point and menu."""
import storage
import results
import reports
from student import Student, valid_id, valid_date


def ask(prompt):
    return input(prompt).strip()


def ask_score(subject):
    """Keep asking until a valid score between 0 and 100 is entered."""
    while True:
        try:
            score = float(ask(f"  {subject} score (0-100): "))
        except ValueError:
            print("  Please enter a number.")
        else:
            if 0 <= score <= 100:
                return score
            print("  Score must be between 0 and 100.")


def find(students, key):
    """Find by exact ID or partial name; returns a list."""
    key = key.lower()
    return [s for s in students.values()
            if s.student_id.lower() == key or key in s.name.lower()]


def pick_student(students):
    matches = find(students, ask("Enter student ID or name: "))
    if not matches:
        print("No student found.")
        return None
    if len(matches) > 1:
        print("Multiple matches:")
        for s in matches:
            print(" ", s)
        sid = ask("Enter the exact ID: ").upper()
        return students.get(sid)
    return matches[0]


def add_student(students):
    sid = ask("Student ID (e.g. 24/SCI01/001): ").upper()
    if not valid_id(sid):
        print("Invalid ID format.")
        return
    if sid in students:
        print("That ID already exists.")
        return
    name = ask("Full name: ").title()
    if not name:
        print("Name cannot be empty.")
        return
    class_name = ask("Class/Form: ")
    gender = ask("Gender (M/F): ").upper()
    if gender not in ("M", "F"):
        print("Gender must be M or F.")
        return
    dob = ask("Date of birth (YYYY-MM-DD): ")
    if not valid_date(dob):
        print("Invalid date.")
        return
    students[sid] = Student(sid, name, class_name, gender, dob)
    storage.save_students(students)
    print("Student added.")


def view_students(students):
    if not students:
        print("No students registered.")
    for s in students.values():
        print(s)


def search_student(students):
    matches = find(students, ask("Search ID or name: "))
    print("\n".join(str(s) for s in matches) if matches else "No student found.")


def update_student(students):
    s = pick_student(students)
    if not s:
        return
    print("Leave blank to keep current value.")
    s.name = ask(f"Name [{s.name}]: ").title() or s.name
    s.class_name = ask(f"Class [{s.class_name}]: ") or s.class_name
    g = ask(f"Gender [{s.gender}]: ").upper()
    if g in ("M", "F"):
        s.gender = g
    d = ask(f"DOB [{s.dob}]: ")
    if d and valid_date(d):
        s.dob = d
    elif d:
        print("Invalid date - DOB unchanged.")
    storage.save_students(students)
    print("Student updated.")


def delete_student(students):
    s = pick_student(students)
    if s and ask(f"Delete {s.name}? (y/n): ").lower() == "y":
        del students[s.student_id]
        storage.save_students(students)
        print("Student deleted.")


def record_scores(students):
    s = pick_student(students)
    if not s:
        return
    if s.scores:
        print("Existing scores:", s.scores)
        if ask("Replace them? (y/n): ").lower() != "y":
            return
    subjects = []
    print(f"Enter at least {results.MIN_SUBJECTS} subjects. Type 'done' to finish.")
    while True:
        sub = ask("Subject name: ").title()
        if sub.lower() == "done":
            if len(subjects) >= results.MIN_SUBJECTS:
                break
            print(f"You need at least {results.MIN_SUBJECTS} subjects.")
            continue
        if sub and sub not in subjects:
            subjects.append(sub)
            if len(subjects) >= results.MIN_SUBJECTS:
                print("  (minimum reached - add more or type 'done')")
    s.set_scores({})
    scores = {}
    for sub in subjects:
        scores[sub] = ask_score(sub)
    s.set_scores(scores)
    storage.save_students(students)
    print("Scores saved.")


def update_one_score(students):
    s = pick_student(students)
    if not s or not s.scores:
        print("No scores to update.")
        return
    print("Subjects:", ", ".join(s.scores))
    sub = ask("Subject to update: ").title()
    if sub not in s.scores:
        print("Subject not found.")
        return
    s.scores[sub] = ask_score(sub)
    s.set_scores(s.scores)
    storage.save_students(students)
    print("Score updated.")


def show_report_card(students):
    s = pick_student(students)
    if s:
        print(reports.report_card(s))


def list_results(students):
    if not students:
        print("No students registered.")
        return
    by = "name" if ask("Sort by (1) average or (2) name? ") == "2" else "average"
    print(reports.summary_table(reports.sort_students(students.values(), by)))


def class_stats(students):
    print(reports.stats_text(students.values()))


def export_report(students):
    try:
        path = reports.save_report(students.values())
        print(f"Report saved to {path}")
    except OSError as e:
        print(f"Could not save report: {e}")


MENU = """
===== STUDENT RESULT SYSTEM =====
1. Add student          7. Update one score
2. View all students    8. Show report card
3. Search student       9. List results (sorted)
4. Update student      10. Class statistics
5. Delete student      11. Save text report
6. Record scores        0. Exit
"""

ACTIONS = {
    "1": add_student, "2": view_students, "3": search_student,
    "4": update_student, "5": delete_student, "6": record_scores,
    "7": update_one_score, "8": show_report_card, "9": list_results,
    "10": class_stats, "11": export_report,
}


def main():
    students = storage.load_students()
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            storage.save_students(students)
            print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            try:
                action(students)
            except KeyboardInterrupt:
                print("\nCancelled.")
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
