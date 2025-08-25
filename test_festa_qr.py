#!/usr/bin/env python3
"""
Test script for QR Code generation functionality
Tests the core features without requiring Flask web server
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_database():
    """Test database functionality"""
    print("🧪 Testing database functionality...")
    
    from database import init_database, add_qr_code, get_qr_code, get_all_qr_codes
    
    # Initialize database
    init_database()
    print("✅ Database initialized")
    
    # Test adding QR code data
    result = add_qr_code(
        employee_name="João Silva", 
        employee_id="TEST001", 
        qr_code_data="FESTA2024:TEST001:João Silva:20241225_100000:abc123", 
        qr_image_path="static/qr_codes/test_qr.png"
    )
    
    if result:
        print("✅ QR code added to database")
        
        # Test retrieval
        qr_code = get_qr_code("TEST001")
        if qr_code:
            print(f"✅ QR code retrieved: {qr_code['employee_name']}")
        else:
            print("❌ QR code not found")
    else:
        print("❌ Failed to add QR code")
    
    return result is not None

def test_qr_generation():
    """Test QR code generation (without actual image creation if qrcode not available)"""
    print("\n🧪 Testing QR code generation...")
    
    try:
        from qr_generator import generate_festa_qr_code, validate_festa_qr_code
        
        # This will fail if qrcode library is not installed, but we can still test the logic
        try:
            qr_data, filepath = generate_festa_qr_code("Maria Santos", "TEST002")
            print(f"✅ QR code generated: {qr_data}")
            print(f"✅ File path: {filepath}")
            
            # Test validation
            is_valid, emp_id, emp_name = validate_festa_qr_code(qr_data)
            if is_valid and emp_id == "TEST002" and emp_name == "Maria Santos":
                print("✅ QR code validation works")
                return True
            else:
                print("❌ QR code validation failed")
                return False
                
        except ImportError as e:
            print(f"⚠️ QR code library not available: {e}")
            print("📝 Testing validation logic only...")
            
            # Test validation with mock data
            test_data = "FESTA2024:TEST002:Maria Santos:20241225_100000:xyz789"
            is_valid, emp_id, emp_name = validate_festa_qr_code(test_data)
            
            if is_valid and emp_id == "TEST002" and emp_name == "Maria Santos":
                print("✅ QR code validation logic works")
                return True
            else:
                print("❌ QR code validation logic failed")
                return False
                
    except Exception as e:
        print(f"❌ Error in QR generation test: {e}")
        return False

def test_festa_qr_format():
    """Test the specific format for Festa de Final de Ano QR codes"""
    print("\n🧪 Testing Festa QR code format...")
    
    from qr_generator import validate_festa_qr_code
    
    # Test valid format
    valid_qr = "FESTA2024:EMP001:João Silva:20241225_120000:abcd1234"
    is_valid, emp_id, emp_name = validate_festa_qr_code(valid_qr)
    
    if is_valid and emp_id == "EMP001" and emp_name == "João Silva":
        print("✅ Valid festa QR format recognized")
    else:
        print("❌ Valid festa QR format not recognized")
        return False
    
    # Test invalid format
    invalid_qr = "INVALID:EMP001:João Silva:20241225_120000:abcd1234"
    is_valid, _, _ = validate_festa_qr_code(invalid_qr)
    
    if not is_valid:
        print("✅ Invalid QR format correctly rejected")
    else:
        print("❌ Invalid QR format incorrectly accepted")
        return False
    
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    # Remove test database if it exists
    if os.path.exists('festa_qrcodes.db'):
        os.remove('festa_qrcodes.db')
        print("✅ Test database removed")
    
    # Remove test QR code images
    test_dir = 'static/qr_codes'
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            if file.startswith('test_') or file.startswith('festa_qr_TEST'):
                os.remove(os.path.join(test_dir, file))
                print(f"✅ Removed test file: {file}")

def main():
    """Run all tests"""
    print("🎄 Testing QR Code System for Festa de Final de Ano")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    tests = [
        test_database,
        test_qr_generation, 
        test_festa_qr_format
    ]
    
    for test in tests:
        try:
            result = test()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            all_passed = False
    
    # Results
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Sistema está funcionando.")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    # Cleanup
    cleanup_test_data()
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)