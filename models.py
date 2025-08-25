"""
SQLite Database Models for Lightera QR Code Volunteer System

This module defines the database schema and models for:
- Funcionários (Employees)
- Eventos (Events) 
- QR Codes

The system supports QR code generation for different event types:
- Festa (Party)
- Cestas (Baskets)
- Brinquedos (Toys)
- Material Escolar (School Materials)
"""

import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class EventType(Enum):
    """Tipos de eventos suportados pelo sistema"""
    FESTA = "festa"
    CESTAS = "cestas" 
    BRINQUEDOS = "brinquedos"
    MATERIAL_ESCOLAR = "material_escolar"


class QRCodeStatus(Enum):
    """Status do QR Code"""
    ATIVO = "ativo"
    USADO = "usado"
    EXPIRADO = "expirado"
    INATIVO = "inativo"


class DatabaseManager:
    """Gerenciador de conexão e operações do banco de dados SQLite"""
    
    def __init__(self, db_path: str = "lightera_qr.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        return conn
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        with self.get_connection() as conn:
            # Criar tabela de funcionários
            conn.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    cargo TEXT,
                    telefone TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Criar tabela de eventos
            conn.execute("""
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    tipo TEXT NOT NULL CHECK (tipo IN ('festa', 'cestas', 'brinquedos', 'material_escolar')),
                    data_evento DATE,
                    local TEXT,
                    responsavel_id INTEGER,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (responsavel_id) REFERENCES funcionarios (id)
                )
            """)
            
            # Criar tabela de QR codes
            conn.execute("""
                CREATE TABLE IF NOT EXISTS qr_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    hash_codigo TEXT UNIQUE NOT NULL,
                    evento_id INTEGER NOT NULL,
                    funcionario_criador_id INTEGER NOT NULL,
                    destinatario_nome TEXT,
                    destinatario_info TEXT,
                    quantidade INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'usado', 'expirado', 'inativo')),
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_uso TIMESTAMP,
                    data_expiracao TIMESTAMP,
                    observacoes TEXT,
                    FOREIGN KEY (evento_id) REFERENCES eventos (id),
                    FOREIGN KEY (funcionario_criador_id) REFERENCES funcionarios (id)
                )
            """)
            
            # Criar índices para melhor performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_funcionarios_email ON funcionarios (email)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_funcionarios_ativo ON funcionarios (ativo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_eventos_tipo ON eventos (tipo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_eventos_data ON eventos (data_evento)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_qrcodes_codigo ON qr_codes (codigo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_qrcodes_hash ON qr_codes (hash_codigo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_qrcodes_status ON qr_codes (status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_qrcodes_evento ON qr_codes (evento_id)")
            
            conn.commit()


class Funcionario:
    """Modelo para Funcionários/Voluntários"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def criar(self, nome: str, email: str, cargo: str = None, telefone: str = None) -> int:
        """Cria um novo funcionário"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO funcionarios (nome, email, cargo, telefone)
                VALUES (?, ?, ?, ?)
            """, (nome, email, cargo, telefone))
            conn.commit()
            return cursor.lastrowid
    
    def buscar_por_id(self, funcionario_id: int) -> Optional[Dict[str, Any]]:
        """Busca funcionário por ID"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM funcionarios WHERE id = ? AND ativo = 1
            """, (funcionario_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def buscar_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca funcionário por email"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM funcionarios WHERE email = ? AND ativo = 1
            """, (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def listar_ativos(self) -> List[Dict[str, Any]]:
        """Lista todos os funcionários ativos"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM funcionarios WHERE ativo = 1 
                ORDER BY nome
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def atualizar(self, funcionario_id: int, **kwargs) -> bool:
        """Atualiza dados do funcionário"""
        campos_permitidos = ['nome', 'email', 'cargo', 'telefone']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and valor is not None:
                campos.append(f"{campo} = ?")
                valores.append(valor)
        
        if not campos:
            return False
        
        campos.append("data_atualizacao = CURRENT_TIMESTAMP")
        valores.append(funcionario_id)
        
        with self.db.get_connection() as conn:
            conn.execute(f"""
                UPDATE funcionarios SET {', '.join(campos)}
                WHERE id = ?
            """, valores)
            conn.commit()
            return conn.total_changes > 0
    
    def desativar(self, funcionario_id: int) -> bool:
        """Desativa um funcionário (soft delete)"""
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE funcionarios SET ativo = 0, data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (funcionario_id,))
            conn.commit()
            return conn.total_changes > 0


class Evento:
    """Modelo para Eventos"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def criar(self, nome: str, tipo: EventType, responsavel_id: int,
              descricao: str = None, data_evento: str = None, local: str = None) -> int:
        """Cria um novo evento"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO eventos (nome, descricao, tipo, data_evento, local, responsavel_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, descricao, tipo.value, data_evento, local, responsavel_id))
            conn.commit()
            return cursor.lastrowid
    
    def buscar_por_id(self, evento_id: int) -> Optional[Dict[str, Any]]:
        """Busca evento por ID"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, f.nome as responsavel_nome 
                FROM eventos e
                LEFT JOIN funcionarios f ON e.responsavel_id = f.id
                WHERE e.id = ? AND e.ativo = 1
            """, (evento_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def listar_por_tipo(self, tipo: EventType) -> List[Dict[str, Any]]:
        """Lista eventos por tipo"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, f.nome as responsavel_nome 
                FROM eventos e
                LEFT JOIN funcionarios f ON e.responsavel_id = f.id
                WHERE e.tipo = ? AND e.ativo = 1
                ORDER BY e.data_evento DESC, e.nome
            """, (tipo.value,))
            return [dict(row) for row in cursor.fetchall()]
    
    def listar_ativos(self) -> List[Dict[str, Any]]:
        """Lista todos os eventos ativos"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, f.nome as responsavel_nome 
                FROM eventos e
                LEFT JOIN funcionarios f ON e.responsavel_id = f.id
                WHERE e.ativo = 1
                ORDER BY e.data_evento DESC, e.nome
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def atualizar(self, evento_id: int, **kwargs) -> bool:
        """Atualiza dados do evento"""
        campos_permitidos = ['nome', 'descricao', 'tipo', 'data_evento', 'local', 'responsavel_id']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and valor is not None:
                if campo == 'tipo' and isinstance(valor, EventType):
                    valor = valor.value
                campos.append(f"{campo} = ?")
                valores.append(valor)
        
        if not campos:
            return False
        
        campos.append("data_atualizacao = CURRENT_TIMESTAMP")
        valores.append(evento_id)
        
        with self.db.get_connection() as conn:
            conn.execute(f"""
                UPDATE eventos SET {', '.join(campos)}
                WHERE id = ?
            """, valores)
            conn.commit()
            return conn.total_changes > 0
    
    def desativar(self, evento_id: int) -> bool:
        """Desativa um evento (soft delete)"""
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE eventos SET ativo = 0, data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (evento_id,))
            conn.commit()
            return conn.total_changes > 0


