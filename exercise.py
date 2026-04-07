from models import WorkoutSession, Exercise
from helpers import get_personal_bests, prompt_int, prompt_float


def log_exercise(current_user):
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


def view_personal_bests(current_user):
    bests = get_personal_bests(current_user.id)
    if not bests:
        print("No data yet.")
        return
    print("\n--- Personal Bests ---")
    for name, weight in bests:
        print(f"  {name}: {weight}kg")
