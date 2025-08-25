import os
import sqlite3
import qrcode
import io
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Database setup
DATABASE = 'qr_codes.db'

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            employee_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP NULL,
            is_used BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_qr_code(content, type_name, employee_name=None):
    """Generate QR code and save to database."""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO qr_codes (type, content, employee_name)
        VALUES (?, ?, ?)
    ''', (type_name, content, employee_name))
    
    qr_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return qr_id, img_base64

@app.route('/')
def index():
    """Main page with QR code generation options."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate QR code based on form data."""
    data = request.get_json()
    
    qr_type = data.get('type')
    employee_name = data.get('employee_name', '')
    
    # Generate unique content based on type and current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    content = f"{qr_type}_{timestamp}_{employee_name}"
    
    try:
        qr_id, img_base64 = generate_qr_code(content, qr_type, employee_name)
        
        return jsonify({
            'success': True,
            'qr_id': qr_id,
            'image': f"data:image/png;base64,{img_base64}",
            'content': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/list')
def list_qr_codes():
    """List all generated QR codes."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, type, content, employee_name, created_at, is_used
        FROM qr_codes
        ORDER BY created_at DESC
        LIMIT 50
    ''')
    
    qr_codes = []
    for row in cursor.fetchall():
        qr_codes.append({
            'id': row[0],
            'type': row[1],
            'content': row[2],
            'employee_name': row[3],
            'created_at': row[4],
            'is_used': row[5]
        })
    
    conn.close()
    return render_template('list.html', qr_codes=qr_codes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)