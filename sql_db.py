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


def add_entry(conn, user_id, guild_id, balance=0.0):

    sql = """ INSERT INTO wallet(user_id,guild_id,balance)
                VALUES(?,?,?)"""

    cur = conn.cursor()
    cur.execute(sql, (user_id, guild_id, balance))
    conn.commit()

    return cur.lastrowid


def update_entry(conn, user_id, guild_id, diff=0.0):
    sql = """ UPDATE wallet
                SET balance = balance + ?
                WHERE user_id = ? 
                AND guild_id = ?;"""

    cur = conn.cursor()
    cur.execute(sql, (diff, user_id, guild_id))
    conn.commit()


def select_entry(conn, user_id, guild_id):
    sql = """SELECT * FROM wallet
                WHERE user_id = ? 
                AND guild_id = ?;"""

    cur = conn.cursor()
    cur.execute(sql, (user_id, guild_id, ))
    rows = cur.fetchall()

    balance = 0

    if len(rows) > 0:
        balance = rows[0]

    return balance


def has_entry(conn, user_id, guild_id):
    val = select_entry(conn, user_id, guild_id)
    if val == 0:
        return False
    else:
        return True


def safe_add_entry(conn, user_id, guild_id):
    if not has_entry(conn, user_id, guild_id):
        add_entry(conn, user_id, guild_id)


def select_entry_sorted(conn, guild_id):
    sql = """SELECT * FROM wallet
                WHERE guild_id = ?
                ORDER BY balance DESC;"""

    cur = conn.cursor()
    cur.execute(sql, (guild_id, ))
    rows = cur.fetchall()

    return rows


def main():

    sql_create_wallet = """CREATE TABLE IF NOT EXISTS wallet (
                                user_id integer NOT NULL,
                                guild_id integer NOT NULL,
                                balance integer NOT NULL,
                                PRIMARY KEY ( user_id, guild_id )
                            );"""

    conn = create_conn("./sql_currency.db")

    #add_entry(conn, 10001, 3000, 0)
    update_entry(conn, 1212, 32434, 20)
    print(select_entry(conn, 1212, 3434))

    '''if conn is not None:
        create_table(conn, sql_create_wallet)
        print("Successfully Made table")
    else:
        print("Failed create")'''


if __name__ == "__main__":
    main()
    #add_user()