"""
Engine de Machine Learning para predição de preços de criptomoedas
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from typing import List, Dict, Tuple
from app.data_fetcher import coin_gecko
import pickle
import os

class MLPredictor:
    """Classe para predição de preços usando Machine Learning"""
    
    def __init__(self):
        self.model = None
        self.models_dir = "models"
        os.makedirs(self.models_dir, exist_ok=True)
    
    def _create_features(self, prices: List[float], volumes: List[float] = None) -> np.ndarray:
        """Cria features para o modelo ML"""
        if len(prices) < 20:
            # Se não há dados suficientes, retorna features padrão
            return np.array([[0] * 10])
        
        features = []
        
        # Features de preço
        current_price = prices[-1]
        price_change_1d = ((prices[-1] - prices[-2]) / prices[-2] * 100) if len(prices) > 1 else 0
        price_change_3d = ((prices[-1] - prices[-4]) / prices[-4] * 100) if len(prices) > 4 else 0
        price_change_7d = ((prices[-1] - prices[-8]) / prices[-8] * 100) if len(prices) > 8 else 0
        
        # Médias móveis
        sma_5 = np.mean(prices[-5:])
        sma_10 = np.mean(prices[-10:])
        sma_20 = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
        
        # Volatilidade
        volatility = np.std(prices[-10:]) / np.mean(prices[-10:]) if len(prices) >= 10 else 0
        
        # Features de volume (se disponível)
        volume_avg = np.mean(volumes[-10:]) if volumes and len(volumes) >= 10 else 0
        volume_ratio = volumes[-1] / volume_avg if volumes and volume_avg > 0 else 1
        
        features.append([
            current_price,
            price_change_1d,
            price_change_3d,
            price_change_7d,
            sma_5,
            sma_10,
            sma_20,
            volatility,
            volume_avg,
            volume_ratio
        ])
        
        return np.array(features)
    
    def _prepare_training_data(self, prices: List[float], volumes: List[float] = None, 
                               days_ahead: int = 7) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara dados para treinamento"""
        X, y = [], []
        
        window_size = 30
        for i in range(window_size, len(prices) - days_ahead):
            # Features
            feature_window = prices[i-window_size:i]
            volume_window = volumes[i-window_size:i] if volumes else None
            features = self._create_features(feature_window, volume_window)[0]
            X.append(features)
            
            # Target (preço futuro)
            future_price = prices[i + days_ahead - 1]
            y.append(future_price)
        
        return np.array(X), np.array(y)
    
    def train_model(self, coin_id: str, days_ahead: int = 7) -> Dict:
        """Treina o modelo para uma criptomoeda específica"""
        # Buscar dados históricos
        historical_data = coin_gecko.get_historical_data(coin_id, days=90)
        
        if len(historical_data) < 50:
            raise ValueError(f"Dados insuficientes para treinar modelo: {coin_id}")
        
        prices = [item["price"] for item in historical_data]
        volumes = [item.get("volume", 0) for item in historical_data]
        
        # Preparar dados
        X, y = self._prepare_training_data(prices, volumes, days_ahead)
        
        if len(X) < 10:
            raise ValueError("Dados insuficientes para treinamento")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Treinar modelo
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Salvar modelo
        model_path = os.path.join(self.models_dir, f"{coin_id}_{days_ahead}d.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        return {
            "coin_id": coin_id,
            "days_ahead": days_ahead,
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "model_path": model_path
        }
    
    def load_model(self, coin_id: str, days_ahead: int = 7) -> bool:
        """Carrega modelo salvo"""
        model_path = os.path.join(self.models_dir, f"{coin_id}_{days_ahead}d.pkl")
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            return True
        return False
    
    def predict(self, coin_id: str, days_ahead: int = 7) -> Dict:
        """Faz predição de preço"""
        # Tentar carregar modelo existente
        if not self.load_model(coin_id, days_ahead):
            # Se não existe, treinar novo modelo
            self.train_model(coin_id, days_ahead)
        
        # Buscar dados recentes
        historical_data = coin_gecko.get_historical_data(coin_id, days=60)
        prices = [item["price"] for item in historical_data]
        volumes = [item.get("volume", 0) for item in historical_data]
        
        if len(prices) < 30:
            raise ValueError(f"Dados insuficientes para predição: {coin_id}")
        
        # Criar features
        features = self._create_features(prices, volumes)
        
        # Fazer predição
        predicted_price = self.model.predict(features)[0]
        current_price = prices[-1]
        
        # Calcular confiança (baseado na variância das predições das árvores)
        if hasattr(self.model, 'estimators_'):
            tree_predictions = np.array([tree.predict(features)[0] for tree in self.model.estimators_])
            confidence = 1 - (np.std(tree_predictions) / np.mean(tree_predictions)) if np.mean(tree_predictions) > 0 else 0.5
            confidence = max(0, min(1, confidence))  # Limitar entre 0 e 1
        else:
            confidence = 0.7  # Confiança padrão
        
        predicted_change = ((predicted_price - current_price) / current_price) * 100
        
        return {
            "coin_id": coin_id,
            "current_price": round(current_price, 2),
            "predicted_price": round(predicted_price, 2),
            "predicted_change": round(predicted_change, 2),
            "confidence": round(confidence, 3),
            "days_ahead": days_ahead,
            "prediction_date": historical_data[-1]["timestamp"],
            "model_info": {
                "type": "RandomForestRegressor",
                "estimators": self.model.n_estimators if hasattr(self.model, 'n_estimators') else 100
            }
        }

# Instância global do preditor
ml_predictor = MLPredictor()

