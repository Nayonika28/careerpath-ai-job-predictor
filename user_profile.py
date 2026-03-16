"""
User Profile Module - Academic Details Management
==================================================

This module handles user profile management including academic details,
education history, and profile completion tracking.

Author: CareerPath AI Team
Date: 2026
"""

import sqlite3
import pandas as pd
from datetime import datetime

def create_user_profile_table():
    """Create user profile table for academic details"""
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_profiles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER UNIQUE,
                  degree TEXT,
                  specialization TEXT,
                  cgpa REAL,
                  university TEXT,
                  graduation_year INTEGER,
                  skills TEXT,
                  projects TEXT,
                  certifications TEXT,
                  profile_complete INTEGER DEFAULT 0,
                  created_at DATETIME,
                  updated_at DATETIME,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

def save_user_profile(user_id, degree, specialization, cgpa, university="", 
                      graduation_year=None, skills="", projects="", certifications=""):
    """Save or update user academic profile"""
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    
    # Check if profile exists
    c.execute("SELECT id FROM user_profiles WHERE user_id = ?", (user_id,))
    existing = c.fetchone()
    
    if existing:
        # Update existing profile
        c.execute('''UPDATE user_profiles 
                     SET degree = ?, specialization = ?, cgpa = ?, 
                         university = ?, graduation_year = ?, skills = ?,
                         projects = ?, certifications = ?, 
                         profile_complete = 1, updated_at = ?
                     WHERE user_id = ?''',
                 (degree, specialization, cgpa, university, graduation_year,
                  skills, projects, certifications, datetime.now(), user_id))
    else:
        # Insert new profile
        c.execute('''INSERT INTO user_profiles 
                     (user_id, degree, specialization, cgpa, university, 
                      graduation_year, skills, projects, certifications, 
                      profile_complete, created_at, updated_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)''',
                 (user_id, degree, specialization, cgpa, university, graduation_year,
                  skills, projects, certifications, datetime.now(), datetime.now()))
    
    conn.commit()
    conn.close()
    return True

def get_user_profile(user_id):
    """Get user academic profile"""
    conn = sqlite3.connect('career_path.db')
    df = pd.read_sql_query("SELECT * FROM user_profiles WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    
    if not df.empty:
        return df.iloc[0].to_dict()
    return None

def get_profile_completion_percentage(user_id):
    """Calculate profile completion percentage"""
    profile = get_user_profile(user_id)
    if profile is None:
        return 0
    
    fields = ['degree', 'specialization', 'cgpa', 'university', 'skills', 'projects', 'certifications']
    completed = sum(1 for field in fields if profile.get(field) and str(profile[field]).strip())
    return int((completed / len(fields)) * 100)

def update_profile_field(user_id, field_name, field_value):
    """Update specific profile field"""
    conn = sqlite3.connect('career_path.db')
    c = conn.cursor()
    
    c.execute(f'''UPDATE user_profiles 
                 SET {field_name} = ?, updated_at = ?
                 WHERE user_id = ?''',
             (field_value, datetime.now(), user_id))
    
    conn.commit()
    conn.close()
    return True

def get_all_profiles_summary():
    """Get summary of all user profiles for admin dashboard"""
    conn = sqlite3.connect('career_path.db')
    df = pd.read_sql_query('''SELECT u.name, u.email, up.degree, up.specialization, 
                                     up.cgpa, up.profile_complete, up.updated_at
                              FROM users u 
                              LEFT JOIN user_profiles up ON u.id = up.user_id
                              ORDER BY up.updated_at DESC''', conn)
    conn.close()
    return df
