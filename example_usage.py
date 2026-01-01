"""
Exemplos de uso da API CryptoAnalytics Pro
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """Imprime um título de seção formatado"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def example_get_crypto_info():
    """Exemplo: Obter informações de uma criptomoeda"""
    print_section("1. Informações de Criptomoeda")
    
    coin_id = "bitcoin"
    response = requests.get(f"{BASE_URL}/crypto/{coin_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 {data['name']} ({data['symbol']})")
        print(f"💰 Preço Atual: ${data['current_price']:,.2f}")
        print(f"📈 Variação 24h: {data['price_change_24h']:+.2f}%")
        print(f"💵 Market Cap: ${data['market_cap']:,.2f}")
        print(f"📊 Volume 24h: ${data['total_volume']:,.2f}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())

def example_technical_analysis():
    """Exemplo: Análise técnica"""
    print_section("2. Análise Técnica")
    
    coin_id = "ethereum"
    response = requests.get(f"{BASE_URL}/analysis/{coin_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔍 Análise Técnica: {coin_id.upper()}")
        print(f"\n📊 Médias Móveis:")
        print(f"   SMA 20: ${data['sma_20']:,.2f}")
        print(f"   SMA 50: ${data['sma_50']:,.2f}")
        print(f"   EMA 12: ${data['ema_12']:,.2f}")
        print(f"   EMA 26: ${data['ema_26']:,.2f}")
        
        print(f"\n📈 Indicadores:")
        print(f"   RSI: {data['rsi']}")
        print(f"   MACD: {data['macd']:.2f}")
        
        print(f"\n🎯 Sinais:")
        print(f"   Sinal: {data['signal'].upper()}")
        print(f"   Tendência: {data['trend'].upper()}")
        print(f"   Suporte: ${data['support_level']:,.2f}")
        print(f"   Resistência: ${data['resistance_level']:,.2f}")
    else:
        print(f"❌ Erro: {response.status_code}")

def example_ml_prediction():
    """Exemplo: Predição com Machine Learning"""
    print_section("3. Predição com Machine Learning")
    
    coin_id = "bitcoin"
    days = 7
    response = requests.get(f"{BASE_URL}/predict/{coin_id}?days={days}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🤖 Predição para {days} dias: {coin_id.upper()}")
        print(f"\n💰 Preços:")
        print(f"   Atual: ${data['current_price']:,.2f}")
        print(f"   Predito: ${data['predicted_price']:,.2f}")
        print(f"   Variação: {data['predicted_change']:+.2f}%")
        
        print(f"\n📊 Confiança do Modelo:")
        confidence_percent = data['confidence'] * 100
        print(f"   {confidence_percent:.1f}%")
        
        print(f"\n🔧 Informações do Modelo:")
        print(f"   Tipo: {data['model_info']['type']}")
        print(f"   Estimadores: {data['model_info']['estimators']}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())

def example_list_cryptos():
    """Exemplo: Listar criptomoedas"""
    print_section("4. Listar Criptomoedas")
    
    limit = 10
    response = requests.get(f"{BASE_URL}/cryptos?limit={limit}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📋 Top {data['total']} Criptomoedas:\n")
        
        for idx, crypto in enumerate(data['cryptos'][:10], 1):
            print(f"{idx:2d}. {crypto['name']:20s} ({crypto['symbol']:5s}) "
                  f"${crypto['current_price']:>12,.2f}")
    else:
        print(f"❌ Erro: {response.status_code}")

def example_trending():
    """Exemplo: Criptomoedas em alta"""
    print_section("5. Criptomoedas em Alta")
    
    response = requests.get(f"{BASE_URL}/trending?limit=5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔥 Top {data['total']} Criptomoedas em Alta:\n")
        
        for idx, crypto in enumerate(data['cryptos'], 1):
            print(f"{idx}. {crypto['name']} ({crypto['symbol']})")
    else:
        print(f"❌ Erro: {response.status_code}")

def example_historical_data():
    """Exemplo: Dados históricos"""
    print_section("6. Dados Históricos")
    
    coin_id = "bitcoin"
    days = 7
    response = requests.get(f"{BASE_URL}/historical/{coin_id}?days={days}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📈 Dados Históricos: {coin_id.upper()} ({days} dias)")
        print(f"   Total de pontos: {data['data_points']}")
        
        if data['prices']:
            print(f"\n   Primeiros 5 registros:")
            for price_data in data['prices'][:5]:
                date = datetime.fromisoformat(price_data['timestamp'])
                print(f"   {date.strftime('%d/%m/%Y %H:%M')}: "
                      f"${price_data['price']:,.2f}")
    else:
        print(f"❌ Erro: {response.status_code}")

def main():
    """Executa todos os exemplos"""
    print("\n" + "🚀"*30)
    print("  CryptoAnalytics Pro - Exemplos de Uso da API")
    print("🚀"*30)
    
    try:
        # Verificar se a API está rodando
        health_check = requests.get("http://localhost:8000/health", timeout=2)
        if health_check.status_code != 200:
            print("\n⚠️  A API não está respondendo corretamente.")
            print("   Certifique-se de que o servidor está rodando:")
            print("   python main.py")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API.")
        print("   Certifique-se de que o servidor está rodando:")
        print("   python main.py")
        return
    
    # Executar exemplos
    example_get_crypto_info()
    example_technical_analysis()
    example_ml_prediction()
    example_list_cryptos()
    example_trending()
    example_historical_data()
    
    print("\n" + "="*60)
    print("  ✅ Exemplos concluídos!")
    print("="*60)
    print("\n💡 Dica: Acesse http://localhost:8000/docs para ver a")
    print("   documentação interativa completa da API.\n")

if __name__ == "__main__":
    main()

