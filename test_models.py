"""
Testes básicos para validar os modelos SQLite
Este script testa as funcionalidades principais dos modelos de dados.
"""

import os
import tempfile
from models import DatabaseManager, Funcionario, Evento, QRCode, EventType, QRCodeStatus


def test_database_creation():
    """Testa a criação do banco de dados"""
    print("🧪 Testando criação do banco de dados...")
    
    # Usar arquivo temporário para teste
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        db_manager = DatabaseManager(db_path)
        
        # Verificar se o arquivo foi criado
        assert os.path.exists(db_path), "Arquivo do banco não foi criado"
        
        # Testar conexão
        with db_manager.get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['funcionarios', 'eventos', 'qr_codes']
            for table in expected_tables:
                assert table in tables, f"Tabela {table} não foi criada"
        
        print("   ✅ Banco de dados criado com sucesso")
        return db_manager
        
    except Exception as e:
        print(f"   ❌ Erro na criação do banco: {e}")
        raise
    finally:
        # Limpar arquivo temporário
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_funcionario_operations():
    """Testa operações CRUD de funcionários"""
    print("🧪 Testando operações de funcionários...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        db_manager = DatabaseManager(db_path)
        funcionario_model = Funcionario(db_manager)
        
        # Teste de criação
        func_id = funcionario_model.criar(
            nome="Test User",
            email="test@example.com",
            cargo="Teste",
            telefone="11999999999"
        )
        assert func_id > 0, "ID do funcionário deve ser positivo"
        print("   ✅ Funcionário criado")
        
        # Teste de busca por ID
        funcionario = funcionario_model.buscar_por_id(func_id)
        assert funcionario is not None, "Funcionário deve ser encontrado"
        assert funcionario['nome'] == "Test User", "Nome deve coincidir"
        assert funcionario['email'] == "test@example.com", "Email deve coincidir"
        print("   ✅ Busca por ID funcionando")
        
        # Teste de busca por email
        funcionario = funcionario_model.buscar_por_email("test@example.com")
        assert funcionario is not None, "Funcionário deve ser encontrado por email"
        assert funcionario['id'] == func_id, "ID deve coincidir"
        print("   ✅ Busca por email funcionando")
        
        # Teste de atualização
        sucesso = funcionario_model.atualizar(func_id, nome="Test User Updated")
        assert sucesso, "Atualização deve ter sucesso"
        
        funcionario_atualizado = funcionario_model.buscar_por_id(func_id)
        assert funcionario_atualizado['nome'] == "Test User Updated", "Nome deve estar atualizado"
        print("   ✅ Atualização funcionando")
        
        # Teste de listagem
        funcionarios = funcionario_model.listar_ativos()
        assert len(funcionarios) == 1, "Deve haver 1 funcionário ativo"
        print("   ✅ Listagem funcionando")
        
        # Teste de desativação
        sucesso = funcionario_model.desativar(func_id)
        assert sucesso, "Desativação deve ter sucesso"
        
        funcionarios_ativos = funcionario_model.listar_ativos()
        assert len(funcionarios_ativos) == 0, "Não deve haver funcionários ativos"
        print("   ✅ Desativação funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro nos testes de funcionário: {e}")
        raise
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_evento_operations():
    """Testa operações CRUD de eventos"""
    print("🧪 Testando operações de eventos...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        db_manager = DatabaseManager(db_path)
        funcionario_model = Funcionario(db_manager)
        evento_model = Evento(db_manager)
        
        # Criar funcionário primeiro
        func_id = funcionario_model.criar("Test User", "test@example.com")
        
        # Teste de criação de evento
        evento_id = evento_model.criar(
            nome="Evento Teste",
            tipo=EventType.FESTA,
            responsavel_id=func_id,
            descricao="Evento para teste",
            local="Local Teste"
        )
        assert evento_id > 0, "ID do evento deve ser positivo"
        print("   ✅ Evento criado")
        
        # Teste de busca por ID
        evento = evento_model.buscar_por_id(evento_id)
        assert evento is not None, "Evento deve ser encontrado"
        assert evento['nome'] == "Evento Teste", "Nome deve coincidir"
        assert evento['tipo'] == EventType.FESTA.value, "Tipo deve coincidir"
        print("   ✅ Busca por ID funcionando")
        
        # Teste de listagem por tipo
        eventos_festa = evento_model.listar_por_tipo(EventType.FESTA)
        assert len(eventos_festa) == 1, "Deve haver 1 evento do tipo festa"
        print("   ✅ Listagem por tipo funcionando")
        
        # Teste de atualização
        sucesso = evento_model.atualizar(evento_id, nome="Evento Teste Atualizado")
        assert sucesso, "Atualização deve ter sucesso"
        
        evento_atualizado = evento_model.buscar_por_id(evento_id)
        assert evento_atualizado['nome'] == "Evento Teste Atualizado", "Nome deve estar atualizado"
        print("   ✅ Atualização funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro nos testes de evento: {e}")
        raise
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_qrcode_operations():
    """Testa operações CRUD de QR codes"""
    print("🧪 Testando operações de QR codes...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        db_manager = DatabaseManager(db_path)
        funcionario_model = Funcionario(db_manager)
        evento_model = Evento(db_manager)
        qr_model = QRCode(db_manager)
        
        # Criar funcionário e evento primeiro
        func_id = funcionario_model.criar("Test User", "test@example.com")
        evento_id = evento_model.criar("Evento Teste", EventType.FESTA, func_id)
        
        # Teste de criação de QR code
        qr_id = qr_model.criar(
            codigo="TEST_QR_001",
            evento_id=evento_id,
            funcionario_criador_id=func_id,
            destinatario_nome="Test Recipient",
            quantidade=2
        )
        assert qr_id > 0, "ID do QR code deve ser positivo"
        print("   ✅ QR Code criado")
        
        # Teste de busca por código
        qr_data = qr_model.buscar_por_codigo("TEST_QR_001")
        assert qr_data is not None, "QR code deve ser encontrado"
        assert qr_data['codigo'] == "TEST_QR_001", "Código deve coincidir"
        assert qr_data['destinatario_nome'] == "Test Recipient", "Destinatário deve coincidir"
        print("   ✅ Busca por código funcionando")
        
        # Teste de validação
        valido, mensagem = qr_model.validar_codigo("TEST_QR_001")
        assert valido, f"Código deve ser válido: {mensagem}"
        print("   ✅ Validação funcionando")
        
        # Teste de uso do código
        sucesso = qr_model.usar_codigo("TEST_QR_001")
        assert sucesso, "Uso do código deve ter sucesso"
        
        # Verificar se código foi marcado como usado
        qr_usado = qr_model.buscar_por_codigo("TEST_QR_001")
        assert qr_usado['status'] == QRCodeStatus.USADO.value, "Status deve ser 'usado'"
        print("   ✅ Uso do código funcionando")
        
        # Teste de validação de código usado
        valido, mensagem = qr_model.validar_codigo("TEST_QR_001")
        assert not valido, "Código usado não deve ser válido"
        assert "já foi utilizado" in mensagem, "Mensagem deve indicar que foi usado"
        print("   ✅ Validação de código usado funcionando")
        
        # Teste de estatísticas
        stats = qr_model.estatisticas_por_evento(evento_id)
        assert stats['usado'] == 1, "Deve haver 1 código usado"
        assert stats['total'] == 1, "Total deve ser 1"
        print("   ✅ Estatísticas funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro nos testes de QR code: {e}")
        raise
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Iniciando testes dos modelos SQLite...\n")
    
    try:
        test_database_creation()
        test_funcionario_operations()
        test_evento_operations()
        test_qrcode_operations()
        
        print("\n✅ Todos os testes passaram com sucesso!")
        print("🎉 Os modelos SQLite estão funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Falha nos testes: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)