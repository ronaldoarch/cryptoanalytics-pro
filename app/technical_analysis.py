"""
Módulo de análise técnica para criptomoedas
"""

import numpy as np
from typing import List, Dict
from app.data_fetcher import coin_gecko

class TechnicalAnalyzer:
    """Classe para análise técnica de criptomoedas"""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> float:
        """Calcula Média Móvel Simples (SMA)"""
        if len(prices) < period:
            return np.mean(prices) if prices else 0
        return np.mean(prices[-period:])
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Calcula Média Móvel Exponencial (EMA)"""
        if not prices:
            return 0
        
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calcula RSI (Relative Strength Index)"""
        if len(prices) < period + 1:
            return 50.0  # Valor neutro
        
        deltas = np.diff(prices[-period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    @staticmethod
    def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26) -> float:
        """Calcula MACD (Moving Average Convergence Divergence)"""
        if len(prices) < slow:
            return 0
        
        ema_fast = TechnicalAnalyzer.calculate_ema(prices, fast)
        ema_slow = TechnicalAnalyzer.calculate_ema(prices, slow)
        
        return round(ema_fast - ema_slow, 2)
    
    @staticmethod
    def find_support_resistance(prices: List[float]) -> tuple:
        """Encontra níveis de suporte e resistência"""
        if not prices:
            return 0, 0
        
        recent_prices = prices[-30:] if len(prices) > 30 else prices
        support = min(recent_prices)
        resistance = max(recent_prices)
        
        return round(support, 2), round(resistance, 2)
    
    @staticmethod
    def determine_trend(prices: List[float], sma_20: float, sma_50: float) -> str:
        """Determina a tendência do mercado"""
        if len(prices) < 2:
            return "lateral"
        
        current_price = prices[-1]
        
        if current_price > sma_20 > sma_50:
            return "alta"
        elif current_price < sma_20 < sma_50:
            return "baixa"
        else:
            return "lateral"
    
    @staticmethod
    def generate_signal(rsi: float, macd: float, trend: str, current_price: float, 
                       sma_20: float) -> str:
        """Gera sinal de compra/venda/manutenção"""
        buy_signals = 0
        sell_signals = 0
        
        # RSI
        if rsi < 30:
            buy_signals += 1
        elif rsi > 70:
            sell_signals += 1
        
        # MACD
        if macd > 0:
            buy_signals += 1
        elif macd < 0:
            sell_signals += 1
        
        # Tendência
        if trend == "alta":
            buy_signals += 1
        elif trend == "baixa":
            sell_signals += 1
        
        # Preço vs SMA
        if current_price > sma_20:
            buy_signals += 1
        else:
            sell_signals += 1
        
        if buy_signals >= 3:
            return "compra"
        elif sell_signals >= 3:
            return "venda"
        else:
            return "manutenção"
    
    def analyze(self, coin_id: str) -> Dict:
        """Realiza análise técnica completa"""
        # Buscar dados históricos
        historical_data = coin_gecko.get_historical_data(coin_id, days=60)
        prices = [item["price"] for item in historical_data]
        
        if not prices:
            raise ValueError(f"Não foi possível obter dados para {coin_id}")
        
        # Calcular indicadores
        sma_20 = self.calculate_sma(prices, 20)
        sma_50 = self.calculate_sma(prices, 50)
        ema_12 = self.calculate_ema(prices, 12)
        ema_26 = self.calculate_ema(prices, 26)
        rsi = self.calculate_rsi(prices)
        macd = self.calculate_macd(prices)
        
        # Suporte e resistência
        support, resistance = self.find_support_resistance(prices)
        
        # Tendência
        trend = self.determine_trend(prices, sma_20, sma_50)
        
        # Sinal
        current_price = prices[-1]
        signal = self.generate_signal(rsi, macd, trend, current_price, sma_20)
        
        return {
            "coin_id": coin_id,
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "ema_12": round(ema_12, 2),
            "ema_26": round(ema_26, 2),
            "rsi": round(rsi, 2),
            "macd": round(macd, 2),
            "signal": signal,
            "support_level": support,
            "resistance_level": resistance,
            "trend": trend
        }

# Instância global do analisador
analyzer = TechnicalAnalyzer()