class QRCode:
    """Modelo para QR Codes"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def _gerar_hash(self, codigo: str) -> str:
        """Gera hash SHA256 do código para validação"""
        return hashlib.sha256(codigo.encode()).hexdigest()
    
    def criar(self, codigo: str, evento_id: int, funcionario_criador_id: int,
              destinatario_nome: str = None, destinatario_info: str = None,
              quantidade: int = 1, data_expiracao: str = None,
              observacoes: str = None) -> int:
        """Cria um novo QR code"""
        hash_codigo = self._gerar_hash(codigo)
        
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO qr_codes 
                (codigo, hash_codigo, evento_id, funcionario_criador_id, 
                 destinatario_nome, destinatario_info, quantidade, 
                 data_expiracao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo, hash_codigo, evento_id, funcionario_criador_id,
                  destinatario_nome, destinatario_info, quantidade,
                  data_expiracao, observacoes))
            conn.commit()
            return cursor.lastrowid
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Busca QR code por código"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT qr.*, e.nome as evento_nome, e.tipo as evento_tipo,
                       f.nome as criador_nome
                FROM qr_codes qr
                JOIN eventos e ON qr.evento_id = e.id
                JOIN funcionarios f ON qr.funcionario_criador_id = f.id
                WHERE qr.codigo = ?
            """, (codigo,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def validar_codigo(self, codigo: str) -> tuple[bool, str]:
        """Valida se o código existe e está ativo"""
        qr_data = self.buscar_por_codigo(codigo)
        
        if not qr_data:
            return False, "Código QR não encontrado"
        
        if qr_data['status'] == QRCodeStatus.USADO.value:
            return False, "Código QR já foi utilizado"
        
        if qr_data['status'] == QRCodeStatus.EXPIRADO.value:
            return False, "Código QR expirado"
        
        if qr_data['status'] == QRCodeStatus.INATIVO.value:
            return False, "Código QR inativo"
        
        # Verificar expiração por data
        if qr_data['data_expiracao']:
            try:
                data_exp = datetime.fromisoformat(qr_data['data_expiracao'])
                if datetime.now() > data_exp:
                    self.marcar_expirado(qr_data['id'])
                    return False, "Código QR expirado"
            except ValueError:
                pass
        
        return True, "Código QR válido"
    
    def usar_codigo(self, codigo: str) -> bool:
        """Marca o código como usado"""
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE qr_codes 
                SET status = 'usado', data_uso = CURRENT_TIMESTAMP
                WHERE codigo = ? AND status = 'ativo'
            """, (codigo,))
            conn.commit()
            return conn.total_changes > 0
    
    def marcar_expirado(self, qr_id: int) -> bool:
        """Marca o código como expirado"""
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE qr_codes SET status = 'expirado'
                WHERE id = ?
            """, (qr_id,))
            conn.commit()
            return conn.total_changes > 0
    
    def listar_por_evento(self, evento_id: int) -> List[Dict[str, Any]]:
        """Lista QR codes de um evento"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT qr.*, f.nome as criador_nome
                FROM qr_codes qr
                JOIN funcionarios f ON qr.funcionario_criador_id = f.id
                WHERE qr.evento_id = ?
                ORDER BY qr.data_criacao DESC
            """, (evento_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def listar_por_funcionario(self, funcionario_id: int) -> List[Dict[str, Any]]:
        """Lista QR codes criados por um funcionário"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT qr.*, e.nome as evento_nome, e.tipo as evento_tipo
                FROM qr_codes qr
                JOIN eventos e ON qr.evento_id = e.id
                WHERE qr.funcionario_criador_id = ?
                ORDER BY qr.data_criacao DESC
            """, (funcionario_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def estatisticas_por_evento(self, evento_id: int) -> Dict[str, int]:
        """Retorna estatísticas de uso dos QR codes de um evento"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT status, COUNT(*) as total
                FROM qr_codes 
                WHERE evento_id = ?
                GROUP BY status
            """, (evento_id,))
            
            stats = {'ativo': 0, 'usado': 0, 'expirado': 0, 'inativo': 0}
            for row in cursor.fetchall():
                stats[row['status']] = row['total']
            
            stats['total'] = sum(stats.values())
            return stats