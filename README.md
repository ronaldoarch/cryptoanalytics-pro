# 🚀 CryptoAnalytics Pro - Sistema de Análise e Predição de Criptomoedas

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub](https://img.shields.io/github/stars/ronaldoarch/cryptoanalytics-pro?style=social)

**Sistema profissional de análise de mercado de criptomoedas com predições usando Machine Learning**

[Características](#-características) • [Tecnologias](#-tecnologias) • [Instalação](#-instalação) • [Uso](#-uso) • [API](#-api)

</div>

---

## 📋 Sobre o Projeto

CryptoAnalytics Pro é uma aplicação completa que combina **análise de dados em tempo real**, **machine learning** e **visualizações interativas** para fornecer insights valiosos sobre o mercado de criptomoedas.

### 🎯 Objetivos do Projeto

- Demonstrar habilidades em **Python avançado**
- Implementar **APIs RESTful** com FastAPI
- Aplicar **Machine Learning** para predições
- Criar **visualizações interativas** e modernas
- Integrar com **APIs externas** (CoinGecko)
- Seguir **boas práticas** de desenvolvimento

---

## ✨ Características

- 🔄 **API REST completa** com FastAPI
- 🤖 **Modelos de ML** para predição de preços
- 📊 **Dashboard interativo** com gráficos em tempo real
- 💹 **Análise técnica** (médias móveis, RSI, etc.)
- 📈 **Visualizações** com Chart.js
- 🔐 **Validação de dados** com Pydantic
- 📝 **Documentação automática** (Swagger/OpenAPI)
- 🎨 **Interface moderna** e responsiva

---

## 🛠 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **NumPy & Pandas** - Manipulação de dados
- **Scikit-learn** - Machine Learning
- **Requests** - Integração com APIs externas

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript (ES6+)** - Interatividade
- **Chart.js** - Gráficos interativos
- **Bootstrap 5** - Design responsivo

### DevOps
- **Docker** (opcional) - Containerização
- **Git** - Controle de versão

---

## 📦 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd python
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python main.py
```

5. **Acesse a aplicação**
- Dashboard: http://localhost:8000
- API Docs: http://localhost:8000/docs
- API Alternativa: http://localhost:8000/redoc

---

## 🚀 Uso

### Dashboard Web

Acesse `http://localhost:8000` para visualizar o dashboard interativo com:
- Gráficos de preços em tempo real
- Análise técnica
- Predições de ML
- Comparação entre criptomoedas

### API REST

#### Obter informações de uma criptomoeda
```bash
GET /api/crypto/{coin_id}
```

#### Obter predição de preço
```bash
GET /api/predict/{coin_id}?days=7
```

#### Obter análise técnica
```bash
GET /api/analysis/{coin_id}
```

#### Listar criptomoedas disponíveis
```bash
GET /api/cryptos
```

Consulte a documentação interativa em `/docs` para ver todos os endpoints disponíveis.

---

## 📊 Exemplos de Uso da API

### Python
```python
import requests

# Obter dados do Bitcoin
response = requests.get("http://localhost:8000/api/crypto/bitcoin")
data = response.json()
print(data)

# Obter predição para 7 dias
response = requests.get("http://localhost:8000/api/predict/bitcoin?days=7")
prediction = response.json()
print(prediction)
```

### cURL
```bash
# Obter dados do Ethereum
curl http://localhost:8000/api/crypto/ethereum

# Obter análise técnica
curl http://localhost:8000/api/analysis/bitcoin
```

---

## 🏗 Estrutura do Projeto

```
python/
├── main.py                 # Aplicação principal FastAPI
├── app/
│   ├── __init__.py
│   ├── api.py             # Endpoints da API
│   ├── models.py          # Modelos Pydantic
│   ├── ml_engine.py       # Engine de Machine Learning
│   ├── data_fetcher.py    # Integração com APIs externas
│   └── technical_analysis.py  # Análise técnica
├── static/
│   ├── css/
│   │   └── style.css      # Estilos do dashboard
│   ├── js/
│   │   └── dashboard.js   # Lógica do frontend
│   └── index.html         # Dashboard principal
├── models/                # Modelos ML salvos
├── requirements.txt       # Dependências
└── README.md             # Documentação
```

---

## 🧪 Funcionalidades Técnicas

### Machine Learning
- Modelo de regressão para predição de preços
- Treinamento com dados históricos
- Validação cruzada
- Métricas de avaliação (MAE, RMSE)

### Análise Técnica
- Médias móveis (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Suporte e resistência

### API Features
- Validação automática de dados
- Tratamento de erros robusto
- Documentação automática (OpenAPI)
- Rate limiting (preparado)
- CORS configurado

---

## 📈 Melhorias Futuras

- [ ] Autenticação e autorização (JWT)
- [ ] Banco de dados para histórico
- [ ] WebSockets para atualizações em tempo real
- [ ] Mais modelos de ML (LSTM, Prophet)
- [ ] Alertas personalizados
- [ ] Backtesting de estratégias
- [ ] Deploy em cloud (AWS/GCP)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela! ⭐**

Feito com ❤️ usando Python e FastAPI

</div>

