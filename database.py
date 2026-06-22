import sqlite3

conn = sqlite3.connect("study.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS uploads(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    pages INTEGER,
    words INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully!")