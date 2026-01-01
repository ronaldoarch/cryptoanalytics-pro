# 🔧 Solução de Problemas

## Problema: "Address already in use" (Porta 8000 ocupada)

### Solução Rápida
```bash
./stop.sh
```

### Solução Manual
```bash
# Encontrar processos na porta 8000
lsof -ti:8000

# Encerrar processos
kill -9 $(lsof -ti:8000)
```

### Usar Porta Diferente
```bash
# Usar porta 8001
PORT=8001 python main.py

# Ou no script
PORT=8001 ./start.sh
```

Depois acesse: http://localhost:8001

---

## Problema: "command not found: python"

### Solução
No macOS, use `python3` ao invés de `python`:

```bash
python3 -m venv venv
source venv/bin/activate
python3 main.py
```

---

## Problema: Erro ao instalar dependências

### Solução
1. Atualize pip, setuptools e wheel:
```bash
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

2. Instale as dependências novamente:
```bash
pip install -r requirements.txt
```

---

## Problema: Erro ao buscar criptomoeda

### Possíveis Causas
1. **Nome incorreto**: Use IDs da CoinGecko (ex: `bitcoin`, não `BTC`)
2. **Sem conexão**: Verifique sua conexão com a internet
3. **API indisponível**: A CoinGecko pode estar temporariamente indisponível

### Solução
- Verifique IDs válidos em: https://www.coingecko.com/
- Teste com criptomoedas populares: `bitcoin`, `ethereum`, `cardano`

---

## Problema: Erro ao fazer predição ML

### Possíveis Causas
1. **Dados insuficientes**: A criptomoeda precisa ter histórico suficiente
2. **Primeira execução**: O modelo precisa ser treinado (pode demorar)

### Solução
- Use criptomoedas mais populares primeiro
- Aguarde o treinamento do modelo (pode levar alguns segundos)

---

## Problema: Dashboard não carrega

### Verificações
1. O servidor está rodando? Verifique: http://localhost:8000/health
2. Os arquivos estáticos existem? Verifique: `ls static/`
3. Console do navegador mostra erros?

### Solução
```bash
# Verificar estrutura
ls -la static/

# Reiniciar servidor
./stop.sh
./start.sh
```

---

## Comandos Úteis

### Ver processos Python rodando
```bash
ps aux | grep python
```

### Ver o que está usando a porta 8000
```bash
lsof -i:8000
```

### Limpar cache Python
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Recriar ambiente virtual
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Ainda com problemas?

1. Verifique os logs do servidor no terminal
2. Verifique a versão do Python: `python3 --version` (deve ser 3.9+)
3. Verifique se todas as dependências foram instaladas: `pip list`
4. Consulte a documentação completa no README.md

