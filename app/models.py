"""
Modelos Pydantic para validação de dados
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class CryptoInfo(BaseModel):
    """Informações básicas de uma criptomoeda"""
    id: str
    name: str
    symbol: str
    current_price: float = Field(..., description="Preço atual em USD")
    market_cap: float = Field(..., description="Market cap em USD")
    total_volume: float = Field(..., description="Volume total em USD")
    price_change_24h: float = Field(..., description="Variação percentual em 24h")
    high_24h: float = Field(..., description="Maior preço em 24h")
    low_24h: float = Field(..., description="Menor preço em 24h")
    last_updated: str = Field(..., description="Data da última atualização")

class PriceData(BaseModel):
    """Dados de preço históricos"""
    timestamp: str
    price: float
    volume: float

class HistoricalData(BaseModel):
    """Dados históricos de uma criptomoeda"""
    coin_id: str
    prices: List[PriceData]
    period_days: int

class PredictionResponse(BaseModel):
    """Resposta de predição de preço"""
    coin_id: str
    current_price: float
    predicted_price: float = Field(..., description="Preço predito")
    predicted_change: float = Field(..., description="Variação percentual predita")
    confidence: float = Field(..., ge=0, le=1, description="Nível de confiança (0-1)")
    days_ahead: int = Field(..., description="Número de dias à frente")
    prediction_date: str
    model_info: Dict[str, str] = Field(..., description="Informações do modelo")

class TechnicalAnalysis(BaseModel):
    """Análise técnica de uma criptomoeda"""
    coin_id: str
    sma_20: float = Field(..., description="Média móvel simples de 20 períodos")
    sma_50: float = Field(..., description="Média móvel simples de 50 períodos")
    ema_12: float = Field(..., description="Média móvel exponencial de 12 períodos")
    ema_26: float = Field(..., description="Média móvel exponencial de 26 períodos")
    rsi: float = Field(..., ge=0, le=100, description="RSI (0-100)")
    macd: float = Field(..., description="MACD")
    signal: str = Field(..., description="Sinal de compra/venda/manutenção")
    support_level: float = Field(..., description="Nível de suporte")
    resistance_level: float = Field(..., description="Nível de resistência")
    trend: str = Field(..., description="Tendência (alta/baixa/lateral)")

class CryptoListResponse(BaseModel):
    """Lista de criptomoedas disponíveis"""
    total: int
    cryptos: List[Dict[str, str]]

class ErrorResponse(BaseModel):
    """Resposta de erro"""
    error: str
    detail: Optional[str] = None
    status_code: int

