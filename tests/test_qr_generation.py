import unittest
import sqlite3
import json
import os
import app as app_module

class QRCodeTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test database and Flask app."""
        self.app = app_module.app.test_client()
        self.app.testing = True
        
        # Use a test database
        self.test_db = 'test_qr_codes.db'
        app_module.DATABASE = self.test_db
        
        # Initialize test database
        app_module.init_db()
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sistema de QR Codes - Lightera', response.data)
    
    def test_generate_qr_code_festa(self):
        """Test QR code generation for festa type."""
        response = self.app.post('/generate',
                                data=json.dumps({
                                    'type': 'festa',
                                    'employee_name': 'Test User'
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('qr_id', data)
        self.assertIn('image', data)
        self.assertIn('content', data)
        self.assertIn('festa', data['content'])
        self.assertIn('Test User', data['content'])
    
    def test_generate_qr_code_cestas(self):
        """Test QR code generation for cestas type."""
        response = self.app.post('/generate',
                                data=json.dumps({
                                    'type': 'cestas',
                                    'employee_name': 'Maria Santos'
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('cestas', data['content'])
        self.assertIn('Maria Santos', data['content'])
    
    def test_generate_qr_code_without_employee(self):
        """Test QR code generation without employee name."""
        response = self.app.post('/generate',
                                data=json.dumps({
                                    'type': 'material_escolar',
                                    'employee_name': ''
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('material_escolar', data['content'])
    
    def test_list_qr_codes(self):
        """Test the QR codes listing page."""
        # First generate a QR code
        self.app.post('/generate',
                     data=json.dumps({
                         'type': 'brinquedos',
                         'employee_name': 'Test User'
                     }),
                     content_type='application/json')
        
        # Then check the list page
        response = self.app.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'QR Codes Gerados', response.data)
        self.assertIn(b'brinquedos', response.data)
    
    def test_database_storage(self):
        """Test that QR codes are properly stored in database."""
        # Generate a QR code
        self.app.post('/generate',
                     data=json.dumps({
                         'type': 'festa',
                         'employee_name': 'Database Test'
                     }),
                     content_type='application/json')
        
        # Check database
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM qr_codes WHERE employee_name = 'Database Test'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'festa')  # type column
        self.assertEqual(result[3], 'Database Test')  # employee_name column

if __name__ == '__main__':
    unittest.main()