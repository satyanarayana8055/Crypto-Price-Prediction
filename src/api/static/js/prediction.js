// Prediction page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializePredictionPage();
});

function initializePredictionPage() {
    console.log('Initializing Prediction Page...');
    
    // Initialize charts
    if (window.ChartManager) {
        window.ChartManager.initializeCharts();
    }
    
    // Load initial prediction data
    loadPredictionData();
    
    // Set up event listeners
    setupPredictionEventListeners();
}

function setupPredictionEventListeners() {
    // Coin selector
    const coinSelect = document.getElementById('coinSelect');
    if (coinSelect) {
        coinSelect.addEventListener('change', handleCoinChange);
    }
    
    // History period buttons
    const historyBtns = document.querySelectorAll('.history-btn');
    historyBtns.forEach(btn => {
        btn.addEventListener('click', handleHistoryPeriodChange);
    });
}

function handleCoinChange(event) {
    const newCoin = event.target.value;
    console.log(`Switched to ${newCoin} for predictions`);
    loadPredictionData(newCoin);
}

function handleHistoryPeriodChange(event) {
    const period = event.target.dataset.period;
    const buttons = event.target.parentElement.querySelectorAll('.history-btn');
    
    // Update active state
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update prediction history chart
    loadPredictionHistory(period);
}

async function loadPredictionData(coinId = 'bitcoin') {
    try {
        // Show loading state
        showLoadingState();
        
        // Load prediction data
        const [predictionData, metricsData, currentData] = await Promise.all([
            fetch(`/api/predict/${coinId}`).then(r => r.json()),
            fetch(`/api/model-metrics/${coinId}`).then(r => r.json()),
            fetch(`/api/data/${coinId}`).then(r => r.json())
        ]);
        
        // Update displays
        updatePredictionDisplay(predictionData, currentData);
        updateModelInfo(metricsData);
        updateFeatureImportance(metricsData);
        updateMetricsCards(metricsData);
        
        // Load prediction history
        loadPredictionHistory('24h');
        
        // Hide loading state
        hideLoadingState();
        
    } catch (error) {
        console.error('Error loading prediction data:', error);
        showErrorMessage('Failed to load prediction data');
        hideLoadingState();
    }
}

function updatePredictionDisplay(predictionData, currentData) {
    if (predictionData.error || currentData.error) {
        console.error('Prediction or current data error');
        return;
    }
    
    // Update current price
    const currentPriceEl = document.getElementById('currentPricePred');
    if (currentPriceEl && currentData.price) {
        currentPriceEl.textContent = formatCurrency(currentData.price);
    }
    
    // Update predicted price
    const predictedPriceEl = document.getElementById('predictedPricePred');
    if (predictedPriceEl && predictionData.predicted_price) {
        predictedPriceEl.textContent = formatCurrency(predictionData.predicted_price);
    }
    
    // Update change amount and percentage
    const changeAmountEl = document.getElementById('changeAmount');
    const changePercentageEl = document.getElementById('changePercentage');
    
    if (changeAmountEl && changePercentageEl && predictionData.price_change !== undefined) {
        const change = predictionData.price_change;
        const changePercent = predictionData.price_change_percentage;
        
        changeAmountEl.textContent = `${change >= 0 ? '+' : ''}${formatCurrency(Math.abs(change))}`;
        changePercentageEl.textContent = `${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`;
        
        // Update colors
        const colorClass = change >= 0 ? 'positive' : 'negative';
        changeAmountEl.className = `change-amount ${colorClass}`;
        changePercentageEl.className = `change-percentage ${colorClass}`;
        
        // Update arrow direction
        const arrowEl = document.getElementById('predictionArrow');
        if (arrowEl) {
            arrowEl.setAttribute('data-lucide', change >= 0 ? 'trending-up' : 'trending-down');
            if (window.lucide) {
                lucide.createIcons();
            }
        }
    }
    
    // Update confidence
    const confidenceEl = document.getElementById('confidenceValue');
    if (confidenceEl && predictionData.confidence) {
        confidenceEl.textContent = `${predictionData.confidence.toFixed(0)}%`;
        
        // Update confidence badge color
        const badge = document.getElementById('confidenceBadge');
        if (badge) {
            const confidence = predictionData.confidence;
            if (confidence >= 80) {
                badge.style.background = 'rgba(16, 185, 129, 0.2)';
                badge.style.borderColor = 'rgba(16, 185, 129, 0.3)';
            } else if (confidence >= 60) {
                badge.style.background = 'rgba(245, 158, 11, 0.2)';
                badge.style.borderColor = 'rgba(245, 158, 11, 0.3)';
            } else {
                badge.style.background = 'rgba(239, 68, 68, 0.2)';
                badge.style.borderColor = 'rgba(239, 68, 68, 0.3)';
            }
        }
    }
}

