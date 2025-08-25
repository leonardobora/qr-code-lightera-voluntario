"""
Database initialization and utility functions for Lightera QR Code System

This script provides utilities to:
- Initialize the database with sample data
- Reset the database 
- Create initial admin user
- Generate sample events and QR codes for testing
"""

import os
import sys
from datetime import datetime, timedelta
from models import DatabaseManager, Funcionario, Evento, QRCode, EventType, QRCodeStatus


def init_sample_data(db_path: str = "lightera_qr.db"):
    """Inicializa o banco com dados de exemplo"""
    
    # Inicializar banco
    db_manager = DatabaseManager(db_path)
    funcionario_model = Funcionario(db_manager)
    evento_model = Evento(db_manager)
    qr_model = QRCode(db_manager)
    
    print("🗄️ Inicializando banco de dados SQLite...")
    
    # Criar funcionários de exemplo
    print("👥 Criando funcionários de exemplo...")
    
    funcionarios = [
        {
            "nome": "Maria Silva",
            "email": "maria.silva@lightera.org",
            "cargo": "Coordenadora",
            "telefone": "(11) 98765-4321"
        },
        {
            "nome": "João Santos",
            "email": "joao.santos@lightera.org", 
            "cargo": "Voluntário",
            "telefone": "(11) 91234-5678"
        },
        {
            "nome": "Ana Costa",
            "email": "ana.costa@lightera.org",
            "cargo": "Assistente",
            "telefone": "(11) 95555-1234"
        }
    ]
    
    funcionarios_ids = []
    for func_data in funcionarios:
        try:
            func_id = funcionario_model.criar(**func_data)
            funcionarios_ids.append(func_id)
            print(f"   ✅ Funcionário criado: {func_data['nome']} (ID: {func_id})")
        except Exception as e:
            print(f"   ❌ Erro ao criar funcionário {func_data['nome']}: {e}")
    
    if not funcionarios_ids:
        print("❌ Nenhum funcionário foi criado. Abortando...")
        return False
    
    # Criar eventos de exemplo
    print("\n🎉 Criando eventos de exemplo...")
    
    data_futuro = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    data_passado = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    eventos = [
        {
            "nome": "Festa de Natal 2024",
            "tipo": EventType.FESTA,
            "responsavel_id": funcionarios_ids[0],
            "descricao": "Festa natalina para as famílias atendidas",
            "data_evento": data_futuro,
            "local": "Centro Comunitário Lightera"
        },
        {
            "nome": "Distribuição de Cestas Básicas - Janeiro",
            "tipo": EventType.CESTAS,
            "responsavel_id": funcionarios_ids[1],
            "descricao": "Distribuição mensal de cestas básicas",
            "data_evento": data_futuro,
            "local": "Sede Lightera"
        },
        {
            "nome": "Doação de Brinquedos - Dia das Crianças",
            "tipo": EventType.BRINQUEDOS,
            "responsavel_id": funcionarios_ids[2],
            "descricao": "Entrega de brinquedos para crianças",
            "data_evento": data_passado,
            "local": "Praça Central"
        },
        {
            "nome": "Kit Escolar 2024",
            "tipo": EventType.MATERIAL_ESCOLAR,
            "responsavel_id": funcionarios_ids[0],
            "descricao": "Distribuição de material escolar",
            "data_evento": data_futuro,
            "local": "Escola Municipal"
        }
    ]
    
    eventos_ids = []
    for evento_data in eventos:
        try:
            evento_id = evento_model.criar(**evento_data)
            eventos_ids.append(evento_id)
            print(f"   ✅ Evento criado: {evento_data['nome']} (ID: {evento_id})")
        except Exception as e:
            print(f"   ❌ Erro ao criar evento {evento_data['nome']}: {e}")
    
    # Criar QR codes de exemplo
    print("\n📱 Criando QR codes de exemplo...")
    
    if eventos_ids:
        qr_codes_exemplos = [
            {
                "codigo": "FESTA_NATAL_001",
                "evento_id": eventos_ids[0] if len(eventos_ids) > 0 else None,
                "funcionario_criador_id": funcionarios_ids[0],
                "destinatario_nome": "Família Santos",
                "destinatario_info": "4 pessoas - Endereço: Rua A, 123",
                "quantidade": 4,
                "observacoes": "Prioridade: Alta - Família com crianças pequenas"
            },
            {
                "codigo": "CESTA_JAN_001",
                "evento_id": eventos_ids[1] if len(eventos_ids) > 1 else None,
                "funcionario_criador_id": funcionarios_ids[1],
                "destinatario_nome": "Maria da Silva",
                "destinatario_info": "2 pessoas - Telefone: (11) 99999-1111",
                "quantidade": 1,
                "observacoes": "Possui restrições alimentares"
            },
            {
                "codigo": "BRINQUEDO_001",
                "evento_id": eventos_ids[2] if len(eventos_ids) > 2 else None,
                "funcionario_criador_id": funcionarios_ids[2],
                "destinatario_nome": "Pedro Oliveira",
                "destinatario_info": "Idade: 8 anos - Preferência: Bola",
                "quantidade": 1,
                "observacoes": "Já retirado"
            },
            {
                "codigo": "ESCOLAR_2024_001",
                "evento_id": eventos_ids[3] if len(eventos_ids) > 3 else None,
                "funcionario_criador_id": funcionarios_ids[0],
                "destinatario_nome": "Ana Santos",
                "destinatario_info": "Série: 3º ano - Escola: Municipal Santos",
                "quantidade": 1,
                "data_expiracao": (datetime.now() + timedelta(days=60)).isoformat(),
                "observacoes": "Material específico para 3º ano"
            }
        ]
        
        for qr_data in qr_codes_exemplos:
            if qr_data["evento_id"] is not None:
                try:
                    qr_id = qr_model.criar(**qr_data)
                    print(f"   ✅ QR Code criado: {qr_data['codigo']} (ID: {qr_id})")
                    
                    # Marcar um dos QR codes como usado para demonstração
                    if qr_data["codigo"] == "BRINQUEDO_001":
                        qr_model.usar_codigo(qr_data["codigo"])
                        print(f"      📱 QR Code {qr_data['codigo']} marcado como usado")
                        
                except Exception as e:
                    print(f"   ❌ Erro ao criar QR code {qr_data['codigo']}: {e}")
    
    print("\n✅ Inicialização do banco de dados concluída!")
    print(f"   📁 Arquivo do banco: {db_path}")
    print(f"   👥 Funcionários criados: {len(funcionarios_ids)}")
    print(f"   🎉 Eventos criados: {len(eventos_ids)}")
    print("\n🚀 Sistema pronto para uso!")
    
    return True


