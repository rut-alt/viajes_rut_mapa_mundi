import sqlite3

def crear_db():

    conn = sqlite3.connect("viajes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_db()
