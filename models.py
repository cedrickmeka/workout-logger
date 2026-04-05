import sqlite3

DB = "workout_logger.db"


def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                duration INTEGER NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                sets INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                weight REAL NOT NULL,
                FOREIGN KEY (session_id) REFERENCES workout_sessions(id)
            );
        """)


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

    @classmethod
    def create(cls, name):
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
            return cls(cursor.lastrowid, name)

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
            return cls(row["id"], row["name"]) if row else None

    @classmethod
    def all(cls):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM users").fetchall()
            return [cls(r["id"], r["name"]) for r in rows]

    def sessions(self):
        return WorkoutSession.find_by_user(self.id)


class WorkoutSession:
    def __init__(self, id, user_id, date, duration, notes):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.duration = duration
        self.notes = notes

    def __repr__(self):
        return f"Session(id={self.id}, date={self.date}, duration={self.duration}min)"

    @classmethod
    def create(cls, user_id, date, duration, notes=""):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO workout_sessions (user_id, date, duration, notes) VALUES (?, ?, ?, ?)",
                (user_id, date, duration, notes),
            )
            return cls(cursor.lastrowid, user_id, date, duration, notes)

    @classmethod
    def find_by_id(cls, session_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM workout_sessions WHERE id = ?", (session_id,)).fetchone()
            return cls(row["id"], row["user_id"], row["date"], row["duration"], row["notes"]) if row else None

    @classmethod
    def find_by_user(cls, user_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM workout_sessions WHERE user_id = ?", (user_id,)).fetchall()
            return [cls(r["id"], r["user_id"], r["date"], r["duration"], r["notes"]) for r in rows]

    def delete(self):
        with get_connection() as conn:
            conn.execute("DELETE FROM exercises WHERE session_id = ?", (self.id,))
            conn.execute("DELETE FROM workout_sessions WHERE id = ?", (self.id,))

    def exercises(self):
        return Exercise.find_by_session(self.id)


class Exercise:
    def __init__(self, id, session_id, name, sets, reps, weight):
        self.id = id
        self.session_id = session_id
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def __repr__(self):
        return f"Exercise(id={self.id}, name={self.name}, sets={self.sets}, reps={self.reps}, weight={self.weight}kg)"

    @classmethod
    def create(cls, session_id, name, sets, reps, weight):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO exercises (session_id, name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
                (session_id, name, sets, reps, weight),
            )
            return cls(cursor.lastrowid, session_id, name, sets, reps, weight)

    @classmethod
    def find_by_id(cls, exercise_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
            return cls(row["id"], row["session_id"], row["name"], row["sets"], row["reps"], row["weight"]) if row else None

    @classmethod
    def find_by_session(cls, session_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM exercises WHERE session_id = ?", (session_id,)).fetchall()
            return [cls(r["id"], r["session_id"], r["name"], r["sets"], r["reps"], r["weight"]) for r in rows]

    def update(self, sets=None, reps=None, weight=None):
        self.sets = sets or self.sets
        self.reps = reps or self.reps
        self.weight = weight or self.weight
        with get_connection() as conn:
            conn.execute(
                "UPDATE exercises SET sets = ?, reps = ?, weight = ? WHERE id = ?",
                (self.sets, self.reps, self.weight, self.id),
            )

    def delete(self):
        with get_connection() as conn:
            conn.execute("DELETE FROM exercises WHERE id = ?", (self.id,))