def reset_database(db_path: str = "lightera_qr.db"):
    """Remove o banco de dados existente"""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Banco de dados {db_path} removido.")
    else:
        print(f"ℹ️ Banco de dados {db_path} não existe.")


def show_database_stats(db_path: str = "lightera_qr.db"):
    """Mostra estatísticas do banco de dados"""
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados {db_path} não encontrado.")
        return
    
    db_manager = DatabaseManager(db_path)
    funcionario_model = Funcionario(db_manager)
    evento_model = Evento(db_manager)
    
    print(f"📊 Estatísticas do banco {db_path}:")
    
    # Estatísticas de funcionários
    funcionarios = funcionario_model.listar_ativos()
    print(f"   👥 Funcionários ativos: {len(funcionarios)}")
    
    # Estatísticas de eventos
    eventos = evento_model.listar_ativos()
    print(f"   🎉 Eventos ativos: {len(eventos)}")
    
    # Estatísticas por tipo de evento
    for tipo in EventType:
        eventos_tipo = evento_model.listar_por_tipo(tipo)
        print(f"      - {tipo.value.replace('_', ' ').title()}: {len(eventos_tipo)}")
    
    # Estatísticas de QR codes
    with db_manager.get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) as total FROM qr_codes")
        total_qr = cursor.fetchone()["total"]
        print(f"   📱 QR Codes total: {total_qr}")
        
        cursor = conn.execute("""
            SELECT status, COUNT(*) as count 
            FROM qr_codes 
            GROUP BY status
        """)
        for row in cursor.fetchall():
            print(f"      - {row['status'].title()}: {row['count']}")


def main():
    """Função principal para execução via linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Utilitários do banco de dados Lightera QR")
    parser.add_argument("--db", default="lightera_qr.db", help="Caminho do banco de dados")
    parser.add_argument("--reset", action="store_true", help="Reinicia o banco de dados")
    parser.add_argument("--init", action="store_true", help="Inicializa com dados de exemplo")
    parser.add_argument("--stats", action="store_true", help="Mostra estatísticas do banco")
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database(args.db)
    
    if args.init:
        init_sample_data(args.db)
    
    if args.stats:
        show_database_stats(args.db)
    
    if not any([args.reset, args.init, args.stats]):
        print("🗄️ Lightera QR Code Database Utilities")
        print("\nOpções disponíveis:")
        print("  --reset    Reinicia o banco de dados")
        print("  --init     Inicializa com dados de exemplo")
        print("  --stats    Mostra estatísticas do banco")
        print("  --db PATH  Especifica o caminho do banco (padrão: lightera_qr.db)")
        print("\nExemplos:")
        print("  python db_utils.py --init")
        print("  python db_utils.py --reset --init")
        print("  python db_utils.py --stats")


if __name__ == "__main__":
    main()