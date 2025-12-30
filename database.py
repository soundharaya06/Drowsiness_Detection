import sqlite3
import os

os.makedirs("databases", exist_ok=True)

conn = sqlite3.connect("databases/system.db")
c = conn.cursor()

# Employees table
c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    role TEXT
)
""")

# Logs table
c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    eye_status TEXT,
    drowsy TEXT,
    timestamp TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
""")

conn.commit()
conn.close()

print("✅ system.db with employees & logs tables created")
