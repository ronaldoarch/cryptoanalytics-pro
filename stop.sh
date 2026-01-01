#!/bin/bash
# Script para parar o CryptoAnalytics Pro

echo "🛑 Parando CryptoAnalytics Pro..."

# Encontrar e encerrar processos na porta 8000
PIDS=$(lsof -ti:8000)

if [ -z "$PIDS" ]; then
    echo "✅ Nenhum processo rodando na porta 8000"
else
    echo "Encerrando processos: $PIDS"
    kill -9 $PIDS 2>/dev/null
    sleep 1
    echo "✅ Processos encerrados"
fi

# Também encerrar processos python main.py
PYTHON_PIDS=$(ps aux | grep "[p]ython.*main.py" | awk '{print $2}')
if [ ! -z "$PYTHON_PIDS" ]; then
    echo "Encerrando processos Python: $PYTHON_PIDS"
    kill -9 $PYTHON_PIDS 2>/dev/null
    echo "✅ Processos Python encerrados"
fi

echo ""
echo "✅ Porta 8000 liberada!"

