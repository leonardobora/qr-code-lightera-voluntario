# QR Code Scanner - Lightera Voluntário

Sistema web para escaneamento de códigos QR usando HTML5-QRCode para programa social corporativo.

## 🚀 Funcionalidades

- ✅ Scanner QR via câmera do dispositivo (HTML5-QRCode)
- ✅ Interface responsiva com Bootstrap 5
- ✅ Suporte a múltiplas câmeras
- ✅ Processamento e validação de QR codes
- ✅ Feedback visual em tempo real

## 📋 Pré-requisitos

- Python 3.8+
- Flask
- Navegador moderno com suporte a câmera

## 🛠️ Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse http://localhost:5000

## 📱 Como Usar

1. Acesse a página inicial
2. Clique em "Iniciar Scanner"
3. Permita acesso à câmera quando solicitado
4. Aponte a câmera para um código QR
5. Aguarde o processamento automático

## 🏗️ Arquitetura

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **QR Scanner**: HTML5-QRCode library
- **Banco de dados**: SQLite (futuro)

## 📝 Rotas da API

- `GET /` - Página inicial
- `GET /scanner` - Página do scanner QR
- `POST /api/process_qr` - Processar dados do QR code

## 🔧 Desenvolvimento

Para desenvolvimento, o Flask roda em modo debug na porta 5000.

## 📄 Licença

Sistema desenvolvido para Lightera Voluntário - Programa Social Corporativo.