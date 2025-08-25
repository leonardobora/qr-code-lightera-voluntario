#!/usr/bin/env python3
"""
Demo script for QR Code System - Festa de Final de Ano
Demonstrates core functionality without requiring external libraries
"""

import os
import sys
from datetime import datetime
import uuid

# Add current directory to path
sys.path.insert(0, os.getcwd())

from database import init_database, add_qr_code, get_qr_code, mark_qr_used, get_all_qr_codes

def create_festa_qr_data(employee_name, employee_id):
    """Create QR code data for festa (without generating actual image)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    # QR code data includes employee info and festa identifier
    qr_data = f"FESTA2024:{employee_id}:{employee_name}:{timestamp}:{unique_id}"
    return qr_data

def validate_festa_qr_data(qr_data):
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

def demo():
    """Run demo of the QR code system"""
    print("🎄 DEMO: Sistema QR Codes - Festa de Final de Ano")
    print("=" * 60)
    
    # Initialize database
    print("\n1️⃣ Inicializando banco de dados...")
    init_database()
    print("✅ Banco de dados inicializado")
    
    # Sample employees
    employees = [
        ("João Silva", "EMP001"),
        ("Maria Santos", "EMP002"), 
        ("Pedro Oliveira", "EMP003"),
        ("Ana Costa", "EMP004")
    ]
    
    print("\n2️⃣ Gerando QR Codes para funcionários...")
    for name, emp_id in employees:
        # Create QR data (simulating image generation)
        qr_data = create_festa_qr_data(name, emp_id)
        image_path = f"static/qr_codes/festa_qr_{emp_id}.png"  # Would be actual path
        
        # Add to database
        result = add_qr_code(name, emp_id, qr_data, image_path)
        
        if result:
            print(f"✅ QR Code gerado para {name} ({emp_id})")
            print(f"   Dados: {qr_data}")
        else:
            print(f"❌ Falha ao gerar QR Code para {name}")
    
    print("\n3️⃣ Listando QR Codes gerados...")
    all_qr_codes = get_all_qr_codes()
    print(f"📊 Total de QR Codes: {len(all_qr_codes)}")
    
    for qr in all_qr_codes:
        status = "🔴 USADO" if qr['is_used'] else "🟢 DISPONÍVEL"
        print(f"   {qr['employee_name']} ({qr['employee_id']}) - {status}")
    
    print("\n4️⃣ Simulando validação de entrada na festa...")
    
    # Simulate validation of first employee
    test_employee = employees[0]
    test_qr = get_qr_code(test_employee[1])
    
    if test_qr:
        print(f"\n🔍 Validando QR Code de {test_qr['employee_name']}...")
        
        # Validate format
        is_valid, emp_id, emp_name = validate_festa_qr_data(test_qr['qr_code_data'])
        
        if is_valid:
            print(f"✅ QR Code válido para {emp_name} ({emp_id})")
            
            if not test_qr['is_used']:
                # Mark as used
                mark_qr_used(emp_id)
                print(f"🎉 ENTRADA LIBERADA! {emp_name} pode entrar na festa.")
            else:
                print(f"⚠️ QR Code já foi usado por {emp_name}")
        else:
            print("❌ QR Code inválido!")
    
    print("\n5️⃣ Tentativa de uso duplo...")
    # Try to use the same QR code again
    if test_qr:
        updated_qr = get_qr_code(test_employee[1])
        if updated_qr['is_used']:
            print(f"🚫 Tentativa de reuso detectada para {updated_qr['employee_name']}")
            print(f"   QR Code já foi usado em {updated_qr['used_at']}")
        
    print("\n6️⃣ Status final dos QR Codes...")
    final_qr_codes = get_all_qr_codes()
    used_count = sum(1 for qr in final_qr_codes if qr['is_used'])
    available_count = len(final_qr_codes) - used_count
    
    print(f"📊 Relatório da Festa:")
    print(f"   Total de QR Codes: {len(final_qr_codes)}")
    print(f"   🟢 Disponíveis: {available_count}")
    print(f"   🔴 Usados: {used_count}")
    print(f"   📈 Taxa de uso: {(used_count/len(final_qr_codes)*100):.1f}%")
    
    print("\n" + "=" * 60)
    print("🎉 Demo concluída! O sistema está funcionando perfeitamente.")
    print("\n💡 Para usar a interface web:")
    print("   1. Instale as dependências: pip install -r requirements.txt")
    print("   2. Execute: python3 app.py")
    print("   3. Acesse: http://localhost:5000")

def cleanup():
    """Clean up demo data"""
    if os.path.exists('festa_qrcodes.db'):
        os.remove('festa_qrcodes.db')
        print("\n🧹 Dados de demo removidos")

if __name__ == '__main__':
    try:
        demo()
        input("\n⏸️ Pressione Enter para limpar os dados de demo...")
        cleanup()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrompida")
        cleanup()
    except Exception as e:
        print(f"\n❌ Erro durante demo: {e}")
        cleanup()
        sys.exit(1)