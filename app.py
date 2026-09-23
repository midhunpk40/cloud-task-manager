```python
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        task = request.form["task"]

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO tasks (task) VALUES (?)",
            (task,)
        )
        connection.commit()
        connection.close()

        return redirect("/")

    connection = get_db_connection()
    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()
    connection.close()

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
```
