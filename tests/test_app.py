import sqlite3

import pytest
import app as task_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "tasks.db"

    def get_test_db_connection():
        connection = sqlite3.connect(test_database)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(
        task_app,
        "get_db_connection",
        get_test_db_connection,
    )

    connection = get_test_db_connection()
    connection.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    connection.commit()
    connection.close()

    task_app.app.config.update(TESTING=True)

    with task_app.app.test_client() as test_client:
        yield test_client


def test_add_task(client, tmp_path):
    response = client.post("/", data={"task": "Learn GitHub OIDC"})

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    connection = sqlite3.connect(tmp_path / "tasks.db")
    task = connection.execute(
        "SELECT task FROM tasks"
    ).fetchone()[0]
    connection.close()

    assert task == "Learn GitHub OIDC"