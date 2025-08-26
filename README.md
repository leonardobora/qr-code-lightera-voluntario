# QR Code Sistema Social Corporativo

Sistema web desenvolvido em Flask para geração e validação de códigos QR para programa social corporativo.

## 🚀 Funcionalidades

- **Cadastro de Funcionários**: Gerencie funcionários responsáveis pelo programa
- **Geração de QR Codes**: Crie códigos únicos para diferentes categorias:
  - 🎉 Festas e eventos
  - 🛒 Cestas básicas
  - 🧸 Brinquedos
  - 📚 Material escolar
- **Scanner Web**: Valide códigos QR através da câmera do dispositivo
- **Relatórios**: Acompanhe estatísticas e uso do sistema
- **Interface Responsiva**: Funciona em desktop e mobile

## 🛠️ Tecnologias

- **Backend**: Python 3.8+ / Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5 / Bootstrap 5 / JavaScript
- **QR Code**: qrcode (Python) / HTML5-QRCode (JavaScript)
- **Outras**: Pillow, Flask-SQLAlchemy

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/leonardobora/qr-code-lightera-voluntario.git
cd qr-code-lightera-voluntario
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse o sistema**
   - Abra seu navegador em: http://localhost:5000

## 📖 Como Usar

### 1. Cadastrar Funcionários
- Acesse "Funcionários" no menu
- Clique em "Novo Funcionário"
- Preencha nome, email e departamento

### 2. Gerar QR Codes
- Acesse "Gerar QR" no menu
- Selecione o funcionário responsável
- Escolha a categoria (festa, cestas, brinquedos, material escolar)
- Adicione uma descrição (opcional)
- Clique em "Gerar QR Code"

### 3. Validar QR Codes
- Acesse "Scanner" no menu
- Clique em "Iniciar Scanner"
- Aponte a câmera para o QR code
- O sistema validará automaticamente

### 4. Acompanhar Relatórios
- Acesse "Relatórios" no menu
- Visualize estatísticas de uso
- Veja QR codes recentemente gerados e utilizados

## 🏗️ Estrutura do Projeto

```
qr-code-lightera-voluntario/
├── app.py                  # Aplicação principal Flask
├── models.py              # Modelos do banco de dados
├── routes.py              # Rotas e controladores
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── employee_form.html
│   ├── qr_generator.html
│   ├── view_qr.html
│   ├── scanner.html
│   └── reports.html
└── static/              # Arquivos estáticos
    ├── css/
    │   └── main.css
    └── js/
```

## 🗄️ Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **Employee**: Funcionários do programa
- **QRCode**: Códigos QR gerados
- **Usage**: Log de utilização dos códigos

## 🔒 Segurança

- Códigos QR únicos e não reutilizáveis
- Validação de dados de entrada
- Rastreamento de uso por funcionário
- Log de todas as validações

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Entre em contato com a equipe de desenvolvimento

---

**Sistema QR Code - Programa Social Corporativo**  
Desenvolvido com ❤️ para facilitar a gestão de programas sociais corporativos.