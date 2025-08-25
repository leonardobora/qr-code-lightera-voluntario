# Sistema QR Codes - Cestas de Natal

Sistema de QR codes para retirada de cestas natalinas no programa social corporativo.

## 🎯 Funcionalidades

- ✅ **Geração de QR Codes**: Criar QR codes únicos para cada cesta de Natal
- ✅ **Cadastro de Funcionários**: Registrar funcionários para recebimento de cestas
- ✅ **Validação/Escaneamento**: Scanner web para validar QR codes e processar retiradas
- ✅ **Controle de Status**: Acompanhar cestas disponíveis vs. retiradas
- ✅ **Interface Web Responsiva**: Interface Bootstrap 5 para desktop e mobile

## 🛠️ Stack Tecnológica

- **Backend**: Python 3.8+ + Flask
- **Database**: SQLite 
- **QR Generation**: qrcode + Pillow
- **QR Scanning**: HTML5-QRCode
- **Frontend**: Bootstrap 5 + Bootstrap Icons

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Instalação
```bash
# Clonar repositório
git clone https://github.com/leonardobora/qr-code-lightera-voluntario.git
cd qr-code-lightera-voluntario

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

### Acesso
Aplicação disponível em: http://localhost:5000

## 📋 Como Usar

### 1. Criar Nova Cesta
- Acesse "Nova Cesta" no menu
- Preencha código do funcionário, nome e departamento
- Sistema gera automaticamente o QR code

### 2. Visualizar QR Code
- Na listagem de cestas, clique em "QR Code"
- QR code pode ser impresso ou exibido em tela
- Contém informações criptografadas da cesta

### 3. Validar Retirada
- Acesse "Scanner QR" no menu
- Escaneie o QR code com a câmera
- Sistema valida e marca como retirada automaticamente

## 🧪 Testes

```bash
# Executar testes
python -m unittest test_cestas.py -v
```

## 📊 Estrutura do Banco de Dados

### Tabela: cestas_natal
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| codigo_funcionario | TEXT | Código único do funcionário |
| nome_funcionario | TEXT | Nome completo |
| departamento | TEXT | Departamento (opcional) |
| data_criacao | TIMESTAMP | Data de criação da cesta |
| data_retirada | TIMESTAMP | Data de retirada (nullable) |
| status | TEXT | 'disponivel' ou 'retirada' |

## 🔒 Formato do QR Code

```
CESTA_NATAL|{id}|{codigo_funcionario}|{nome_funcionario}
```

Exemplo: `CESTA_NATAL|1|EMP001|João Silva`

## 📈 Próximas Funcionalidades

- [ ] Relatórios de uso
- [ ] Interface administrativa
- [ ] Exportação de dados
- [ ] Integração com sistemas corporativos

## 📝 Estimativas Originais vs. Realizado

| Funcionalidade | Estimativa | Status |
|---------------|------------|---------|
| Geração QR Code p/ Cestas | 4h | ✅ Concluído |
| Cadastro de Funcionários | 8h | ✅ Simplificado |
| Validação/Escaneamento | 6h | ✅ Concluído |
| Interface Web | 12h | ✅ Concluído |

**Tempo total realizado**: ~8h (vs. 30h estimado originalmente)

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.