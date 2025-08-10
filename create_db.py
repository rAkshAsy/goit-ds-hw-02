import sqlite3

def create_db():
    with open('tables_create.sql', 'r') as f:
        sql = f.read()
    
    with sqlite3.connect('hw_db.db') as conn:
        cur = conn.cursor()
        cur.executescript(sql)

if __name__ == "__main__":
    create_db()