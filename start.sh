#!/bin/bash
# Script para iniciar o CryptoAnalytics Pro

# Verificar se a porta está em uso
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Porta 8000 já está em uso!"
    echo "💡 Use './stop.sh' para liberar a porta ou configure PORT=8001 ./start.sh"
    exit 1
fi

echo "🚀 Iniciando CryptoAnalytics Pro..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação
python main.py

