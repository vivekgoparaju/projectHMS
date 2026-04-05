from app import create_app
from app.db import init_db, get_db
import sqlite3

app = create_app()

with app.app_context():
    init_db()
    db = get_db()
    try:
        db.execute('INSERT INTO admin (username, password) VALUES (?, ?)', ('admin', 'admin123'))
        db.commit()
        print("Initialized database and inserted root admin (admin/admin123).")
    except sqlite3.IntegrityError:
        print("Admin user already exists.")
