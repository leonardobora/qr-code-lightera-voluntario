import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'festa_qrcodes.db'

def init_database():
    """Initialize the SQLite database for storing QR codes"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create table for festa QR codes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS festa_qrcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            qr_code_data TEXT NOT NULL,
            qr_image_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_used BOOLEAN DEFAULT FALSE,
            used_at TIMESTAMP NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_qr_code(employee_name, employee_id, qr_code_data, qr_image_path):
    """Add a new QR code to the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO festa_qrcodes (employee_name, employee_id, qr_code_data, qr_image_path)
            VALUES (?, ?, ?, ?)
        ''', (employee_name, employee_id, qr_code_data, qr_image_path))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Employee ID already exists
    finally:
        conn.close()

def get_qr_code(employee_id):
    """Get QR code information by employee ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM festa_qrcodes WHERE employee_id = ?
    ''', (employee_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'employee_name': result[1],
            'employee_id': result[2],
            'qr_code_data': result[3],
            'qr_image_path': result[4],
            'created_at': result[5],
            'is_used': result[6],
            'used_at': result[7]
        }
    return None

def mark_qr_used(employee_id):
    """Mark a QR code as used"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE festa_qrcodes 
        SET is_used = TRUE, used_at = CURRENT_TIMESTAMP
        WHERE employee_id = ?
    ''', (employee_id,))
    
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()
    
    return affected_rows > 0

def get_all_qr_codes():
    """Get all QR codes"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM festa_qrcodes ORDER BY created_at DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    qr_codes = []
    for result in results:
        qr_codes.append({
            'id': result[0],
            'employee_name': result[1],
            'employee_id': result[2],
            'qr_code_data': result[3],
            'qr_image_path': result[4],
            'created_at': result[5],
            'is_used': result[6],
            'used_at': result[7]
        })
    
    return qr_codes

if __name__ == '__main__':
    init_database()
    print("Database initialized successfully!")