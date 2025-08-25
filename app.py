import sqlite3
import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import qrcode
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database configuration
DATABASE = 'cestas_natal.db'

def get_db_connection():
    """Get database connection"""
    # Use DATABASE from config if testing, otherwise use global DATABASE
    db_path = app.config.get('DATABASE', DATABASE) if app else DATABASE
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cestas_natal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_funcionario TEXT NOT NULL,
                nome_funcionario TEXT NOT NULL,
                departamento TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_retirada TIMESTAMP,
                status TEXT DEFAULT 'disponivel'
            )
        ''')
        conn.commit()

def generate_qr_code(data):
    """Generate QR code for given data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for web display
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode()
    
    return img_base64

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/cestas')
def cestas():
    """List all Christmas baskets"""
    with get_db_connection() as conn:
        cestas = conn.execute(
            'SELECT * FROM cestas_natal ORDER BY data_criacao DESC'
        ).fetchall()
    return render_template('cestas.html', cestas=cestas)

@app.route('/cestas/nova', methods=['GET', 'POST'])
def nova_cesta():
    """Create new Christmas basket"""
    if request.method == 'POST':
        codigo_funcionario = request.form['codigo_funcionario']
        nome_funcionario = request.form['nome_funcionario']
        departamento = request.form.get('departamento', '')
        
        if not codigo_funcionario or not nome_funcionario:
            flash('Código do funcionário e nome são obrigatórios', 'error')
            return render_template('nova_cesta.html')
        
        with get_db_connection() as conn:
            # Check if employee already has a basket
            existing = conn.execute(
                'SELECT id FROM cestas_natal WHERE codigo_funcionario = ? AND status = "disponivel"',
                (codigo_funcionario,)
            ).fetchone()
            
            if existing:
                flash('Funcionário já possui uma cesta de Natal disponível', 'error')
                return render_template('nova_cesta.html')
            
            # Create new basket
            cursor = conn.execute(
                'INSERT INTO cestas_natal (codigo_funcionario, nome_funcionario, departamento) VALUES (?, ?, ?)',
                (codigo_funcionario, nome_funcionario, departamento)
            )
            cesta_id = cursor.lastrowid
            conn.commit()
        
        flash('Cesta de Natal criada com sucesso!', 'success')
        return redirect(url_for('cesta_qr', cesta_id=cesta_id))
    
    return render_template('nova_cesta.html')

@app.route('/cestas/<int:cesta_id>/qr')
def cesta_qr(cesta_id):
    """Display QR code for basket"""
    with get_db_connection() as conn:
        cesta = conn.execute(
            'SELECT * FROM cestas_natal WHERE id = ?',
            (cesta_id,)
        ).fetchone()
    
    if not cesta:
        flash('Cesta não encontrada', 'error')
        return redirect(url_for('cestas'))
    
    # Generate QR code data
    qr_data = f"CESTA_NATAL|{cesta['id']}|{cesta['codigo_funcionario']}|{cesta['nome_funcionario']}"
    qr_code_base64 = generate_qr_code(qr_data)
    
    return render_template('cesta_qr.html', cesta=cesta, qr_code=qr_code_base64)

@app.route('/scanner')
def scanner():
    """QR code scanner page"""
    return render_template('scanner.html')

@app.route('/api/validar_qr', methods=['POST'])
def validar_qr():
    """Validate QR code and process basket pickup"""
    data = request.get_json()
    qr_content = data.get('qr_content', '')
    
    try:
        # Parse QR code content
        parts = qr_content.split('|')
        if len(parts) != 4 or parts[0] != 'CESTA_NATAL':
            return jsonify({'success': False, 'message': 'QR Code inválido'})
        
        cesta_id = int(parts[1])
        codigo_funcionario = parts[2]
        nome_funcionario = parts[3]
        
        with get_db_connection() as conn:
            # Get basket info
            cesta = conn.execute(
                'SELECT * FROM cestas_natal WHERE id = ? AND codigo_funcionario = ?',
                (cesta_id, codigo_funcionario)
            ).fetchone()
            
            if not cesta:
                return jsonify({'success': False, 'message': 'Cesta não encontrada'})
            
            if cesta['status'] == 'retirada':
                return jsonify({
                    'success': False, 
                    'message': f'Cesta já foi retirada em {cesta["data_retirada"]}'
                })
            
            # Mark as picked up
            conn.execute(
                'UPDATE cestas_natal SET status = "retirada", data_retirada = CURRENT_TIMESTAMP WHERE id = ?',
                (cesta_id,)
            )
            conn.commit()
        
        return jsonify({
            'success': True,
            'message': f'Cesta retirada com sucesso!',
            'funcionario': nome_funcionario,
            'codigo': codigo_funcionario
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao processar QR Code: {str(e)}'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)