import sqlite3
from datetime import datetime

DATABASE = "predictions.db"


def init_db():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journeys (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source TEXT,

            destination TEXT,

            distance REAL,

            duration REAL,

            risk_score INTEGER,

            risk_level TEXT,

            highest_section INTEGER,

            created_at TEXT

        )
    """)

    connection.commit()

    connection.close()


def save_journey(
    source,
    destination,
    distance,
    duration,
    risk_score,
    risk_level,
    highest_section
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO journeys
        (
            source,
            destination,
            distance,
            duration,
            risk_score,
            risk_level,
            highest_section,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source,
        destination,
        distance,
        duration,
        risk_score,
        risk_level,
        highest_section,
        datetime.now().isoformat()
    ))

    connection.commit()

    connection.close()


def get_history():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM journeys
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]