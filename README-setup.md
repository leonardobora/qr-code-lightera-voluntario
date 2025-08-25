# QR Code Lightera Voluntario - Setup Guide

## 📦 Dependências Python

Este projeto requer Python 3.8+ e utiliza as seguintes dependências principais:

### 🏗️ Core Dependencies (Aplicação)
- **Flask 3.0.0** - Framework web backend
- **qrcode 7.4.2** - Geração de códigos QR
- **Pillow 10.1.0** - Processamento de imagens
- **SQLite3** - Banco de dados local (built-in do Python)

### 📊 Análise e Visualização
- **pandas 2.1.4** - Análise de dados
- **plotly 5.17.0** - Visualizações e gráficos
- **numpy 1.26.2** - Computação numérica
- **kaleido 0.2.1** - Export de imagens do Plotly

### 🧪 Testes e Desenvolvimento
- **pytest 7.4.3** - Framework de testes
- **pytest-flask 1.3.0** - Testes específicos para Flask
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente

### 🔗 Extensões Flask
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-WTF 1.2.1** - Formulários e validação
- **WTForms 3.1.1** - Processamento de formulários

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/leonardobora/qr-code-lightera-voluntario.git
cd qr-code-lightera-voluntario
```

### 2. Instale as dependências
```bash
# Instalação básica
pip install -r requirements.txt

# Para desenvolvimento (inclui ferramentas adicionais)
pip install -r requirements-dev.txt
```

### 3. Verifique a instalação
```bash
python verify_setup.py
```

## ✅ Verificação de Setup

O script `verify_setup.py` testa:
- ✅ Dependências core do Flask
- ✅ Funcionalidade de geração de QR codes
- ✅ Bibliotecas de análise de dados
- ✅ Funcionalidade básica do Flask

### Saída esperada:
```
🚀 QR Code Lightera Voluntario - Dependency Verification
============================================================
🔍 Testing core application dependencies...
✅ Flask: 3.0.0
✅ QRCode library: Available
✅ Pillow (PIL): 10.1.0
✅ SQLite3: 3.45.1

🔍 Testing data analysis dependencies...
✅ Pandas: 2.1.4
✅ Plotly: 5.17.0
✅ NumPy: 1.26.2

🔍 Testing QR code generation...
✅ QR Code generation: Successful
✅ Generated QR image size: (370, 370)

🔍 Testing Flask functionality...
✅ Flask app creation: Successful
✅ Flask app context: Working

============================================================
📊 SUMMARY
✅ Tests passed: 4
❌ Tests failed: 0

🎉 All dependencies are properly installed and working!
🚀 You're ready to start developing the QR Code application!
```

## 🎯 Stack Tecnológico

- **Backend**: Python 3.8+ com Flask
- **Banco de Dados**: SQLite
- **QR Codes**: qrcode + Pillow
- **Frontend**: HTML5 + Bootstrap 5 + HTML5-QRCode (JavaScript)
- **Análise**: pandas + plotly

## 📁 Estrutura do Projeto

```
qr-code-lightera-voluntario/
├── requirements.txt          # Dependências principais
├── requirements-dev.txt      # Dependências de desenvolvimento
├── verify_setup.py          # Script de verificação
├── script.py                # Análise de funcionalidades
├── chart_script.py          # Geração de gráficos
└── README-setup.md          # Este arquivo
```

## 🔧 Desenvolvimento

### Executar análises do projeto:
```bash
# Análise de funcionalidades
python script.py

# Geração de gráficos
python chart_script.py
```

### Próximos passos:
1. Criar estrutura Flask básica
2. Implementar geração de QR codes
3. Criar interface web
4. Adicionar banco de dados SQLite
5. Implementar scanner de QR codes