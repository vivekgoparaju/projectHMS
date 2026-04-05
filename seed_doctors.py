import sqlite3
from faker import Faker
import random

fake = Faker()

specializations = [
    "Cardiologist", "Neurologist", "Pediatrician", "Orthopedic", 
    "Dermatologist", "Psychiatrist", "Radiologist", "General Surgeon",
    "Oncologist", "Endocrinologist", "Gastroenterologist"
]

db_path = 'app/database/data.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

for _ in range(20):
    name = "Dr. " + fake.last_name()
    email = fake.email()
    password = 'password123' # Default password for all seed doctors
    specialization = random.choice(specializations)
    phone = fake.phone_number()
    # Random placeholder image from pravatar
    img_url = f"https://i.pravatar.cc/150?u={fake.uuid4()}"
    
    cur.execute('''
        INSERT INTO doctors (name, email, password, specialization, phone, img_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, password, specialization, phone, img_url))

conn.commit()
conn.close()

print("Successfully seeded 20 mock doctors to the database!")
