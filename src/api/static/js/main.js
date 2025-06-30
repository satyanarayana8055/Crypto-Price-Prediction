// Global variables
let currentCoin = 'bitcoin';
let chartInstances = {};

// Initialize the application
function initializeApp() {
    console.log('Initializing CryptoPredictAI Dashboard...');
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadInitialData();
    
    // Start real-time updates
    startRealTimeUpdates();
}

// Set up all event listeners
function setupEventListeners() {
    // Coin selector
    const coinSelects = document.querySelectorAll('#coinSelect');
    coinSelects.forEach(select => {
        select.addEventListener('change', handleCoinChange);
    });
    
    // Chart period buttons
    const chartBtns = document.querySelectorAll('.chart-btn');
    chartBtns.forEach(btn => {
        btn.addEventListener('click', handleChartPeriodChange);
    });
    
    // Navigation toggle for mobile
    const navToggle = document.querySelector('.nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', toggleNav);
    }
}

// Toggle mobile navigation
function toggleNav() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('show');
    }
}

// Handle coin selection change
function handleCoinChange(event) {
    const newCoin = event.target.value;
    if (newCoin !== currentCoin) {
        currentCoin = newCoin;
        console.log(`Switched to ${currentCoin}`);
        
        // Update all coin selects
        const coinSelects = document.querySelectorAll('#coinSelect');
        coinSelects.forEach(select => {
            if (select !== event.target) {
                select.value = newCoin;
            }
        });
        
        // Reload data for new coin
        loadCoinData(currentCoin);
    }
}

// Handle chart period change
function handleChartPeriodChange(event) {
    const period = event.target.dataset.period;
    const buttons = event.target.parentElement.querySelectorAll('.chart-btn');
    
    // Update active state
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update chart
    updatePriceChart(currentCoin, period);
}

// Load initial data
function loadInitialData() {
    loadCoinData(currentCoin);
    loadSupportedCoins();
}

// Load data for specific coin
async function loadCoinData(coinId) {
    try {
        // Show loading state
        showLoadingState();
        
        // Load current price data
        const priceData = await fetchCoinData(coinId);
        updatePriceDisplay(priceData);
        
        // Load historical data for chart
        const historicalData = await fetchHistoricalData(coinId, 30);
        updatePriceChart(coinId, historicalData);
        
        // Load prediction data
        const predictionData = await fetchPrediction(coinId);
        updatePredictionDisplay(predictionData);
        
        // Load model metrics
        const metricsData = await fetchModelMetrics(coinId);
        updateMetricsDisplay(metricsData);
        
        // Hide loading state
        hideLoadingState();
        
    } catch (error) {
        console.error('Error loading coin data:', error);
        showErrorMessage('Failed to load data. Please try again.');
        hideLoadingState();
    }
}

