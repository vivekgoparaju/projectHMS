import sqlite3
import urllib.parse

db_path = 'app/database/data.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

doctors = cur.execute('SELECT id, name FROM doctors').fetchall()

for doc_id, name in doctors:
    # Use UI Avatars to generate a professional, modern badge-style avatar for the doctor
    # E.g. "Dr. John Doe" -> "DJ" on a colored background
    encoded_name = urllib.parse.quote(name)
    img_url = f"https://ui-avatars.com/api/?name={encoded_name}&background=random&color=fff&size=150&rounded=true&font-size=0.33"
    cur.execute('UPDATE doctors SET img_url = ? WHERE id = ?', (img_url, doc_id))

conn.commit()
conn.close()

print("Successfully updated doctor images to professional badges!")
