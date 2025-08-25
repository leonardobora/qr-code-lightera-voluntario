from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with QR code scanner"""
    return render_template('index.html')

@app.route('/scanner')
def scanner():
    """QR Scanner page"""
    return render_template('scanner.html')

@app.route('/api/process_qr', methods=['POST'])
def process_qr():
    """Process scanned QR code data"""
    data = request.get_json()
    qr_data = data.get('qr_data', '')
    
    # Basic processing - in a real app, this would validate against database
    return jsonify({
        'success': True,
        'message': f'QR Code processado com sucesso!',
        'data': qr_data,
        'timestamp': data.get('timestamp', '')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)