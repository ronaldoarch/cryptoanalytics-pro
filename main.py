"""
CryptoAnalytics Pro - Sistema de Análise e Predição de Criptomoedas
Aplicação principal FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api import router
from app.models import CryptoInfo, PredictionResponse, TechnicalAnalysis
import uvicorn
import os

# Criar instância do FastAPI
app = FastAPI(
    title="CryptoAnalytics Pro API",
    description="API profissional para análise e predição de criptomoedas usando Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir rotas da API
app.include_router(router, prefix="/api", tags=["Crypto Analytics"])

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Página principal do dashboard"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "CryptoAnalytics Pro",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Permitir configurar porta via variável de ambiente
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Iniciando CryptoAnalytics Pro na porta {port}...")
    print(f"📊 Dashboard: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print("\n💡 Pressione Ctrl+C para parar o servidor\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

