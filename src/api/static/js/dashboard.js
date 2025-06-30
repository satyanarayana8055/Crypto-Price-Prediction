// Dashboard-specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    console.log('Initializing Dashboard...');
    
    // Initialize charts
    if (window.ChartManager) {
        window.ChartManager.initializeCharts();
    }
    
    // Load initial dashboard data
    loadDashboardData();
    
    // Set up auto-refresh
    setInterval(loadDashboardData, 30000); // Refresh every 30 seconds
}

async function loadDashboardData() {
    const currentCoin = window.CryptoApp ? window.CryptoApp.currentCoin() : 'bitcoin';
    
    try {
        // Load current data
        const [coinData, historicalData, predictionData, metricsData] = await Promise.all([
            fetch(`/api/data/${currentCoin}`).then(r => r.json()),
            fetch(`/api/historical/${currentCoin}?days=30`).then(r => r.json()),
            fetch(`/api/predict/${currentCoin}`).then(r => r.json()),
            fetch(`/api/model-metrics/${currentCoin}`).then(r => r.json())
        ]);
        
        // Update displays
        updateDashboardStats(coinData, predictionData);
        updateDashboardChart(historicalData);
        updateDashboardMetrics(metricsData);
        updateActivityFeed();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateDashboardStats(coinData, predictionData) {
    // Update current price
    const currentPriceEl = document.getElementById('currentPrice');
    if (currentPriceEl && coinData.price) {
        currentPriceEl.textContent = formatCurrency(coinData.price);
    }
    
    // Update price change
    const priceChangeEl = document.getElementById('priceChange');
    if (priceChangeEl && coinData.price_change_24h !== undefined) {
        const change = coinData.price_change_24h;
        const changePercent = (change / (coinData.price - change)) * 100;
        
        priceChangeEl.textContent = `${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`;
        priceChangeEl.className = `stat-change ${change >= 0 ? 'positive' : 'negative'}`;
    }
    
    // Update market cap
    const marketCapEl = document.getElementById('marketCap');
    if (marketCapEl && coinData.market_cap) {
        marketCapEl.textContent = formatCurrency(coinData.market_cap, true);
    }
    
    // Update 24h volume
    const volumeEl = document.getElementById('volume24h');
    if (volumeEl && coinData.volume) {
        volumeEl.textContent = formatCurrency(coinData.volume, true);
    }
    
    // Update prediction
    const predictedPriceEl = document.getElementById('predictedPrice');
    if (predictedPriceEl && predictionData.predicted_price) {
        predictedPriceEl.textContent = formatCurrency(predictionData.predicted_price);
    }
    
    const predictionChangeEl = document.getElementById('predictionChange');
    if (predictionChangeEl && predictionData.price_change_percentage) {
        const change = predictionData.price_change_percentage;
        predictionChangeEl.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
        predictionChangeEl.className = `stat-change ${change >= 0 ? 'positive' : 'negative'}`;
    }
}

function updateDashboardChart(historicalData) {
    if (window.ChartManager && historicalData.prices) {
        window.ChartManager.updatePriceChart('bitcoin', historicalData);
    }
}

function updateDashboardMetrics(metricsData) {
    // Update accuracy
    const accuracyEl = document.getElementById('modelAccuracy');
    if (accuracyEl && metricsData.accuracy) {
        accuracyEl.textContent = `${(metricsData.accuracy * 100).toFixed(1)}%`;
    }
    
    // Update MAE
    const maeEl = document.getElementById('modelMAE');
    if (maeEl && metricsData.mae) {
        maeEl.textContent = metricsData.mae.toFixed(1);
    }
    
    // Update R² Score
    const r2El = document.getElementById('modelR2');
    if (r2El && metricsData.r2_score) {
        r2El.textContent = metricsData.r2_score.toFixed(2);
    }
    
    // Update MAPE
    const mapeEl = document.getElementById('modelMAPE');
    if (mapeEl && metricsData.mape) {
        mapeEl.textContent = `${metricsData.mape.toFixed(1)}%`;
    }
}

function updateActivityFeed() {
    const activityList = document.getElementById('activityList');
    if (!activityList) return;
    
    // Generate some sample activity items
    const activities = [
        {
            icon: 'check-circle',
            iconClass: 'success',
            title: 'Model Update Completed',
            time: '2 minutes ago'
        },
        {
            icon: 'info',
            iconClass: 'info',
            title: 'New prediction generated',
            time: '15 minutes ago'
        },
        {
            icon: 'alert-triangle',
            iconClass: 'warning',
            title: 'Data drift detected',
            time: '1 hour ago'
        }
    ];
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon ${activity.iconClass}">
                <i data-lucide="${activity.icon}"></i>
            </div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        </div>
    `).join('');
    
    // Reinitialize Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
}

function refreshMetrics() {
    console.log('Refreshing metrics...');
    loadDashboardData();
}

// Utility function to format currency (if not available globally)
function formatCurrency(value, short = false) {
    if (value === null || value === undefined) return '$0.00';
    
    if (short && value >= 1e9) {
        return `$${(value / 1e9).toFixed(2)}B`;
    } else if (short && value >= 1e6) {
        return `$${(value / 1e6).toFixed(2)}M`;
    } else if (short && value >= 1e3) {
        return `$${(value / 1e3).toFixed(2)}K`;
    }
    
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: value < 1 ? 4 : 2,
        maximumFractionDigits: value < 1 ? 4 : 2
    }).format(value);
}