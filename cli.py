from login import login_menu, current_user as auth_user
from session import create_session, view_all_sessions, view_session, delete_session
from exercise import log_exercise, update_exercise, delete_exercise, view_personal_bests
import login


def main_menu():
    print(f"\n=== Menu ({login.current_user.name}) ===")
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


def run():
    while not login.current_user:
        login_menu()

    user = login.current_user

    actions = {
        "1": lambda: create_session(user),
        "2": lambda: view_all_sessions(user),
        "3": lambda: view_session(user),
        "4": lambda: log_exercise(user),
        "5": update_exercise,
        "6": delete_exercise,
        "7": lambda: delete_session(user),
        "8": lambda: view_personal_bests(user),
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
