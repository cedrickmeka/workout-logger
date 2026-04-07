# Workout Logger CLI
A simple command-line app built using Python and SQLite. It lets you log your workout sessions and keep track of the exercises you did in each one.

# What it does
-Create a workout session (date, duration, notes)
-Add exercises to a session (name, sets, reps, weight)
-View all your sessions
-View a session and the exercises in it
-Update an exercise
-Delete an exercise or a whole session
-See your personal best (heaviest weight) for each exercise

# File tree
workout_logger/
├── cli.py
├── login.py
├── session.py
├── exercise.py
├── models.py
├── helpers.py
├── README.md
├── workout_logger.db
└── .gitignore

# How the data is connected
User → WorkoutSession → Exercise

A user can have many sessions and each session can have many exercises.

# How it runs
No installs needed. It uses Python's built-in sqlite3 module and creates a workout_logger.db file automatically when you run it for the first time.
