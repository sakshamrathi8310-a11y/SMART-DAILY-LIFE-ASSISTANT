import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sleep REAL,
        screen_time REAL,
        steps REAL,
        work_hours REAL,
        mood REAL,
        food REAL,
        stress INTEGER,
        productivity REAL,
        health REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_data(row):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO history (sleep,screen_time,steps,work_hours,mood,food,stress,productivity,health)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, tuple(row))

    conn.commit()
    conn.close()


def load_data():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql("SELECT * FROM history", conn)
    conn.close()
    return df