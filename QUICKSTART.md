# 🚀 Guia Rápido de Início

## Instalação Rápida

### 1. Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação
```bash
python main.py
# ou
python3 main.py
# ou use o script
./start.sh
```

### 4. Parar a aplicação
```bash
# Pressione Ctrl+C no terminal onde está rodando
# ou use o script
./stop.sh
```

**Nota:** Se aparecer erro "Address already in use", significa que a porta 8000 está ocupada. Use `./stop.sh` para liberar a porta.

### 4. Acessar
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Alternativa**: http://localhost:8000/redoc

## Testar a API

### Usando Python
```bash
python example_usage.py
```

### Usando cURL
```bash
# Informações do Bitcoin
curl http://localhost:8000/api/crypto/bitcoin

# Análise técnica
curl http://localhost:8000/api/analysis/bitcoin

# Predição ML
curl http://localhost:8000/api/predict/bitcoin?days=7
```

### Usando o Dashboard Web
1. Acesse http://localhost:8000
2. Digite o nome de uma criptomoeda (ex: bitcoin, ethereum)
3. Clique em "Buscar" ou pressione Enter
4. Explore as análises e predições!

## Criptomoedas Populares para Testar

- `bitcoin` - Bitcoin
- `ethereum` - Ethereum
- `cardano` - Cardano
- `solana` - Solana
- `binancecoin` - Binance Coin
- `ripple` - Ripple
- `polkadot` - Polkadot
- `dogecoin` - Dogecoin

## Estrutura do Projeto

```
python/
├── main.py              # Aplicação principal
├── app/                 # Módulos da aplicação
│   ├── api.py          # Endpoints REST
│   ├── models.py       # Modelos Pydantic
│   ├── ml_engine.py    # Engine de ML
│   ├── data_fetcher.py # Integração APIs
│   └── technical_analysis.py # Análise técnica
├── static/             # Frontend
│   ├── index.html     # Dashboard
│   ├── css/           # Estilos
│   └── js/            # JavaScript
├── models/             # Modelos ML salvos
└── requirements.txt    # Dependências
```

## Próximos Passos

1. ✅ Instalar e executar a aplicação
2. ✅ Explorar o dashboard web
3. ✅ Testar os endpoints da API
4. ✅ Ler a documentação em `/docs`
5. ✅ Personalizar e expandir o projeto

## Dicas

- A primeira predição pode demorar um pouco (treinamento do modelo)
- Os modelos são salvos em `models/` para reutilização
- A API CoinGecko tem rate limits (use com moderação)
- Para produção, considere adicionar cache e autenticação

## Problemas Comuns

### Erro de conexão
- Verifique se a API está rodando
- Verifique sua conexão com a internet
- A API CoinGecko pode estar temporariamente indisponível

### Erro ao buscar criptomoeda
- Verifique se o ID está correto (use IDs da CoinGecko)
- Algumas criptomoedas podem não ter dados suficientes

### Erro ao fazer predição
- O modelo precisa de dados históricos suficientes
- Tente com criptomoedas mais populares primeiro

## Suporte

Consulte o README.md completo para mais informações detalhadas.

