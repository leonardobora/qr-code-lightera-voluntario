#!/bin/bash

# Script para executar o sistema QR Code
echo "🚀 Iniciando Sistema QR Code - Programa Social Corporativo"

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Verificar se existe arquivo .env
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo de configuração..."
    cp .env.example .env
fi

# Executar aplicação
echo "🌐 Iniciando servidor Flask..."
echo "📱 Acesse: http://localhost:5000"
python app.py