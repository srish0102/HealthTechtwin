import sqlite3
import pandas as pd

def init_db():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect('metabotwin.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            glucose INTEGER,
            bmi REAL,
            age INTEGER,
            risk_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_log(glucose, bmi, age, risk):
    """Saves a new record."""
    conn = sqlite3.connect('metabotwin.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (glucose, bmi, age, risk_score) VALUES (?, ?, ?, ?)',
              (glucose, bmi, age, risk))
    conn.commit()
    conn.close()

def get_history():
    """Fetches all past records."""
    conn = sqlite3.connect('metabotwin.db')
    try:
        df = pd.read_sql_query("SELECT timestamp, glucose, bmi, risk_score FROM history ORDER BY timestamp DESC", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df