import unittest
import tempfile
import os
import json
from app import app, init_db, get_db_connection

class CestasNatalTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test database and Flask app"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        # Override the DATABASE constant in app module
        import app as app_module
        app_module.DATABASE = app.config['DATABASE']
        self.app = app.test_client()
        
        # Initialize database for testing
        with app.app_context():
            init_db()
    
    def tearDown(self):
        """Clean up test database"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_home_page(self):
        """Test home page loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Cestas de Natal', rv.data)
    
    def test_cestas_page(self):
        """Test cestas listing page"""
        rv = self.app.get('/cestas')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Cestas de Natal', rv.data)
    
    def test_nova_cesta_get(self):
        """Test new basket form page"""
        rv = self.app.get('/cestas/nova')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Nova Cesta de Natal', rv.data)
    
    def test_nova_cesta_post(self):
        """Test creating a new basket"""
        rv = self.app.post('/cestas/nova', data={
            'codigo_funcionario': 'EMP001',
            'nome_funcionario': 'João Silva',
            'departamento': 'TI'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'QR Code da Cesta', rv.data)
    
    def test_nova_cesta_missing_data(self):
        """Test creating basket with missing required data"""
        rv = self.app.post('/cestas/nova', data={
            'codigo_funcionario': '',
            'nome_funcionario': 'João Silva'
        })
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'obrigat', rv.data)
    
    def test_duplicate_employee_basket(self):
        """Test preventing duplicate baskets for same employee"""
        # Create first basket
        self.app.post('/cestas/nova', data={
            'codigo_funcionario': 'EMP001',
            'nome_funcionario': 'João Silva',
            'departamento': 'TI'
        })
        
        # Try to create second basket for same employee
        rv = self.app.post('/cestas/nova', data={
            'codigo_funcionario': 'EMP001',
            'nome_funcionario': 'João Silva',
            'departamento': 'TI'
        })
        self.assertIn(b'j\xc3\xa1 possui', rv.data)  # "já possui" in UTF-8
    
    def test_scanner_page(self):
        """Test QR scanner page"""
        rv = self.app.get('/scanner')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Scanner de QR Code', rv.data)
    
    def test_validar_qr_invalid(self):
        """Test QR validation with invalid code"""
        rv = self.app.post('/api/validar_qr', 
                          data=json.dumps({'qr_content': 'INVALID_QR_CODE'}),
                          content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertFalse(data['success'])
    
    def test_validar_qr_valid(self):
        """Test QR validation with valid code"""
        # First create a basket
        with app.app_context():
            conn = get_db_connection()
            cursor = conn.execute(
                'INSERT INTO cestas_natal (codigo_funcionario, nome_funcionario, departamento) VALUES (?, ?, ?)',
                ('EMP001', 'João Silva', 'TI')
            )
            cesta_id = cursor.lastrowid
            conn.commit()
            conn.close()
        
        # Test validation
        qr_content = f"CESTA_NATAL|{cesta_id}|EMP001|João Silva"
        rv = self.app.post('/api/validar_qr', 
                          data=json.dumps({'qr_content': qr_content}),
                          content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertTrue(data['success'])
        self.assertIn('retirada com sucesso', data['message'])

if __name__ == '__main__':
    unittest.main()