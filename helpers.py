from models import get_connection


def get_personal_bests(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT e.name, MAX(e.weight) as max_weight
            FROM exercises e
            JOIN workout_sessions s ON e.session_id = s.id
            WHERE s.user_id = ?
            GROUP BY e.name
        """, (user_id,)).fetchall()
    return [(r["name"], r["max_weight"]) for r in rows]


def prompt_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def prompt_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Please enter a valid number.")