function updateModelInfo(metricsData) {
    if (metricsData.error) return;
    
    // Update training samples
    const trainingSamplesEl = document.getElementById('trainingSamples');
    if (trainingSamplesEl && metricsData.training_samples) {
        trainingSamplesEl.textContent = metricsData.training_samples.toLocaleString();
    }
    
    // Update last updated
    const lastUpdatedEl = document.getElementById('lastUpdated');
    if (lastUpdatedEl && metricsData.last_updated) {
        const lastUpdated = new Date(metricsData.last_updated);
        const now = new Date();
        const diffHours = Math.floor((now - lastUpdated) / (1000 * 60 * 60));
        lastUpdatedEl.textContent = `${diffHours} hours ago`;
    }
}

function updateFeatureImportance(metricsData) {
    if (metricsData.error || !metricsData.feature_importance) return;
    
    if (window.ChartManager) {
        window.ChartManager.updateFeatureChart(metricsData);
    }
}

function updateMetricsCards(metricsData) {
    if (metricsData.error) return;
    
    // Update accuracy
    const accuracyEl = document.getElementById('accuracyMetric');
    if (accuracyEl && metricsData.accuracy) {
        accuracyEl.textContent = `${(metricsData.accuracy * 100).toFixed(1)}%`;
    }
    
    // Update MSE
    const mseEl = document.getElementById('mseMetric');
    if (mseEl && metricsData.mse) {
        mseEl.textContent = metricsData.mse.toFixed(1);
    }
    
    // Update MAE
    const maeEl = document.getElementById('maeMetric');
    if (maeEl && metricsData.mae) {
        maeEl.textContent = metricsData.mae.toFixed(1);
    }
    
    // Update MAPE
    const mapeEl = document.getElementById('mapeMetric');
    if (mapeEl && metricsData.mape) {
        mapeEl.textContent = `${metricsData.mape.toFixed(1)}%`;
    }
}

async function loadPredictionHistory(period) {
    try {
        const coinId = document.getElementById('coinSelect')?.value || 'bitcoin';
        
        // Generate sample prediction history data
        const now = new Date();
        const hours = period === '24h' ? 24 : period === '7d' ? 168 : 720;
        
        const actualData = {
            prices: []
        };
        
        const predictionData = {
            predictions: []
        };
        
        // Generate sample data
        for (let i = hours; i >= 0; i--) {
            const timestamp = new Date(now.getTime() - i * 60 * 60 * 1000);
            const basePrice = 45000 + Math.sin(i / 10) * 2000;
            const noise = (Math.random() - 0.5) * 1000;
            
            actualData.prices.push({
                timestamp: timestamp,
                price: basePrice + noise
            });
            
            predictionData.predictions.push({
                timestamp: timestamp,
                predicted_price: basePrice + noise + (Math.random() - 0.5) * 500
            });
        }
        
        // Update chart
        if (window.ChartManager) {
            window.ChartManager.updatePredictionHistoryChart(actualData, predictionData);
        }
        
    } catch (error) {
        console.error('Error loading prediction history:', error);
    }
}

function generatePrediction() {
    console.log('Generating new prediction...');
    
    // Show loading state on button
    const generateBtn = document.querySelector('.generate-btn');
    if (generateBtn) {
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<i data-lucide="loader"></i> Generating...';
        generateBtn.disabled = true;
        
        // Reinitialize icons
        if (window.lucide) {
            lucide.createIcons();
        }
        
        // Simulate prediction generation
        setTimeout(() => {
            loadPredictionData();
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
            
            // Reinitialize icons
            if (window.lucide) {
                lucide.createIcons();
            }
        }, 2000);
    }
}

// Utility functions
function showLoadingState() {
    const elements = document.querySelectorAll('.metric-value, .change-amount, .change-percentage');
    elements.forEach(el => {
        el.style.opacity = '0.6';
    });
}

function hideLoadingState() {
    const elements = document.querySelectorAll('.metric-value, .change-amount, .change-percentage');
    elements.forEach(el => {
        el.style.opacity = '1';
    });
}

function showErrorMessage(message) {
    console.error(message);
    // Could implement toast notification here
}

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

// Make generatePrediction available globally
window.generatePrediction = generatePrediction;