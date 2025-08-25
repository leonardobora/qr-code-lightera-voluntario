# QR Code System - Festa de Final de Ano 🎄

Sistema de geração e validação de QR Codes para a Festa de Final de Ano corporativa.

## 📋 Características

- **Geração de QR Codes únicos** para cada funcionário
- **Validação de entrada** na festa
- **Interface web responsiva** com Bootstrap 5
- **Scanner de QR Code** via browser usando HTML5-QRCode
- **Banco de dados SQLite** para armazenamento
- **Sistema de controle de uso único** (cada QR só pode ser usado uma vez)

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Dependências
```bash
pip install -r requirements.txt
```

### Estrutura do Projeto
```
qr-code-lightera-voluntario/
├── app.py                 # Aplicação Flask principal
├── database.py           # Gerenciamento do banco de dados
├── qr_generator.py       # Geração e validação de QR codes
├── requirements.txt      # Dependências do projeto
├── test_festa_qr.py     # Testes automatizados
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── qr_result.html
│   ├── validate.html
│   ├── validate_result.html
│   ├── scanner.html
│   └── list.html
└── static/
    ├── css/
    ├── js/
    └── qr_codes/        # QR codes gerados
```

## 📖 Como Usar

### 1. Inicializar o Sistema
```bash
python3 database.py  # Inicializa o banco de dados
```

### 2. Rodar a Aplicação
```bash
python3 app.py
```
O servidor será iniciado em `http://localhost:5000`

### 3. Gerar QR Code
1. Acesse a página inicial
2. Insira o nome do funcionário
3. Insira o ID do funcionário (ex: EMP001)
4. Clique em "Gerar QR Code"
5. Baixe ou salve a imagem do QR Code

### 4. Validar QR Code
**Opção 1: Scanner Automático**
1. Acesse `/scanner`
2. Permita acesso à câmera
3. Aponte a câmera para o QR Code
4. O sistema validará automaticamente

**Opção 2: Validação Manual**
1. Acesse `/validate`
2. Cole os dados do QR Code
3. Clique em "Validar Entrada"

## 🔧 API Endpoints

### Web Interface
- `GET /` - Página inicial (gerar QR codes)
- `POST /generate` - Gerar novo QR code
- `GET /validate` - Página de validação manual
- `POST /validate` - Validar QR code
- `GET /scanner` - Scanner de QR code
- `GET /list` - Listar todos os QR codes

### API REST
- `POST /api/validate` - Validar QR code via API
  ```json
  {
    "qr_data": "FESTA2024:EMP001:João Silva:20241225_120000:abcd1234"
  }
  ```

## 🎯 Formato do QR Code

Os QR codes seguem o formato específico para a Festa de Final de Ano:
```
FESTA2024:{employee_id}:{employee_name}:{timestamp}:{unique_id}
```

Exemplo:
```
FESTA2024:EMP001:João Silva:20241225_120000:abcd1234
```

## 📊 Funcionalidades

### ✅ Implementadas
- [x] Geração de QR codes únicos
- [x] Banco de dados SQLite
- [x] Interface web responsiva
- [x] Validação de QR codes
- [x] Scanner de câmera
- [x] Controle de uso único
- [x] Listagem de QR codes
- [x] API REST para validação

### 🎨 Design
- Interface moderna com Bootstrap 5
- Tema festivo com cores e ícones natalinos
- Responsivo para desktop e mobile
- Feedback visual claro para validações

## 🧪 Testes

Execute os testes automatizados:
```bash
python3 test_festa_qr.py
```

Os testes cobrem:
- Funcionalidade do banco de dados
- Geração de QR codes
- Validação de formato
- Lógica de negócio

## 🔒 Segurança

- QR codes únicos com timestamp e UUID
- Validação de formato obrigatória
- Controle de uso único por QR code
- Dados armazenados localmente (SQLite)

## 🎄 Características da Festa

O sistema é específico para a **Festa de Final de Ano 2024** com:
- Identificação "FESTA2024" em todos os QR codes
- Tema visual natalino
- Validação específica para o evento
- Relatórios de entrada da festa

## 📝 Notas Técnicas

### Estimativas do Projeto
- **Tempo de desenvolvimento**: 3-4 horas (conforme especificação)
- **Complexidade**: Baixa-Média
- **Stack**: Python 3.8+, Flask, SQLite, HTML5-QRCode, Bootstrap 5

### Bibliotecas Utilizadas
- **Flask**: Framework web Python
- **qrcode[pil]**: Geração de QR codes
- **Pillow**: Processamento de imagens
- **SQLite**: Banco de dados (built-in Python)
- **HTML5-QRCode**: Scanner JavaScript
- **Bootstrap 5**: Framework CSS

## 🚀 Deploy

Para produção, considere:
1. Usar um servidor WSGI (Gunicorn, uWSGI)
2. Configurar HTTPS
3. Backup regular do banco de dados
4. Monitoramento de logs
5. Configurar SECRET_KEY segura

## 📞 Suporte

Este sistema foi desenvolvido para o **Programa Social Corporativo** como parte da feature de QR codes para a Festa de Final de Ano.

**Critérios de Aceite Atendidos:**
- ✅ Funcionalidade implementada conforme especificação
- ✅ Código revisado e testado
- ✅ Documentação atualizada
- ✅ Testes criados

---

*Desenvolvido com ❤️ para a Festa de Final de Ano 2024* 🎄