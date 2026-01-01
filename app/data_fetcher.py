"""
Módulo para buscar dados de APIs externas (CoinGecko)
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time

class CoinGeckoAPI:
    """Cliente para a API CoinGecko"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "CryptoAnalytics-Pro/1.0"
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Faz uma requisição à API"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar dados da API: {str(e)}")
    
    def get_crypto_info(self, coin_id: str) -> Dict:
        """Obtém informações básicas de uma criptomoeda"""
        endpoint = f"coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        }
        return self._make_request(endpoint, params)
    
    def get_historical_data(self, coin_id: str, days: int = 30) -> List[Dict]:
        """Obtém dados históricos de preço"""
        endpoint = f"coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily" if days > 30 else "hourly"
        }
        data = self._make_request(endpoint, params)
        
        # Formatar dados históricos
        prices = []
        volumes_data = data.get("total_volumes", [])
        
        if "prices" in data:
            for idx, price_data in enumerate(data["prices"]):
                timestamp = datetime.fromtimestamp(price_data[0] / 1000)
                # Buscar volume correspondente ao mesmo timestamp
                volume = 0
                if volumes_data and idx < len(volumes_data):
                    volume = volumes_data[idx][1] if len(volumes_data[idx]) > 1 else 0
                
                prices.append({
                    "timestamp": timestamp.isoformat(),
                    "price": price_data[1],
                    "volume": volume
                })
        
        return prices
    
    def get_market_data(self, coin_id: str) -> Dict:
        """Obtém dados de mercado formatados"""
        data = self.get_crypto_info(coin_id)
        market_data = data.get("market_data", {})
        
        return {
            "id": data.get("id", coin_id),
            "name": data.get("name", ""),
            "symbol": data.get("symbol", "").upper(),
            "current_price": market_data.get("current_price", {}).get("usd", 0),
            "market_cap": market_data.get("market_cap", {}).get("usd", 0),
            "total_volume": market_data.get("total_volume", {}).get("usd", 0),
            "price_change_24h": market_data.get("price_change_percentage_24h", 0),
            "high_24h": market_data.get("high_24h", {}).get("usd", 0),
            "low_24h": market_data.get("low_24h", {}).get("usd", 0),
            "last_updated": market_data.get("last_updated", datetime.now().isoformat())
        }
    
    def get_trending_coins(self, limit: int = 10) -> List[Dict]:
        """Obtém lista de criptomoedas em alta"""
        endpoint = "search/trending"
        data = self._make_request(endpoint)
        
        coins = []
        if "coins" in data:
            for coin in data["coins"][:limit]:
                coin_data = coin.get("item", {})
                coins.append({
                    "id": coin_data.get("id", ""),
                    "name": coin_data.get("name", ""),
                    "symbol": coin_data.get("symbol", "").upper(),
                    "rank": coin_data.get("market_cap_rank", 0)
                })
        
        return coins
    
    def get_top_cryptos(self, limit: int = 50) -> List[Dict]:
        """Obtém lista das principais criptomoedas"""
        endpoint = "coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false"
        }
        data = self._make_request(endpoint, params)
        
        cryptos = []
        for coin in data:
            cryptos.append({
                "id": coin.get("id", ""),
                "name": coin.get("name", ""),
                "symbol": coin.get("symbol", "").upper(),
                "current_price": coin.get("current_price", 0),
                "market_cap": coin.get("market_cap", 0)
            })
        
        return cryptos

# Instância global do cliente
coin_gecko = CoinGeckoAPI()

