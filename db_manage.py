import sqlite3 as sq
from pathlib import Path

MAIN_DB_PATH = Path("db_main.db")
MAILOUT_DB_PATH = Path("ras.db")
USER_COLUMNS = ("chat_id", "one", "two", "one_link", "two_link")
EDITABLE_USER_COLUMNS = {"one", "two", "one_link", "two_link"}


def _ensure_schema() -> None:
    with sq.connect(MAIN_DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                chat_id TEXT PRIMARY KEY,
                one TEXT NOT NULL DEFAULT 'False',
                two TEXT NOT NULL DEFAULT 'False',
                one_link TEXT NOT NULL DEFAULT '',
                two_link TEXT NOT NULL DEFAULT ''
            )
            """
        )

    with sq.connect(MAILOUT_DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS ras (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                rassilka TEXT NOT NULL DEFAULT 'False'
            )
            """
        )
        con.execute("INSERT OR IGNORE INTO ras (id, rassilka) VALUES (1, 'False')")


def _validate_user_column(column: str) -> str:
    if column not in USER_COLUMNS and column != "*":
        raise ValueError(f"Unsupported column: {column}")
    return column


_ensure_schema()


async def db_select_id_sys(column):
    _validate_user_column(column)

    with sq.connect(MAIN_DB_PATH) as con:
        sql = con.cursor()
        if column == "*":
            sql.execute(
                "SELECT chat_id, one, two, one_link, two_link FROM users ORDER BY chat_id"
            )
        else:
            sql.execute(f"SELECT {column} FROM users ORDER BY chat_id")
        return sql.fetchall()


async def db_update_sys(column, chat_id, text):
    if column not in EDITABLE_USER_COLUMNS:
        raise ValueError(f"Unsupported column: {column}")

    with sq.connect(MAIN_DB_PATH) as con:
        con.execute(
            f"UPDATE users SET {column} = ? WHERE chat_id = ?",
            (str(text), str(chat_id)),
        )
        con.commit()


async def db_select_sys(column, chat_id):
    _validate_user_column(column)

    with sq.connect(MAIN_DB_PATH) as con:
        sql = con.cursor()
        sql.execute(f"SELECT {column} FROM users WHERE chat_id = ?", (str(chat_id),))
        return sql.fetchone()


async def inicialization(chat_id):
    with sq.connect(MAIN_DB_PATH) as con:
        con.execute(
            """
            INSERT OR IGNORE INTO users (chat_id, one, two, one_link, two_link)
            VALUES (?, 'False', 'False', '', '')
            """,
            (str(chat_id),),
        )
        con.commit()


async def get_rasslika():
    with sq.connect(MAILOUT_DB_PATH) as con:
        sql = con.cursor()
        sql.execute("SELECT rassilka FROM ras WHERE id = 1")
        return sql.fetchall()


async def update_rasslika(text):
    with sq.connect(MAILOUT_DB_PATH) as con:
        con.execute("UPDATE ras SET rassilka = ? WHERE id = 1", (str(text),))
        con.commit()
