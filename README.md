# Sistema de QR Codes - Lightera Voluntário

Sistema básico para geração de QR codes únicos para programa social corporativo.

## Funcionalidades

- ✅ Geração de QR codes para diferentes tipos de eventos/itens:
  - 🎉 Festa
  - 🧺 Cestas
  - 🧸 Brinquedos 
  - 📚 Material Escolar

- ✅ Interface web responsiva com Bootstrap 5
- ✅ Armazenamento em banco SQLite
- ✅ Listagem de QR codes gerados
- ✅ Associação com funcionários responsáveis

## Stack Tecnológica

- **Backend**: Python 3.8+ com Flask
- **Banco de Dados**: SQLite
- **QR Code**: Biblioteca `qrcode` com Pillow
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript

## Instalação e Execução

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Executar a aplicação:
```bash
python app.py
```

3. Acessar no navegador:
```
http://localhost:5000
```

## Estrutura do Projeto

```
├── app.py                    # Aplicação Flask principal
├── requirements.txt          # Dependências Python
├── templates/
│   ├── index.html           # Página principal de geração
│   └── list.html            # Listagem de QR codes
├── tests/
│   └── test_qr_generation.py # Testes automatizados
└── qr_codes.db             # Banco SQLite (criado automaticamente)
```

## API Endpoints

- `GET /` - Página principal para gerar QR codes
- `POST /generate` - Endpoint para gerar novos QR codes
- `GET /list` - Listagem de QR codes gerados

## Executar Testes

```bash
python -m unittest tests.test_qr_generation -v
```

## Screenshots

### Interface Principal
![Interface Principal](https://github.com/user-attachments/assets/d56b24bc-0b91-4aa9-891d-9316516087d1)

### QR Code Gerado
![QR Code Gerado](https://github.com/user-attachments/assets/f53f0015-7770-4618-a665-fb4f681e17b9)

### Lista de QR Codes
![Lista de QR Codes](https://github.com/user-attachments/assets/30d273d8-5a57-4840-8601-4ec5b078abe1)

## Próximos Passos

- [ ] Implementar escaneamento de QR codes
- [ ] Adicionar validação de uso único
- [ ] Sistema de relatórios
- [ ] Interface administrativa
- [ ] Deploy em produção