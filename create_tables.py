import sqlite3

def create_tables():
    conn = sqlite3.connect('students.db')
    sql_file = open('schema.sql')
    sql_tables = sql_file.read()

    conn.executescript(sql_tables)
    conn.commit()
    conn.close()

    sql_file.close()

if __name__ == '__main__':
    create_tables()
