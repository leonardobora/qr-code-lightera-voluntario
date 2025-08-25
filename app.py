from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import qrcode
import io
import base64
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///qr_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models
class Employee(db.Model):
    """Modelo para funcionários que podem gerar QR codes"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    # Relacionamento com QR codes gerados
    qr_codes = db.relationship('QRCode', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.name}>'

class QRCode(db.Model):
    """Modelo para códigos QR gerados"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # festa, cestas, brinquedos, material_escolar
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=False)
    
    # Chave estrangeira para funcionário
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    
    def __repr__(self):
        return f'<QRCode {self.code}>'

class Usage(db.Model):
    """Modelo para rastrear uso dos QR codes"""
    id = db.Column(db.Integer, primary_key=True)
    qr_code_id = db.Column(db.Integer, db.ForeignKey('qr_code.id'), nullable=False)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)
    scanner_info = db.Column(db.String(200))  # Informações sobre quem escaneou
    
    # Relacionamento
    qr_code = db.relationship('QRCode', backref='usage_logs')
    
    def __repr__(self):
        return f'<Usage QR:{self.qr_code_id} at {self.scanned_at}>'

# Create database tables
with app.app_context():
    db.create_all()

# Categorias disponíveis
CATEGORIES = {
    'festa': 'Festa',
    'cestas': 'Cestas Básicas',
    'brinquedos': 'Brinquedos',
    'material_escolar': 'Material Escolar'
}

# Routes
@app.route('/')
def index():
    """Página inicial do sistema"""
    return render_template('index.html')

@app.route('/employees')
def employees():
    """Lista de funcionários"""
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/employees/new', methods=['GET', 'POST'])
def new_employee():
    """Cadastrar novo funcionário"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        
        if not all([name, email, department]):
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('employee_form.html')
        
        # Verificar se email já existe
        if Employee.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('employee_form.html')
        
        employee = Employee(name=name, email=email, department=department)
        db.session.add(employee)
        db.session.commit()
        
        flash('Funcionário cadastrado com sucesso!', 'success')
        return redirect(url_for('employees'))
    
    return render_template('employee_form.html')

@app.route('/qr-generator')
def qr_generator():
    """Página para gerar QR codes"""
    employees = Employee.query.filter_by(active=True).all()
    return render_template('qr_generator.html', employees=employees, categories=CATEGORIES)

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    """Gerar um novo QR code"""
    employee_id = request.form.get('employee_id')
    category = request.form.get('category')
    description = request.form.get('description', '')
    
    if not all([employee_id, category]):
        flash('Funcionário e categoria são obrigatórios!', 'error')
        return redirect(url_for('qr_generator'))
    
    if category not in CATEGORIES:
        flash('Categoria inválida!', 'error')
        return redirect(url_for('qr_generator'))
    
    # Gerar código único
    code = f"{category}_{uuid.uuid4().hex[:8]}"
    
    qr_code = QRCode(
        code=code,
        category=category,
        description=description,
        employee_id=employee_id
    )
    
    db.session.add(qr_code)
    db.session.commit()
    
    flash('QR Code gerado com sucesso!', 'success')
    return redirect(url_for('view_qr', qr_id=qr_code.id))

@app.route('/qr/<int:qr_id>')
def view_qr(qr_id):
    """Visualizar QR code gerado"""
    qr_code = QRCode.query.get_or_404(qr_id)
    
    # Gerar imagem do QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_code.code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converter para base64 para exibir no template
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return render_template('view_qr.html', qr_code=qr_code, img_base64=img_base64, categories=CATEGORIES)

@app.route('/scanner')
def scanner():
    """Página para escanear QR codes"""
    return render_template('scanner.html')

@app.route('/validate-qr', methods=['POST'])
def validate_qr():
    """Validar um QR code escaneado"""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({'success': False, 'message': 'Código não fornecido'})
    
    qr_code = QRCode.query.filter_by(code=code).first()
    
    if not qr_code:
        return jsonify({'success': False, 'message': 'QR Code não encontrado'})
    
    if qr_code.used:
        return jsonify({
            'success': False, 
            'message': f'QR Code já utilizado em {qr_code.used_at.strftime("%d/%m/%Y %H:%M")}'
        })
    
    # Marcar como usado
    qr_code.used = True
    qr_code.used_at = datetime.utcnow()
    
    # Registrar uso
    usage = Usage(qr_code_id=qr_code.id, scanner_info='Scanner web')
    db.session.add(usage)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'QR Code validado com sucesso!',
        'data': {
            'category': CATEGORIES.get(qr_code.category, qr_code.category),
            'description': qr_code.description,
            'employee': qr_code.employee.name,
            'created_at': qr_code.created_at.strftime('%d/%m/%Y %H:%M')
        }
    })

@app.route('/reports')
def reports():
    """Página de relatórios"""
    total_qr_codes = QRCode.query.count()
    used_qr_codes = QRCode.query.filter_by(used=True).count()
    
    # QR codes por categoria
    category_stats = {}
    for cat_key, cat_name in CATEGORIES.items():
        total = QRCode.query.filter_by(category=cat_key).count()
        used = QRCode.query.filter_by(category=cat_key, used=True).count()
        category_stats[cat_name] = {'total': total, 'used': used}
    
    recent_qr_codes = QRCode.query.order_by(QRCode.created_at.desc()).limit(10).all()
    recent_usage = Usage.query.order_by(Usage.scanned_at.desc()).limit(10).all()
    
    return render_template('reports.html',
                         total_qr_codes=total_qr_codes,
                         used_qr_codes=used_qr_codes,
                         category_stats=category_stats,
                         recent_qr_codes=recent_qr_codes,
                         recent_usage=recent_usage,
                         categories=CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)