"""
Endpoints da API REST
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models import (
    CryptoInfo, PredictionResponse, TechnicalAnalysis,
    CryptoListResponse, ErrorResponse
)
from app.data_fetcher import coin_gecko
from app.ml_engine import ml_predictor
from app.technical_analysis import analyzer

router = APIRouter()

@router.get("/crypto/{coin_id}", response_model=CryptoInfo)
async def get_crypto_info(coin_id: str):
    """
    Obtém informações básicas de uma criptomoeda
    
    - **coin_id**: ID da criptomoeda (ex: bitcoin, ethereum)
    """
    try:
        data = coin_gecko.get_market_data(coin_id)
        return CryptoInfo(**data)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Criptomoeda '{coin_id}' não encontrada ou erro ao buscar dados: {str(e)}"
        )

@router.get("/predict/{coin_id}", response_model=PredictionResponse)
async def predict_price(
    coin_id: str,
    days: int = Query(7, ge=1, le=30, description="Número de dias à frente para predição")
):
    """
    Obtém predição de preço usando Machine Learning
    
    - **coin_id**: ID da criptomoeda
    - **days**: Número de dias à frente (1-30)
    """
    try:
        prediction = ml_predictor.predict(coin_id, days_ahead=days)
        return PredictionResponse(**prediction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar predição: {str(e)}"
        )

@router.get("/analysis/{coin_id}", response_model=TechnicalAnalysis)
async def get_technical_analysis(coin_id: str):
    """
    Obtém análise técnica completa de uma criptomoeda
    
    - **coin_id**: ID da criptomoeda
    """
    try:
        analysis = analyzer.analyze(coin_id)
        return TechnicalAnalysis(**analysis)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar análise técnica: {str(e)}"
        )

@router.get("/cryptos", response_model=CryptoListResponse)
async def list_cryptos(
    limit: int = Query(50, ge=1, le=100, description="Número máximo de criptomoedas")
):
    """
    Lista as principais criptomoedas disponíveis
    
    - **limit**: Número máximo de resultados (1-100)
    """
    try:
        cryptos = coin_gecko.get_top_cryptos(limit=limit)
        return CryptoListResponse(
            total=len(cryptos),
            cryptos=cryptos
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar criptomoedas: {str(e)}"
        )

@router.get("/trending", response_model=CryptoListResponse)
async def get_trending_cryptos(
    limit: int = Query(10, ge=1, le=20, description="Número máximo de resultados")
):
    """
    Obtém lista de criptomoedas em alta (trending)
    
    - **limit**: Número máximo de resultados (1-20)
    """
    try:
        cryptos = coin_gecko.get_trending_coins(limit=limit)
        return CryptoListResponse(
            total=len(cryptos),
            cryptos=cryptos
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar criptomoedas em alta: {str(e)}"
        )

@router.get("/historical/{coin_id}")
async def get_historical_data(
    coin_id: str,
    days: int = Query(30, ge=1, le=365, description="Número de dias de histórico")
):
    """
    Obtém dados históricos de preço de uma criptomoeda
    
    - **coin_id**: ID da criptomoeda
    - **days**: Número de dias de histórico (1-365)
    """
    try:
        historical = coin_gecko.get_historical_data(coin_id, days=days)
        return {
            "coin_id": coin_id,
            "period_days": days,
            "data_points": len(historical),
            "prices": historical
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar dados históricos: {str(e)}"
        )

