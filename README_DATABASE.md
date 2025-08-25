# Modelos SQLite - Sistema QR Code Lightera

Este documento descreve os modelos de dados SQLite implementados para o sistema de QR codes da Lightera.

## 📊 Estrutura do Banco

### Tabelas Principais

#### 1. **funcionarios** (Funcionários/Voluntários)
```sql
CREATE TABLE funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cargo TEXT,
    telefone TEXT,
    ativo BOOLEAN DEFAULT 1,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. **eventos** (Eventos)
```sql
CREATE TABLE eventos (
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
);
```

#### 3. **qr_codes** (QR Codes)
```sql
CREATE TABLE qr_codes (
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
);
```

## 🎯 Tipos de Eventos Suportados

- **festa** - Festas e celebrações
- **cestas** - Distribuição de cestas básicas
- **brinquedos** - Doação de brinquedos
- **material_escolar** - Material escolar

## 📱 Status de QR Codes

- **ativo** - QR code disponível para uso
- **usado** - QR code já foi utilizado
- **expirado** - QR code expirado por data
- **inativo** - QR code desativado manualmente

## 🚀 Como Usar

### 1. Inicializar o Banco com Dados de Exemplo

```bash
python3 db_utils.py --init
```

### 2. Ver Estatísticas do Banco

```bash
python3 db_utils.py --stats
```

### 3. Resetar o Banco

```bash
python3 db_utils.py --reset --init
```

### 4. Usar os Modelos no Código

```python
from models import DatabaseManager, Funcionario, Evento, QRCode, EventType

# Inicializar banco
db_manager = DatabaseManager("lightera_qr.db")

# Usar modelos
funcionario_model = Funcionario(db_manager)
evento_model = Evento(db_manager)
qr_model = QRCode(db_manager)

# Criar funcionário
func_id = funcionario_model.criar(
    nome="João Silva",
    email="joao@lightera.org",
    cargo="Voluntário"
)

# Criar evento
evento_id = evento_model.criar(
    nome="Festa Junina 2024",
    tipo=EventType.FESTA,
    responsavel_id=func_id
)

# Criar QR code
qr_id = qr_model.criar(
    codigo="FESTA_JUNINA_001",
    evento_id=evento_id,
    funcionario_criador_id=func_id,
    destinatario_nome="Família Santos"
)

# Validar QR code
valido, mensagem = qr_model.validar_codigo("FESTA_JUNINA_001")
if valido:
    qr_model.usar_codigo("FESTA_JUNINA_001")
```

## 🧪 Executar Testes

```bash
python3 test_models.py
```

## 📁 Arquivos

- `models.py` - Modelos e classes principais
- `db_utils.py` - Utilitários de banco (inicialização, estatísticas)
- `test_models.py` - Testes automatizados
- `lightera_qr.db` - Arquivo do banco SQLite (criado após inicialização)

## 🔧 Funcionalidades Implementadas

### Funcionários
- ✅ Cadastro de funcionários/voluntários
- ✅ Busca por ID e email
- ✅ Listagem de funcionários ativos
- ✅ Atualização de dados
- ✅ Desativação (soft delete)

### Eventos
- ✅ Criação de eventos por tipo
- ✅ Associação com funcionário responsável
- ✅ Busca e listagem por tipo
- ✅ Atualização de dados
- ✅ Desativação de eventos

### QR Codes
- ✅ Geração de QR codes únicos
- ✅ Hash de segurança (SHA256)
- ✅ Validação de códigos
- ✅ Controle de status (ativo/usado/expirado)
- ✅ Associação com eventos e funcionários
- ✅ Estatísticas de uso
- ✅ Controle de expiração por data

## 🔗 Relacionamentos

```
funcionarios (1) ←→ (N) eventos (responsável)
funcionarios (1) ←→ (N) qr_codes (criador)
eventos (1) ←→ (N) qr_codes
```

## 📈 Próximos Passos

Com os modelos SQLite implementados, o sistema está pronto para:

1. **Interface Web** - Implementar Flask/Django para interface
2. **Geração de QR** - Integrar biblioteca `qrcode` 
3. **Scanner** - Implementar leitura de QR codes
4. **Relatórios** - Dashboard com estatísticas
5. **API REST** - Endpoints para integração

---

**Desenvolvido para:** Lightera - Sistema de Voluntários  
**Tecnologia:** Python + SQLite  
**Status:** ✅ Implementado e testado