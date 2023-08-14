import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    photo TEXT,
    faculty TEXT,
    faculty_choose TEXT,
    teams TEXT,
    isu INTEGER,
    contact TEXT
    )""")
    db.commit()

async def add_user(state):
    data = await state.get_data()
    cur.execute("INSERT INTO users (name, photo, faculty, faculty_choose, teams, isu, contact) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data['name'], data['photo'], data['faculty'], data['faculty_choose'], data['teams'], data['isu'], data['contact']))
    db.commit()