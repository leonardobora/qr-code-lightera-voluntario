import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from app import app, QRCodeValidator, QRStatus, QRType

class TestQRCodeValidation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.validator = QRCodeValidator(self.temp_db.name)
        self.app = app.test_client()
        self.app.testing = True
        
        # Patch the global validator in the app
        import app as app_module
        app_module.validator = self.validator

    def tearDown(self):
        """Clean up after tests"""
        os.unlink(self.temp_db.name)

    def test_generate_qr_code(self):
        """Test QR code generation"""
        result = self.validator.generate_qr_code(
            QRType.FESTA, 
            "EMP001", 
            24, 
            "Festa de fim de ano"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["qr_type"], "festa")
        self.assertIn("code", result)
        self.assertIn("qr_image", result)
        self.assertIn("expires_at", result)

    def test_validate_valid_qr_code(self):
        """Test validation of a valid QR code"""
        # Generate a QR code first
        gen_result = self.validator.generate_qr_code(
            QRType.CESTAS, 
            "EMP002", 
            48, 
            "Cestas básicas"
        )
        
        code = gen_result["code"]
        
        # Validate it
        result = self.validator.validate_qr_code(code)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["code"], code)
        self.assertEqual(result["qr_type"], "cestas")
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["employee_id"], "EMP002")
        self.assertTrue(result["is_usable"])

    def test_validate_invalid_qr_code(self):
        """Test validation of an invalid QR code"""
        result = self.validator.validate_qr_code("invalid-code-123")
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)

    def test_use_valid_qr_code(self):
        """Test using a valid QR code"""
        # Generate a QR code first
        gen_result = self.validator.generate_qr_code(
            QRType.BRINQUEDOS, 
            "EMP003", 
            12, 
            "Brinquedos"
        )
        
        code = gen_result["code"]
        
        # Use it
        result = self.validator.use_qr_code(code)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["code"], code)
        self.assertIn("used_at", result)
        
        # Validate it's now used
        validation = self.validator.validate_qr_code(code)
        self.assertEqual(validation["status"], "used")
        self.assertFalse(validation["is_usable"])

    def test_use_already_used_qr_code(self):
        """Test using an already used QR code"""
        # Generate and use a QR code
        gen_result = self.validator.generate_qr_code(
            QRType.MATERIAL_ESCOLAR, 
            "EMP004", 
            6, 
            "Material escolar"
        )
        
        code = gen_result["code"]
        self.validator.use_qr_code(code)
        
        # Try to use it again
        result = self.validator.use_qr_code(code)
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)

    def test_expired_qr_code(self):
        """Test QR code expiration logic"""
        # Generate a QR code with very short expiration
        gen_result = self.validator.generate_qr_code(
            QRType.FESTA, 
            "EMP005", 
            -1,  # Negative hours to create already expired code
            "Test expiration"
        )
        
        code = gen_result["code"]
        
        # Validate - should detect expiration
        result = self.validator.validate_qr_code(code)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "expired")
        self.assertFalse(result["is_usable"])

    def test_get_employee_qrcodes(self):
        """Test getting QR codes for an employee"""
        employee_id = "EMP006"
        
        # Generate multiple QR codes for the same employee
        self.validator.generate_qr_code(QRType.FESTA, employee_id, 24, "Festa 1")
        self.validator.generate_qr_code(QRType.CESTAS, employee_id, 48, "Cestas 1")
        
        # Get employee's QR codes
        codes = self.validator.get_qr_codes_by_employee(employee_id)
        
        self.assertEqual(len(codes), 2)
        # Check that both types are present
        qr_types = [code["qr_type"] for code in codes]
        self.assertIn("festa", qr_types)
        self.assertIn("cestas", qr_types)

    def test_api_generate_endpoint(self):
        """Test the /api/generate endpoint"""
        response = self.app.post('/api/generate', 
            data=json.dumps({
                'qr_type': 'festa',
                'employee_id': 'API_EMP001',
                'duration_hours': 24,
                'metadata': 'API Test'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['qr_type'], 'festa')

    def test_api_validate_endpoint(self):
        """Test the /api/validate endpoint"""
        # Generate a code first
        gen_response = self.app.post('/api/generate', 
            data=json.dumps({
                'qr_type': 'cestas',
                'employee_id': 'API_EMP002',
                'duration_hours': 24,
                'metadata': 'API Test'
            }),
            content_type='application/json'
        )
        
        gen_data = json.loads(gen_response.data)
        code = gen_data['code']
        
        # Validate it
        response = self.app.post('/api/validate', 
            data=json.dumps({'code': code}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['valid'])
        self.assertEqual(data['status'], 'pending')

    def test_api_use_endpoint(self):
        """Test the /api/use endpoint"""
        # Generate a code first
        gen_response = self.app.post('/api/generate', 
            data=json.dumps({
                'qr_type': 'brinquedos',
                'employee_id': 'API_EMP003',
                'duration_hours': 24,
                'metadata': 'API Test'
            }),
            content_type='application/json'
        )
        
        gen_data = json.loads(gen_response.data)
        code = gen_data['code']
        
        # Use it
        response = self.app.post('/api/use', 
            data=json.dumps({'code': code}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()