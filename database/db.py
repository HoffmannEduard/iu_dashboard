import sqlite3

def create_connection():
    return sqlite3.connect(":memory:", check_same_thread=False)

def create_tables(conn) -> None:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS studium (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studiengang TEXT NOT NULL,
            studienabschluss TEXT NOT NULL,
            startdatum TEXT NOT NULL,
            zeitmodell TEXT NOT NULL,
            gesamt_ects INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modul (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modul_code TEXT NOT NULL,
            modul_titel TEXT NOT NULL,
            ects INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modulbuchung (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studium_id INTEGER NOT NULL,
            modul_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            pruefungsart TEXT,
            note REAL,
            FOREIGN KEY (studium_id) REFERENCES studium(id),
            FOREIGN KEY (modul_id) REFERENCES modul(id)
        )
    """)

    conn.commit()