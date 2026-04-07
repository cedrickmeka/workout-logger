from models import WorkoutSession
from helpers import prompt_int


def create_session(current_user):
    date = input("Date (YYYY-MM-DD): ").strip()
    duration = prompt_int("Duration (minutes): ")
    notes = input("Notes (optional): ").strip()
    session = WorkoutSession.create(current_user.id, date, duration, notes)
    print(f"Session created: {session}")


def view_all_sessions(current_user):
    sessions = current_user.sessions()
    if not sessions:
        print("No sessions found.")
        return
    for s in sessions:
        print(f"  [{s.id}] {s.date} | {s.duration} min | Notes: {s.notes or 'None'}")


def view_session(current_user):
    session_id = prompt_int("Enter session ID: ")
    session = WorkoutSession.find_by_id(session_id)
    if not session or session.user_id != current_user.id:
        print("Session not found.")
        return
    print(f"\n{session}")
    exercises = session.exercises()
    if not exercises:
        print("  No exercises logged.")
    for e in exercises:
        print(f"  [{e.id}] {e.name} | {e.sets} sets x {e.reps} reps @ {e.weight}kg")


def delete_session(current_user):
    session_id = prompt_int("Enter session ID: ")
    session = WorkoutSession.find_by_id(session_id)
    if not session or session.user_id != current_user.id:
        print("Session not found.")
        return
    session.delete()
    print("Session and its exercises deleted.")
