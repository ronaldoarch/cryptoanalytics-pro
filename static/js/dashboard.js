// CryptoAnalytics Pro - Dashboard JavaScript

const API_BASE = '/api';
let currentCoinId = null;
let priceChart = null;
let historicalChart = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadTrendingCryptos();
    setupEventListeners();
    initializeHeroChart();
});

// Event Listeners
function setupEventListeners() {
    const searchInput = document.getElementById('cryptoSearch');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchCrypto();
            }
        });
    }
}

// Carregar criptomoedas em alta
async function loadTrendingCryptos() {
    try {
        const response = await fetch(`${API_BASE}/trending?limit=6`);
        const data = await response.json();
        
        const container = document.getElementById('trendingCryptos');
        if (!container) return;
        
        container.innerHTML = '';
        
        data.cryptos.forEach(crypto => {
            const card = createTrendingCard(crypto);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar criptomoedas em alta:', error);
    }
}

// Criar card de trending
function createTrendingCard(crypto) {
    const col = document.createElement('div');
    col.className = 'col-md-4 col-sm-6';
    
    col.innerHTML = `
        <div class="trending-card" onclick="loadCryptoData('${crypto.id}')">
            <div class="symbol">${crypto.symbol}</div>
            <div class="name">${crypto.name}</div>
        </div>
    `;
    
    return col;
}

// Buscar criptomoeda
async function searchCrypto() {
    const searchInput = document.getElementById('cryptoSearch');
    const coinId = searchInput.value.trim().toLowerCase();
    
    if (!coinId) {
        alert('Por favor, digite o nome ou símbolo de uma criptomoeda');
        return;
    }
    
    await loadCryptoData(coinId);
}

// Carregar dados da criptomoeda
async function loadCryptoData(coinId) {
    showLoading();
    currentCoinId = coinId;
    
    try {
        // Buscar informações básicas
        const infoResponse = await fetch(`${API_BASE}/crypto/${coinId}`);
        if (!infoResponse.ok) {
            throw new Error('Criptomoeda não encontrada');
        }
        const cryptoInfo = await infoResponse.json();
        
        // Buscar análise técnica
        const analysisResponse = await fetch(`${API_BASE}/analysis/${coinId}`);
        const analysis = analysisResponse.ok ? await analysisResponse.json() : null;
        
        // Buscar predição
        const predictionResponse = await fetch(`${API_BASE}/predict/${coinId}?days=7`);
        const prediction = predictionResponse.ok ? await predictionResponse.json() : null;
        
        // Buscar dados históricos
        const historicalResponse = await fetch(`${API_BASE}/historical/${coinId}?days=30`);
        const historical = historicalResponse.ok ? await historicalResponse.json() : null;
        
        // Renderizar dados
        renderCryptoInfo(cryptoInfo);
        if (analysis) renderTechnicalAnalysis(analysis);
        if (prediction) renderPrediction(prediction);
        if (historical) renderHistoricalChart(historical);
        
        // Scroll para conteúdo
        document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        alert(`Erro: ${error.message}`);
        console.error(error);
    } finally {
        hideLoading();
    }
}

// Renderizar informações básicas
function renderCryptoInfo(info) {
    const container = document.getElementById('mainContent');
    const changeClass = info.price_change_24h >= 0 ? 'positive' : 'negative';
    const changeIcon = info.price_change_24h >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
    
    container.innerHTML = `
        <div class="col-12 mb-4 fade-in">
            <div class="crypto-card">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h2 class="mb-3">
                            <i class="fab fa-bitcoin me-2"></i>
                            ${info.name} (${info.symbol})
                        </h2>
                        <div class="price">$${formatNumber(info.current_price)}</div>
                        <div class="change ${changeClass} mt-2">
                            <i class="fas ${changeIcon} me-1"></i>
                            ${info.price_change_24h >= 0 ? '+' : ''}${info.price_change_24h.toFixed(2)}%
                        </div>
                    </div>
                    <div class="col-md-4 text-md-end">
                        <div class="mb-2">
                            <small class="text-muted">Market Cap</small>
                            <div class="fw-bold">$${formatNumber(info.market_cap)}</div>
                        </div>
                        <div class="mb-2">
                            <small class="text-muted">Volume 24h</small>
                            <div class="fw-bold">$${formatNumber(info.total_volume)}</div>
                        </div>
                        <div>
                            <small class="text-muted">24h High/Low</small>
                            <div class="fw-bold">
                                $${formatNumber(info.high_24h)} / $${formatNumber(info.low_24h)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-12 fade-in">
            <div class="chart-container">
                <div class="chart-title">Preço Histórico (30 dias)</div>
                <canvas id="priceChart"></canvas>
            </div>
        </div>
    `;
}

// Renderizar análise técnica
function renderTechnicalAnalysis(analysis) {
    const container = document.getElementById('technicalAnalysis');
    const signalClass = analysis.signal.toLowerCase();
    
    container.innerHTML = `
        <div class="col-md-6 mb-3 fade-in">
            <div class="analysis-card">
                <h5><i class="fas fa-chart-line me-2"></i>Médias Móveis</h5>
                <div class="row">
                    <div class="col-6">
                        <div class="analysis-label">SMA 20</div>
                        <div class="analysis-value">$${formatNumber(analysis.sma_20)}</div>
                    </div>
                    <div class="col-6">
                        <div class="analysis-label">SMA 50</div>
                        <div class="analysis-value">$${formatNumber(analysis.sma_50)}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-3 fade-in">
            <div class="analysis-card">
                <h5><i class="fas fa-wave-square me-2"></i>Indicadores</h5>
                <div class="row">
                    <div class="col-6">
                        <div class="analysis-label">RSI</div>
                        <div class="analysis-value">${analysis.rsi}</div>
                    </div>
                    <div class="col-6">
                        <div class="analysis-label">MACD</div>
                        <div class="analysis-value">${analysis.macd.toFixed(2)}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3 fade-in">
            <div class="analysis-card">
                <h5><i class="fas fa-signal me-2"></i>Sinal</h5>
                <div class="signal-badge ${signalClass} mt-3">
                    ${analysis.signal.toUpperCase()}
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3 fade-in">
            <div class="analysis-card">
                <h5><i class="fas fa-arrow-trend-up me-2"></i>Tendência</h5>
                <div class="analysis-value mt-3">${analysis.trend.toUpperCase()}</div>
            </div>
        </div>
        <div class="col-md-4 mb-3 fade-in">
            <div class="analysis-card">
                <h5><i class="fas fa-chart-area me-2"></i>Suporte/Resistência</h5>
                <div class="mt-3">
                    <div class="analysis-label">Suporte</div>
                    <div class="analysis-value">$${formatNumber(analysis.support_level)}</div>
                    <div class="analysis-label mt-2">Resistência</div>
                    <div class="analysis-value">$${formatNumber(analysis.resistance_level)}</div>
                </div>
            </div>
        </div>
    `;
}

// Renderizar predição
function renderPrediction(prediction) {
    const container = document.getElementById('mlPredictions');
    const changeClass = prediction.predicted_change >= 0 ? 'positive' : 'negative';
    const changeIcon = prediction.predicted_change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
    const confidencePercent = (prediction.confidence * 100).toFixed(1);
    
    container.innerHTML = `
        <div class="col-md-8 mx-auto fade-in">
            <div class="prediction-card">
                <h3><i class="fas fa-brain me-2"></i>Predição para ${prediction.days_ahead} dias</h3>
                <div class="prediction-price">
                    $${formatNumber(prediction.predicted_price)}
                </div>
                <div class="prediction-change ${changeClass}">
                    <i class="fas ${changeIcon} me-1"></i>
                    ${prediction.predicted_change >= 0 ? '+' : ''}${prediction.predicted_change.toFixed(2)}%
                </div>
                <div class="mt-4">
                    <div class="d-flex justify-content-between mb-2">
                        <span>Confiança do Modelo</span>
                        <span><strong>${confidencePercent}%</strong></span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%">
                            ${confidencePercent}%
                        </div>
                    </div>
                </div>
                <div class="mt-4">
                    <small>Preço Atual: $${formatNumber(prediction.current_price)}</small><br>
                    <small>Modelo: ${prediction.model_info.type}</small>
                </div>
            </div>
        </div>
    `;
}

// Renderizar gráfico histórico
function renderHistoricalChart(historical) {
    const ctx = document.getElementById('priceChart');
    if (!ctx) return;
    
    const labels = historical.prices.map(p => {
        const date = new Date(p.timestamp);
        return date.toLocaleDateString('pt-BR');
    });
    
    const prices = historical.prices.map(p => p.price);
    
    if (priceChart) {
        priceChart.destroy();
    }
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Preço (USD)',
                data: prices,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

// Inicializar gráfico hero
function initializeHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;
    
    // Dados de exemplo para o hero
    const labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'];
    const data = [100, 120, 115, 140, 135, 160];
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Crescimento',
                data: data,
                borderColor: 'rgba(255, 255, 255, 0.8)',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: { color: 'rgba(255, 255, 255, 0.8)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    ticks: { color: 'rgba(255, 255, 255, 0.8)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Carregar dashboard completo
function loadDashboard() {
    document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
}

// Utilitários
function formatNumber(num) {
    if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    }
    return num.toFixed(2);
}

function showLoading() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

function hideLoading() {
    const modalElement = document.getElementById('loadingModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide();
    }
}

