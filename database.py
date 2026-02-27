
import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  email TEXT UNIQUE, 
                  password TEXT, 
                  role TEXT)''')
    # Predictions history
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  degree TEXT,
                  specialization TEXT,
                  cgpa REAL,
                  skills TEXT,
                  prediction TEXT,
                  timestamp DATETIME,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Create default admin if not exists
    c.execute("SELECT * FROM users WHERE email='admin@example.com'")
    if not c.fetchone():
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                  ('System Admin', 'admin@example.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin')) # pass: admin123
    
    conn.commit()
    conn.close()

def add_prediction(user_id, degree, specialization, cgpa, skills, prediction):
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, degree, specialization, cgpa, skills, prediction, timestamp) VALUES (?,?,?,?,?,?,?)",
              (user_id, degree, specialization, cgpa, skills, prediction, datetime.now()))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect('career_path.db')
    df = pd.read_sql_query(f"SELECT * FROM history WHERE user_id={user_id} ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def get_all_history():
    conn = sqlite3.connect('career_path.db')
    df = pd.read_sql_query("SELECT h.*, u.name as user_name FROM history h JOIN users u ON h.user_id = u.id ORDER BY h.timestamp DESC", conn)
    conn.close()
    return df
