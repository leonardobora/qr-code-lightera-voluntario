# Sistema QR Codes - Lightera Voluntário

Sistema de validação e controle de status para QR codes do programa social corporativo da Lightera.

## ✨ Funcionalidades Implementadas

### 🔧 Sistema de Validação e Controle de Status
- ✅ Geração de QR codes com tipos específicos (festa, cestas, brinquedos, material escolar)
- ✅ Validação de QR codes com verificação de status
- ✅ Controle de status: **pendente** → **usado** → **expirado**
- ✅ Sistema de expiração automática baseado em tempo
- ✅ Associação de QR codes a funcionários
- ✅ Metadados personalizáveis para cada QR code

### 🌐 Interface Web Completa
- ✅ Interface responsiva com Bootstrap 5
- ✅ Abas para diferentes funcionalidades:
  - **Validar QR Code**: Inserir código e verificar status
  - **Gerar QR Code**: Criar novos códigos com configurações
  - **Escanear QR Code**: Scanner integrado via HTML5-QRCode

### 🔗 API REST
- ✅ `POST /api/generate` - Gerar novo QR code
- ✅ `POST /api/validate` - Validar QR code existente
- ✅ `POST /api/use` - Marcar QR code como usado
- ✅ `GET /api/employee/<id>/qrcodes` - Listar QR codes de funcionário

## 🛠️ Stack Técnica

- **Backend**: Python 3.8+ com Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **QR Code**: 
  - Geração: `qrcode` library (Python)
  - Scanner: `html5-qrcode` (JavaScript)
- **Imagens**: Pillow (PIL)

## 📊 Status de QR Codes

| Status | Descrição | Pode ser usado? |
|--------|-----------|-----------------|
| `pending` | QR code válido e disponível para uso | ✅ Sim |
| `used` | QR code já foi utilizado | ❌ Não |
| `expired` | QR code expirou por tempo | ❌ Não |

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar Aplicação
```bash
python app.py
```

### 3. Acessar Interface
Abra o navegador em: `http://localhost:5000`

## 🧪 Executar Testes

```bash
python -m unittest test_validation.py -v
```

## 📝 Uso da API

### Gerar QR Code
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "qr_type": "festa", 
    "employee_id": "EMP001", 
    "duration_hours": 24,
    "metadata": "Festa de fim de ano"
  }'
```

### Validar QR Code
```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"code": "uuid-do-qr-code"}'
```

### Usar QR Code
```bash
curl -X POST http://localhost:5000/api/use \
  -H "Content-Type: application/json" \
  -d '{"code": "uuid-do-qr-code"}'
```

## 📋 Tipos de QR Code Suportados

- `festa` - Festas e eventos corporativos
- `cestas` - Cestas básicas
- `brinquedos` - Distribuição de brinquedos
- `material_escolar` - Material escolar

## 🗄️ Estrutura do Banco de Dados

### Tabela `qr_codes`
- `id` - ID único
- `code` - Código UUID do QR
- `qr_type` - Tipo do QR code
- `status` - Status atual (pending/used/expired)
- `created_at` - Data de criação
- `used_at` - Data de uso (se aplicável)
- `expires_at` - Data de expiração
- `employee_id` - ID do funcionário
- `metadata` - Informações adicionais

### Tabela `employees`
- `id` - ID único
- `employee_id` - ID do funcionário
- `name` - Nome do funcionário
- `department` - Departamento
- `created_at` - Data de cadastro

## 🎯 Implementação Conforme Especificação

Este sistema implementa todos os requisitos da issue #9:

- ✅ **Funcionalidade implementada conforme especificação**
- ✅ **Código revisado e testado** (10 testes unitários)
- ✅ **Documentação atualizada** (este README)
- ✅ **Testes criados** (suite completa de testes)

**Stack**: ✅ Python 3.8+, ✅ Flask, ✅ SQLite, ✅ HTML5-QRCode, ✅ Bootstrap 5

---

*Desenvolvido para o Sistema QR Codes do Programa Social Corporativo da Lightera*