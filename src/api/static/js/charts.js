// Chart.js configuration and management
let priceChart = null;
let featureChart = null;
let predictionHistoryChart = null;

// Initialize charts
function initializeCharts() {
    // Set Chart.js defaults
    Chart.defaults.color = '#a0a0a0';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
    Chart.defaults.backgroundColor = 'rgba(0, 210, 255, 0.1)';
    
    // Initialize price chart if canvas exists
    const priceCanvas = document.getElementById('priceChart');
    if (priceCanvas) {
        initializePriceChart();
    }
    
    // Initialize feature importance chart if canvas exists
    const featureCanvas = document.getElementById('featureChart');
    if (featureCanvas) {
        initializeFeatureChart();
    }
    
    // Initialize prediction history chart if canvas exists
    const predHistoryCanvas = document.getElementById('predictionHistoryChart');
    if (predHistoryCanvas) {
        initializePredictionHistoryChart();
    }
}

// Initialize price chart
function initializePriceChart() {
    const ctx = document.getElementById('priceChart');
    if (!ctx) return;
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Price (USD)',
                data: [],
                borderColor: '#00d2ff',
                backgroundColor: 'rgba(0, 210, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#00d2ff',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 26, 36, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a0a0',
                    borderColor: 'rgba(0, 210, 255, 0.3)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return new Date(context[0].label).toLocaleDateString();
                        },
                        label: function(context) {
                            return `Price: ${formatCurrency(context.parsed.y)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: {
                            day: 'MMM dd'
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#666666'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#666666',
                        callback: function(value) {
                            return formatCurrency(value, true);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    hoverRadius: 8
                }
            }
        }
    });
}

// Initialize feature importance chart
function initializeFeatureChart() {
    const ctx = document.getElementById('featureChart');
    if (!ctx) return;
    
    featureChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Price Lag 1', 'Volume 24h', 'Market Cap', 'Price Change 24h', 'RSI'],
            datasets: [{
                label: 'Importance',
                data: [0.35, 0.22, 0.18, 0.15, 0.10],
                backgroundColor: [
                    'rgba(0, 210, 255, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    '#00d2ff',
                    '#3b82f6',
                    '#f59e0b',
                    '#10b981',
                    '#ef4444'
                ],
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 36, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a0a0',
                    borderColor: 'rgba(0, 210, 255, 0.3)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `Importance: ${(context.parsed.y * 100).toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666666',
                        maxRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 0.4,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#666666',
                        callback: function(value) {
                            return `${(value * 100).toFixed(0)}%`;
                        }
                    }
                }
            }
        }
    });
}

// Initialize prediction history chart
function initializePredictionHistoryChart() {
    const ctx = document.getElementById('predictionHistoryChart');
    if (!ctx) return;
    
    predictionHistoryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Actual Price',
                    data: [],
                    borderColor: '#00d2ff',
                    backgroundColor: 'rgba(0, 210, 255, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6
                },
                {
                    label: 'Predicted Price',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#a0a0a0',
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 26, 36, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a0a0',
                    borderColor: 'rgba(0, 210, 255, 0.3)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        title: function(context) {
                            return new Date(context[0].label).toLocaleDateString();
                        },
                        label: function(context) {
                            return `${context.dataset.label}: ${formatCurrency(context.parsed.y)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        displayFormats: {
                            hour: 'MMM dd HH:mm'
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#666666'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#666666',
                        callback: function(value) {
                            return formatCurrency(value, true);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Update price chart with new data
function updatePriceChart(coinId, data) {
    if (!priceChart || !data || !data.prices) return;
    
    const labels = data.prices.map(item => new Date(item.timestamp));
    const prices = data.prices.map(item => item.price);
    
    priceChart.data.labels = labels;
    priceChart.data.datasets[0].data = prices;
    priceChart.update('none');
}

// Update feature importance chart
function updateFeatureChart(data) {
    if (!featureChart || !data || !data.feature_importance) return;
    
    const features = Object.keys(data.feature_importance);
    const importance = Object.values(data.feature_importance);
    
    featureChart.data.labels = features;
    featureChart.data.datasets[0].data = importance;
    featureChart.update('none');
}

// Update prediction history chart
function updatePredictionHistoryChart(actualData, predictionData) {
    if (!predictionHistoryChart) return;
    
    // Update with actual and predicted data
    if (actualData && actualData.prices) {
        const labels = actualData.prices.map(item => new Date(item.timestamp));
        const prices = actualData.prices.map(item => item.price);
        
        predictionHistoryChart.data.labels = labels;
        predictionHistoryChart.data.datasets[0].data = prices;
    }
    
    if (predictionData && predictionData.predictions) {
        const predLabels = predictionData.predictions.map(item => new Date(item.timestamp));
        const predPrices = predictionData.predictions.map(item => item.predicted_price);
        
        predictionHistoryChart.data.datasets[1].data = predPrices;
    }
    
    predictionHistoryChart.update('none');
}

// Destroy all charts
function destroyCharts() {
    if (priceChart) {
        priceChart.destroy();
        priceChart = null;
    }
    if (featureChart) {
        featureChart.destroy();
        featureChart = null;
    }
    if (predictionHistoryChart) {
        predictionHistoryChart.destroy();
        predictionHistoryChart = null;
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

// Export chart functions
window.ChartManager = {
    initializeCharts,
    updatePriceChart,
    updateFeatureChart,
    updatePredictionHistoryChart,
    destroyCharts
};