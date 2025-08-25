import qrcode
import os
from datetime import datetime
import uuid

def generate_festa_qr_code(employee_name, employee_id):
    """Generate a QR code specifically for Festa de Final de Ano"""
    # Create unique QR code data for the party
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    # QR code data includes employee info and festa identifier
    qr_data = f"FESTA2024:{employee_id}:{employee_name}:{timestamp}:{unique_id}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code image
    filename = f"festa_qr_{employee_id}_{timestamp}.png"
    filepath = os.path.join("static", "qr_codes", filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    img.save(filepath)
    
    return qr_data, filepath

def validate_festa_qr_code(qr_data):
    """Validate if QR code is for Festa de Final de Ano"""
    try:
        parts = qr_data.split(":")
        if len(parts) >= 2 and parts[0] == "FESTA2024":
            employee_id = parts[1]
            employee_name = parts[2] if len(parts) > 2 else "Unknown"
            return True, employee_id, employee_name
        return False, None, None
    except:
        return False, None, None

if __name__ == '__main__':
    # Test QR code generation
    qr_data, filepath = generate_festa_qr_code("João Silva", "EMP001")
    print(f"QR Code generated: {qr_data}")
    print(f"Image saved to: {filepath}")
    
    # Test validation
    is_valid, emp_id, emp_name = validate_festa_qr_code(qr_data)
    print(f"Validation: {is_valid}, Employee: {emp_name} ({emp_id})")