import sqlite3
import qrcode
import uuid
from datetime import datetime, timedelta
from enum import Enum
from flask import Flask, request, jsonify, render_template_string
import io
import base64

class QRStatus(Enum):
    PENDING = "pending"
    USED = "used"
    EXPIRED = "expired"

class QRType(Enum):
    FESTA = "festa"
    CESTAS = "cestas"
    BRINQUEDOS = "brinquedos"
    MATERIAL_ESCOLAR = "material_escolar"

class QRCodeValidator:
    def __init__(self, db_path="qr_codes.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with QR codes table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                qr_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP NULL,
                expires_at TIMESTAMP NOT NULL,
                employee_id TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_qr_code(self, qr_type: QRType, employee_id: str, duration_hours: int = 24, metadata: str = ""):
        """Generate a new QR code with specified type and expiration"""
        code = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=duration_hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO qr_codes (code, qr_type, status, expires_at, employee_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (code, qr_type.value, QRStatus.PENDING.value, expires_at, employee_id, metadata))
            
            conn.commit()
            
            # Generate QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return {
                "success": True,
                "code": code,
                "qr_type": qr_type.value,
                "expires_at": expires_at.isoformat(),
                "qr_image": f"data:image/png;base64,{img_base64}"
            }
            
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Code already exists"}
        finally:
            conn.close()
    
    def validate_qr_code(self, code: str):
        """Validate a QR code and return its status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT code, qr_type, status, created_at, used_at, expires_at, employee_id, metadata
            FROM qr_codes WHERE code = ?
        ''', (code,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"valid": False, "error": "QR code not found"}
        
        code, qr_type, status, created_at, used_at, expires_at, employee_id, metadata = result
        expires_at_dt = datetime.fromisoformat(expires_at)
        
        # Check if expired
        if datetime.now() > expires_at_dt and status == QRStatus.PENDING.value:
            self._update_status(code, QRStatus.EXPIRED)
            status = QRStatus.EXPIRED.value
        
        return {
            "valid": True,
            "code": code,
            "qr_type": qr_type,
            "status": status,
            "created_at": created_at,
            "used_at": used_at,
            "expires_at": expires_at,
            "employee_id": employee_id,
            "metadata": metadata,
            "is_usable": status == QRStatus.PENDING.value
        }
    
    def use_qr_code(self, code: str):
        """Mark a QR code as used"""
        validation = self.validate_qr_code(code)
        
        if not validation["valid"]:
            return validation
        
        if validation["status"] != QRStatus.PENDING.value:
            return {
                "success": False,
                "error": f"QR code cannot be used. Status: {validation['status']}"
            }
        
        self._update_status(code, QRStatus.USED)
        
        return {
            "success": True,
            "message": "QR code successfully used",
            "code": code,
            "used_at": datetime.now().isoformat()
        }
    
    def _update_status(self, code: str, status: QRStatus):
        """Update QR code status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status == QRStatus.USED:
            cursor.execute('''
                UPDATE qr_codes SET status = ?, used_at = CURRENT_TIMESTAMP
                WHERE code = ?
            ''', (status.value, code))
        else:
            cursor.execute('''
                UPDATE qr_codes SET status = ?
                WHERE code = ?
            ''', (status.value, code))
        
        conn.commit()
        conn.close()
    
    def get_qr_codes_by_employee(self, employee_id: str):
        """Get all QR codes for a specific employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT code, qr_type, status, created_at, used_at, expires_at, metadata
            FROM qr_codes WHERE employee_id = ?
            ORDER BY created_at DESC
        ''', (employee_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            "code": row[0],
            "qr_type": row[1],
            "status": row[2],
            "created_at": row[3],
            "used_at": row[4],
            "expires_at": row[5],
            "metadata": row[6]
        } for row in results]

# Flask Application
app = Flask(__name__)
validator = QRCodeValidator()

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema QR Codes - Lightera Voluntário</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
</head>
<body class="bg-light">
    <div class="container mt-4">
        <h1 class="text-center mb-4">Sistema QR Codes - Lightera Voluntário</h1>
        
        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs" id="mainTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="validate-tab" data-bs-toggle="tab" data-bs-target="#validate" type="button">
                    Validar QR Code
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="generate-tab" data-bs-toggle="tab" data-bs-target="#generate" type="button">
                    Gerar QR Code
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="scan-tab" data-bs-toggle="tab" data-bs-target="#scan" type="button">
                    Escanear QR Code
                </button>
            </li>
        </ul>
        
        <div class="tab-content mt-3" id="mainTabsContent">
            <!-- Validate QR Code Tab -->
            <div class="tab-pane fade show active" id="validate" role="tabpanel">
                <div class="card">
                    <div class="card-header">
                        <h5>Validar QR Code</h5>
                    </div>
                    <div class="card-body">
                        <form id="validateForm">
                            <div class="mb-3">
                                <label for="codeInput" class="form-label">Código QR</label>
                                <input type="text" class="form-control" id="codeInput" placeholder="Cole ou digite o código QR" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Validar</button>
                            <button type="button" class="btn btn-success ms-2" id="useCodeBtn" style="display:none;">Usar QR Code</button>
                        </form>
                        <div id="validateResult" class="mt-3"></div>
                    </div>
                </div>
            </div>
            
            <!-- Generate QR Code Tab -->
            <div class="tab-pane fade" id="generate" role="tabpanel">
                <div class="card">
                    <div class="card-header">
                        <h5>Gerar QR Code</h5>
                    </div>
                    <div class="card-body">
                        <form id="generateForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="qrType" class="form-label">Tipo</label>
                                        <select class="form-select" id="qrType" required>
                                            <option value="">Selecione o tipo</option>
                                            <option value="festa">Festa</option>
                                            <option value="cestas">Cestas</option>
                                            <option value="brinquedos">Brinquedos</option>
                                            <option value="material_escolar">Material Escolar</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="employeeId" class="form-label">ID Funcionário</label>
                                        <input type="text" class="form-control" id="employeeId" required>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="duration" class="form-label">Duração (horas)</label>
                                        <input type="number" class="form-control" id="duration" value="24" min="1" max="168" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="metadata" class="form-label">Observações (opcional)</label>
                                        <input type="text" class="form-control" id="metadata">
                                    </div>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Gerar QR Code</button>
                        </form>
                        <div id="generateResult" class="mt-3"></div>
                    </div>
                </div>
            </div>
            
            <!-- Scan QR Code Tab -->
            <div class="tab-pane fade" id="scan" role="tabpanel">
                <div class="card">
                    <div class="card-header">
                        <h5>Escanear QR Code</h5>
                    </div>
                    <div class="card-body">
                        <div id="reader" style="width: 100%; max-width: 600px; margin: 0 auto;"></div>
                        <button id="startScan" class="btn btn-primary mt-3">Iniciar Scanner</button>
                        <button id="stopScan" class="btn btn-secondary mt-3" style="display:none;">Parar Scanner</button>
                        <div id="scanResult" class="mt-3"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Validate QR Code
        document.getElementById('validateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const code = document.getElementById('codeInput').value;
            
            try {
                const response = await fetch('/api/validate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code: code})
                });
                
                const result = await response.json();
                displayValidationResult(result);
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('validateResult').innerHTML = 
                    '<div class="alert alert-danger">Erro ao validar QR code</div>';
            }
        });
        
        // Use QR Code
        document.getElementById('useCodeBtn').addEventListener('click', async function() {
            const code = document.getElementById('codeInput').value;
            
            try {
                const response = await fetch('/api/use', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code: code})
                });
                
                const result = await response.json();
                if (result.success) {
                    document.getElementById('validateResult').innerHTML = 
                        '<div class="alert alert-success">QR Code usado com sucesso!</div>';
                    document.getElementById('useCodeBtn').style.display = 'none';
                } else {
                    document.getElementById('validateResult').innerHTML = 
                        `<div class="alert alert-danger">${result.error}</div>`;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
        
        // Generate QR Code
        document.getElementById('generateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                qr_type: document.getElementById('qrType').value,
                employee_id: document.getElementById('employeeId').value,
                duration_hours: parseInt(document.getElementById('duration').value),
                metadata: document.getElementById('metadata').value
            };
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                displayGenerationResult(result);
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('generateResult').innerHTML = 
                    '<div class="alert alert-danger">Erro ao gerar QR code</div>';
            }
        });
        
        function displayValidationResult(result) {
            const resultDiv = document.getElementById('validateResult');
            const useBtn = document.getElementById('useCodeBtn');
            
            if (!result.valid) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
                useBtn.style.display = 'none';
                return;
            }
            
            let statusClass = 'warning';
            if (result.status === 'used') statusClass = 'secondary';
            else if (result.status === 'expired') statusClass = 'danger';
            else if (result.status === 'pending') statusClass = 'success';
            
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                    <h6>Informações do QR Code</h6>
                    <p><strong>Código:</strong> ${result.code}</p>
                    <p><strong>Tipo:</strong> ${result.qr_type}</p>
                    <p><strong>Status:</strong> <span class="badge bg-${statusClass}">${result.status}</span></p>
                    <p><strong>Funcionário:</strong> ${result.employee_id}</p>
                    <p><strong>Criado em:</strong> ${new Date(result.created_at).toLocaleString('pt-BR')}</p>
                    <p><strong>Expira em:</strong> ${new Date(result.expires_at).toLocaleString('pt-BR')}</p>
                    ${result.used_at ? `<p><strong>Usado em:</strong> ${new Date(result.used_at).toLocaleString('pt-BR')}</p>` : ''}
                    ${result.metadata ? `<p><strong>Observações:</strong> ${result.metadata}</p>` : ''}
                </div>
            `;
            
            useBtn.style.display = result.is_usable ? 'inline-block' : 'none';
        }
        
        function displayGenerationResult(result) {
            const resultDiv = document.getElementById('generateResult');
            
            if (!result.success) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
                return;
            }
            
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <h6>QR Code gerado com sucesso!</h6>
                    <p><strong>Código:</strong> ${result.code}</p>
                    <p><strong>Tipo:</strong> ${result.qr_type}</p>
                    <p><strong>Expira em:</strong> ${new Date(result.expires_at).toLocaleString('pt-BR')}</p>
                    <div class="text-center mt-3">
                        <img src="${result.qr_image}" alt="QR Code" class="img-fluid" style="max-width: 200px;">
                    </div>
                </div>
            `;
        }
        
        // QR Code Scanner
        let html5QrcodeScanner = null;
        
        document.getElementById('startScan').addEventListener('click', function() {
            if (html5QrcodeScanner) {
                html5QrcodeScanner.clear();
            }
            
            html5QrcodeScanner = new Html5QrcodeScanner(
                "reader",
                { fps: 10, qrbox: {width: 250, height: 250} },
                false
            );
            
            html5QrcodeScanner.render(onScanSuccess, onScanFailure);
            
            document.getElementById('startScan').style.display = 'none';
            document.getElementById('stopScan').style.display = 'inline-block';
        });
        
        document.getElementById('stopScan').addEventListener('click', function() {
            if (html5QrcodeScanner) {
                html5QrcodeScanner.clear();
                html5QrcodeScanner = null;
            }
            
            document.getElementById('startScan').style.display = 'inline-block';
            document.getElementById('stopScan').style.display = 'none';
            document.getElementById('scanResult').innerHTML = '';
        });
        
        function onScanSuccess(decodedText, decodedResult) {
            document.getElementById('codeInput').value = decodedText;
            document.getElementById('scanResult').innerHTML = 
                `<div class="alert alert-success">QR Code detectado: ${decodedText}</div>`;
            
            // Switch to validate tab and auto-validate
            const validateTab = new bootstrap.Tab(document.getElementById('validate-tab'));
            validateTab.show();
            
            // Auto-validate the scanned code
            setTimeout(() => {
                document.getElementById('validateForm').dispatchEvent(new Event('submit'));
            }, 500);
        }
        
        function onScanFailure(error) {
            // Ignore scanning failures - they happen frequently
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/validate', methods=['POST'])
def validate_qr_code():
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({"valid": False, "error": "Code is required"}), 400
    
    result = validator.validate_qr_code(code)
    return jsonify(result)

@app.route('/api/use', methods=['POST'])
def use_qr_code():
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({"success": False, "error": "Code is required"}), 400
    
    result = validator.use_qr_code(code)
    return jsonify(result)

@app.route('/api/generate', methods=['POST'])
def generate_qr_code():
    data = request.get_json()
    
    try:
        qr_type = QRType(data.get('qr_type'))
        employee_id = data.get('employee_id')
        duration_hours = data.get('duration_hours', 24)
        metadata = data.get('metadata', '')
        
        if not employee_id:
            return jsonify({"success": False, "error": "Employee ID is required"}), 400
        
        result = validator.generate_qr_code(qr_type, employee_id, duration_hours, metadata)
        return jsonify(result)
        
    except ValueError:
        return jsonify({"success": False, "error": "Invalid QR type"}), 400

@app.route('/api/employee/<employee_id>/qrcodes', methods=['GET'])
def get_employee_qrcodes(employee_id):
    codes = validator.get_qr_codes_by_employee(employee_id)
    return jsonify(codes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)