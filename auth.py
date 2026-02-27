
import hashlib
import sqlite3

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def create_user(name, email, password, role='user'):
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(name, email, password, role) VALUES (?,?,?,?)', (name, email, make_hashes(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email =? AND password =?', (email, make_hashes(password)))
    data = c.fetchone()
    conn.close()
    return data
