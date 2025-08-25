#!/usr/bin/env python3
"""
Setup verification script for QR Code Lightera Voluntario project.
This script validates that all required dependencies are installed and working.
"""

def test_core_dependencies():
    """Test core application dependencies"""
    print("🔍 Testing core application dependencies...")
    
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask: {e}")
        return False

    try:
        import qrcode
        print("✅ QRCode library: Available")
    except ImportError as e:
        print(f"❌ QRCode library: {e}")
        return False

    try:
        from PIL import Image
        print(f"✅ Pillow (PIL): {Image.__version__}")
    except ImportError as e:
        print(f"❌ Pillow (PIL): {e}")
        return False

    try:
        import sqlite3
        print(f"✅ SQLite3: {sqlite3.sqlite_version}")
    except ImportError as e:
        print(f"❌ SQLite3: {e}")
        return False

    return True

def test_data_analysis_dependencies():
    """Test data analysis and visualization dependencies"""
    print("\n🔍 Testing data analysis dependencies...")
    
    try:
        import pandas as pd
        print(f"✅ Pandas: {pd.__version__}")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False

    try:
        import plotly
        print(f"✅ Plotly: {plotly.__version__}")
    except ImportError as e:
        print(f"❌ Plotly: {e}")
        return False

    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False

    return True

def test_qr_functionality():
    """Test QR code generation functionality"""
    print("\n🔍 Testing QR code generation...")
    
    try:
        import qrcode
        from PIL import Image
        
        # Create a test QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('QR Code Lightera Voluntario - Test')
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        print("✅ QR Code generation: Successful")
        print(f"✅ Generated QR image size: {img.size}")
        return True
    except Exception as e:
        print(f"❌ QR Code generation failed: {e}")
        return False

def test_flask_functionality():
    """Test basic Flask functionality"""
    print("\n🔍 Testing Flask functionality...")
    
    try:
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return jsonify({"status": "OK", "message": "Flask is working"})
        
        # Test that app can be created
        print("✅ Flask app creation: Successful")
        
        # Test app context
        with app.app_context():
            print("✅ Flask app context: Working")
        
        return True
    except Exception as e:
        print(f"❌ Flask functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 QR Code Lightera Voluntario - Dependency Verification\n")
    print("=" * 60)
    
    tests = [
        test_core_dependencies,
        test_data_analysis_dependencies,
        test_qr_functionality,
        test_flask_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print(f"✅ Tests passed: {passed}")
    print(f"❌ Tests failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All dependencies are properly installed and working!")
        print("🚀 You're ready to start developing the QR Code application!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        print("💡 Try running: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit(main())