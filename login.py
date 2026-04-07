from models import User

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
