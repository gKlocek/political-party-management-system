def create_database(conn):
    cur = conn.cursor()
    cur.execute(open("init.sql", "r").read())
    cur.close()
    conn.commit()