// Fetch current coin data
async function fetchCoinData(coinId) {
    const response = await fetch(`/api/data/${coinId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Fetch historical data
async function fetchHistoricalData(coinId, days = 30) {
    const response = await fetch(`/api/historical/${coinId}?days=${days}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Fetch prediction data
async function fetchPrediction(coinId) {
    const response = await fetch(`/api/predict/${coinId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Fetch model metrics
async function fetchModelMetrics(coinId) {
    const response = await fetch(`/api/model-metrics/${coinId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Load supported coins
async function loadSupportedCoins() {
    try {
        const response = await fetch('/api/coins');
        const coins = await response.json();
        updateCoinSelectors(coins);
    } catch (error) {
        console.error('Error loading supported coins:', error);
    }
}

// Update coin selectors with available coins
function updateCoinSelectors(coins) {
    const coinSelects = document.querySelectorAll('#coinSelect');
    coinSelects.forEach(select => {
        select.innerHTML = '';
        coins.forEach(coin => {
            const option = document.createElement('option');
            option.value = coin.id;
            option.textContent = `${coin.name} (${coin.symbol})`;
            if (coin.id === currentCoin) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    });
}

// Update price display
function updatePriceDisplay(data) {
    if (data.error) {
        console.error('Price data error:', data.error);
        return;
    }
    
    // Update current price
    const currentPriceEl = document.getElementById('currentPrice');
    if (currentPriceEl && data.price) {
        currentPriceEl.textContent = formatCurrency(data.price);
    }
    
    // Update price change
    const priceChangeEl = document.getElementById('priceChange');
    if (priceChangeEl && data.price_change_24h !== undefined) {
        const change = data.price_change_24h;
        const changePercent = (change / (data.price - change)) * 100;
        
        priceChangeEl.textContent = `${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`;
        priceChangeEl.className = `stat-change ${change >= 0 ? 'positive' : 'negative'}`;
    }
    
    // Update market cap
    const marketCapEl = document.getElementById('marketCap');
    if (marketCapEl && data.market_cap) {
        marketCapEl.textContent = formatCurrency(data.market_cap, true);
    }
    
    // Update 24h volume
    const volumeEl = document.getElementById('volume24h');
    if (volumeEl && data.volume) {
        volumeEl.textContent = formatCurrency(data.volume, true);
    }
}

// Update prediction display
function updatePredictionDisplay(data) {
    if (data.error) {
        console.error('Prediction data error:', data.error);
        return;
    }
    
    // Update predicted price
    const predictedPriceEl = document.getElementById('predictedPrice');
    if (predictedPriceEl && data.predicted_price) {
        predictedPriceEl.textContent = formatCurrency(data.predicted_price);
    }
    
    // Update prediction change
    const predictionChangeEl = document.getElementById('predictionChange');
    if (predictionChangeEl && data.price_change_percentage) {
        const change = data.price_change_percentage;
        predictionChangeEl.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
        predictionChangeEl.className = `stat-change ${change >= 0 ? 'positive' : 'negative'}`;
    }
}

// Update metrics display
function updateMetricsDisplay(data) {
    if (data.error) {
        console.error('Metrics data error:', data.error);
        return;
    }
    
    // Update accuracy
    const accuracyEl = document.getElementById('modelAccuracy');
    if (accuracyEl && data.accuracy) {
        accuracyEl.textContent = `${(data.accuracy * 100).toFixed(1)}%`;
    }
    
    // Update MAE
    const maeEl = document.getElementById('modelMAE');
    if (maeEl && data.mae) {
        maeEl.textContent = data.mae.toFixed(1);
    }
    
    // Update R² Score
    const r2El = document.getElementById('modelR2');
    if (r2El && data.r2_score) {
        r2El.textContent = data.r2_score.toFixed(2);
    }
    
    // Update MAPE
    const mapeEl = document.getElementById('modelMAPE');
    if (mapeEl && data.mape) {
        mapeEl.textContent = `${data.mape.toFixed(1)}%`;
    }
}

// Start real-time updates
function startRealTimeUpdates() {
    // Update every 30 seconds
    setInterval(() => {
        loadCoinData(currentCoin);
    }, 30000);
    
    console.log('Real-time updates started');
}

// Utility function to format currency
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

// Show loading state
function showLoadingState() {
    const elements = document.querySelectorAll('.stat-value, .metric-value');
    elements.forEach(el => {
        el.style.opacity = '0.6';
    });
}

// Hide loading state
function hideLoadingState() {
    const elements = document.querySelectorAll('.stat-value, .metric-value');
    elements.forEach(el => {
        el.style.opacity = '1';
    });
}

// Show error message
function showErrorMessage(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.innerHTML = `
        <i data-lucide="alert-circle"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--color-error);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
    
    // Reinitialize Lucide icons for the toast
    if (window.lucide) {
        lucide.createIcons();
    }
}

// Refresh metrics (called from dashboard)
function refreshMetrics() {
    console.log('Refreshing metrics...');
    loadCoinData(currentCoin);
}

// Add CSS for toast animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.CryptoApp = {
    initializeApp,
    loadCoinData,
    refreshMetrics,
    formatCurrency,
    currentCoin: () => currentCoin
};