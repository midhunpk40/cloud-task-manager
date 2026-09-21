import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0
)
""")

connection.commit()
connection.close()

print("Database created successfully!")