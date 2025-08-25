from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from database import init_database, add_qr_code, get_qr_code, mark_qr_used, get_all_qr_codes
from qr_generator import generate_festa_qr_code, validate_festa_qr_code

app = Flask(__name__)
app.secret_key = 'festa_qr_secret_key_2024'  # Change this in production

# Initialize database on startup
init_database()

@app.route('/')
def index():
    """Main page for QR code generation"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    """Generate a new QR code for Festa de Final de Ano"""
    employee_name = request.form.get('employee_name', '').strip()
    employee_id = request.form.get('employee_id', '').strip()
    
    if not employee_name or not employee_id:
        flash('Nome e ID do funcionário são obrigatórios!', 'error')
        return redirect(url_for('index'))
    
    # Check if QR code already exists for this employee
    existing_qr = get_qr_code(employee_id)
    if existing_qr:
        flash(f'QR Code já existe para o funcionário {employee_id}!', 'warning')
        return render_template('qr_result.html', qr_code=existing_qr)
    
    try:
        # Generate QR code
        qr_data, qr_image_path = generate_festa_qr_code(employee_name, employee_id)
        
        # Save to database
        qr_id = add_qr_code(employee_name, employee_id, qr_data, qr_image_path)
        
        if qr_id:
            qr_code = get_qr_code(employee_id)
            flash('QR Code gerado com sucesso!', 'success')
            return render_template('qr_result.html', qr_code=qr_code)
        else:
            flash('Erro ao salvar QR Code no banco de dados!', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Erro ao gerar QR Code: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/validate', methods=['GET', 'POST'])
def validate_qr():
    """Validate a QR code"""
    if request.method == 'GET':
        return render_template('validate.html')
    
    qr_data = request.form.get('qr_data', '').strip()
    
    if not qr_data:
        flash('Dados do QR Code são obrigatórios!', 'error')
        return render_template('validate.html')
    
    # Validate QR code format
    is_valid, employee_id, employee_name = validate_festa_qr_code(qr_data)
    
    if not is_valid:
        flash('QR Code inválido ou não é para a Festa de Final de Ano!', 'error')
        return render_template('validate.html')
    
    # Check in database
    qr_code = get_qr_code(employee_id)
    
    if not qr_code:
        flash('QR Code não encontrado no sistema!', 'error')
        return render_template('validate.html')
    
    if qr_code['is_used']:
        flash(f'QR Code já foi utilizado em {qr_code["used_at"]}!', 'warning')
        return render_template('validate_result.html', qr_code=qr_code, validation_status='used')
    
    # Mark as used
    mark_qr_used(employee_id)
    qr_code['is_used'] = True
    qr_code['used_at'] = 'Agora'
    
    flash('QR Code validado com sucesso! Entrada liberada.', 'success')
    return render_template('validate_result.html', qr_code=qr_code, validation_status='valid')

@app.route('/api/validate', methods=['POST'])
def api_validate_qr():
    """API endpoint for QR code validation (for mobile scanning)"""
    data = request.get_json()
    qr_data = data.get('qr_data', '').strip() if data else ''
    
    if not qr_data:
        return jsonify({'success': False, 'message': 'QR data is required'})
    
    # Validate QR code format
    is_valid, employee_id, employee_name = validate_festa_qr_code(qr_data)
    
    if not is_valid:
        return jsonify({'success': False, 'message': 'Invalid QR code format'})
    
    # Check in database
    qr_code = get_qr_code(employee_id)
    
    if not qr_code:
        return jsonify({'success': False, 'message': 'QR code not found'})
    
    if qr_code['is_used']:
        return jsonify({
            'success': False, 
            'message': f'QR code already used at {qr_code["used_at"]}',
            'employee_name': qr_code['employee_name'],
            'employee_id': qr_code['employee_id']
        })
    
    # Mark as used
    mark_qr_used(employee_id)
    
    return jsonify({
        'success': True,
        'message': 'QR code validated successfully',
        'employee_name': qr_code['employee_name'],
        'employee_id': qr_code['employee_id']
    })

@app.route('/list')
def list_qr_codes():
    """List all generated QR codes"""
    qr_codes = get_all_qr_codes()
    return render_template('list.html', qr_codes=qr_codes)

@app.route('/scanner')
def scanner():
    """QR code scanner page"""
    return render_template('scanner.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)