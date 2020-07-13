import sqlite3 as sql
from sqlite3 import Error


# handler class for SQLite 3

def create_conn(db_file):
    conn = None

    try:
        conn = sql.connect(db_file)
        print(sql.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():

    sql_create_wallet = """CREATE TABLE IF NOT EXISTS wallet (
                                user_id integer PRIMARY KEY,
                                guild_id integer PRIMARY KEY,
                                balance integer NOT NULL,
                            );"""

    conn = create_conn("./sql_currency.db")

    if conn is not None:
        create_table(conn, sql_create_wallet)
        print("Successfully Made table")
    else:
        print("Failed create")


if __name__ == "__main__":
    main()