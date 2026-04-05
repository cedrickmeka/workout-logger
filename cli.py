from models import initialize_db, User, WorkoutSession, Exercise
from helpers import get_personal_bests, prompt_int, prompt_float

current_user = None


def login_menu():
    global current_user
    print("\n=== Workout Logger ===")
    print("1. Login")
    print("2. Create Account")
    print("0. Exit")
    choice = input("Choose: ").strip()

    if choice == "1":
        name = input("Enter your username: ").strip()
        user = User.find_by_name(name)
        if user:
            current_user = user
            print(f"Welcome back, {user.name}!")
        else:
            print("User not found.")

    elif choice == "2":
        name = input("Choose a username: ").strip()
        if User.find_by_name(name):
            print("Username already taken.")
        else:
            current_user = User.create(name)
            print(f"Account created! Welcome, {current_user.name}!")

    elif choice == "0":
        print("Goodbye!")
        exit()


def main_menu():
    print(f"\n=== Menu ({current_user.name}) ===")
    print("1. Create new workout session")
    print("2. View all sessions")
    print("3. View a session and its exercises")
    print("4. Log an exercise to a session")
    print("5. Update an exercise")
    print("6. Delete an exercise")
    print("7. Delete a session")
    print("8. View personal bests")
    print("0. Logout")
    return input("Choose: ").strip()


def create_session():
    date = input("Date (YYYY-MM-DD): ").strip()
    duration = prompt_int("Duration (minutes): ")
    notes = input("Notes (optional): ").strip()
    session = WorkoutSession.create(current_user.id, date, duration, notes)
    print(f"Session created: {session}")


def view_all_sessions():
    sessions = current_user.sessions()
    if not sessions:
        print("No sessions found.")
        return
    for s in sessions:
        print(f"  [{s.id}] {s.date} | {s.duration} min | Notes: {s.notes or 'None'}")


def view_session():
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


def log_exercise():
    session_id = prompt_int("Enter session ID: ")
    session = WorkoutSession.find_by_id(session_id)
    if not session or session.user_id != current_user.id:
        print("Session not found.")
        return
    name = input("Exercise name: ").strip()
    sets = prompt_int("Sets: ")
    reps = prompt_int("Reps: ")
    weight = prompt_float("Weight (kg): ")
    exercise = Exercise.create(session_id, name, sets, reps, weight)
    print(f"Logged: {exercise}")


def update_exercise():
    exercise_id = prompt_int("Enter exercise ID: ")
    exercise = Exercise.find_by_id(exercise_id)
    if not exercise:
        print("Exercise not found.")
        return
    print("Leave blank to keep current value.")
    sets_input = input(f"Sets [{exercise.sets}]: ").strip()
    reps_input = input(f"Reps [{exercise.reps}]: ").strip()
    weight_input = input(f"Weight [{exercise.weight}]: ").strip()
    exercise.update(
        sets=int(sets_input) if sets_input else None,
        reps=int(reps_input) if reps_input else None,
        weight=float(weight_input) if weight_input else None,
    )
    print(f"Updated: {exercise}")


def delete_exercise():
    exercise_id = prompt_int("Enter exercise ID: ")
    exercise = Exercise.find_by_id(exercise_id)
    if not exercise:
        print("Exercise not found.")
        return
    exercise.delete()
    print("Exercise deleted.")


def delete_session():
    session_id = prompt_int("Enter session ID: ")
    session = WorkoutSession.find_by_id(session_id)
    if not session or session.user_id != current_user.id:
        print("Session not found.")
        return
    session.delete()
    print("Session and its exercises deleted.")


def view_personal_bests():
    bests = get_personal_bests(current_user.id)
    if not bests:
        print("No data yet.")
        return
    print("\n--- Personal Bests ---")
    for name, weight in bests:
        print(f"  {name}: {weight}kg")


def run():
    initialize_db()
    while not current_user:
        login_menu()

    actions = {
        "1": create_session,
        "2": view_all_sessions,
        "3": view_session,
        "4": log_exercise,
        "5": update_exercise,
        "6": delete_exercise,
        "7": delete_session,
        "8": view_personal_bests,
    }

    while True:
        choice = main_menu()
        if choice == "0":
            print("Logged out.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()
