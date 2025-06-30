// Data Drift page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeDataDriftPage();
});

function initializeDataDriftPage() {
    console.log('Initializing Data Drift Page...');
    
    // Load initial drift data
    loadDriftData();
    
    // Set up event listeners
    setupDriftEventListeners();
    
    // Set up auto-refresh
    setInterval(loadDriftData, 60000); // Refresh every minute
}

function setupDriftEventListeners() {
    // Coin selector
    const coinSelect = document.getElementById('coinSelect');
    if (coinSelect) {
        coinSelect.addEventListener('change', handleCoinChange);
    }
}

function handleCoinChange(event) {
    const newCoin = event.target.value;
    console.log(`Switched to ${newCoin} for drift monitoring`);
    loadDriftData(newCoin);
}

async function loadDriftData(coinId = 'bitcoin') {
    try {
        // Show loading state
        showLoadingState();
        
        // Update drift status cards
        updateDriftStatusCards();
        
        // Load drift report
        loadDriftReport(coinId);
        
        // Update feature drift table
        updateFeatureDriftTable();
        
        // Hide loading state
        hideLoadingState();
        
    } catch (error) {
        console.error('Error loading drift data:', error);
        showErrorMessage('Failed to load drift data');
        hideLoadingState();
    }
}

function updateDriftStatusCards() {
    // Update overall drift score
    const overallScoreEl = document.getElementById('overallScore');
    if (overallScoreEl) {
        const score = 0.25; // Sample score
        const scoreValue = overallScoreEl.querySelector('.score-value');
        const scoreStatus = overallScoreEl.querySelector('.score-status');
        
        if (scoreValue) scoreValue.textContent = score.toFixed(2);
        
        if (scoreStatus) {
            if (score < 0.3) {
                scoreStatus.textContent = 'Good';
                scoreStatus.className = 'score-status good';
            } else if (score < 0.5) {
                scoreStatus.textContent = 'Warning';
                scoreStatus.className = 'score-status warning';
            } else {
                scoreStatus.textContent = 'Critical';
                scoreStatus.className = 'score-status critical';
            }
        }
    }
    
    // Update drifted features count
    const driftedFeaturesEl = document.getElementById('driftedFeatures');
    if (driftedFeaturesEl) {
        driftedFeaturesEl.textContent = '2';
    }
    
    // Update last check time
    const lastCheckEl = document.getElementById('lastCheck');
    if (lastCheckEl) {
        lastCheckEl.textContent = '2 hours ago';
    }
}

async function loadDriftReport(coinId) {
    const reportContainer = document.querySelector('.drift-report-container');
    const loadingSpinner = document.getElementById('reportLoading');
    const driftIframe = document.getElementById('driftReport');
    
    if (!reportContainer || !loadingSpinner || !driftIframe) return;
    
    try {
        // Show loading
        loadingSpinner.style.display = 'flex';
        driftIframe.style.display = 'none';
        
        // Try to load drift report
        const response = await fetch(`/api/drift/${coinId}`);
        
        if (response.ok) {
            const htmlContent = await response.text();
            
            // Create a blob URL for the HTML content
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            
            driftIframe.src = url;
            driftIframe.onload = () => {
                loadingSpinner.style.display = 'none';
                driftIframe.style.display = 'block';
            };
        } else {
            // Show placeholder if no report available
            showDriftReportPlaceholder();
        }
        
    } catch (error) {
        console.error('Error loading drift report:', error);
        showDriftReportPlaceholder();
    }
}

function showDriftReportPlaceholder() {
    const reportContainer = document.querySelector('.drift-report-container');
    const loadingSpinner = document.getElementById('reportLoading');
    const driftIframe = document.getElementById('driftReport');
    
    if (reportContainer && loadingSpinner && driftIframe) {
        loadingSpinner.style.display = 'none';
        driftIframe.style.display = 'none';
        
        // Create placeholder
        const placeholder = document.createElement('div');
        placeholder.className = 'drift-report-placeholder';
        placeholder.innerHTML = `
            <div class="placeholder-content">
                <i data-lucide="file-text" style="width: 48px; height: 48px; color: var(--text-secondary); margin-bottom: 1rem;"></i>
                <h4>No Drift Report Available</h4>
                <p>Drift report will be generated after the next data analysis cycle.</p>
                <button class="btn-primary" onclick="generateDriftReport()">
                    <i data-lucide="refresh-cw"></i>
                    Generate Report
                </button>
            </div>
        `;
        
        placeholder.style.cssText = `
            display: flex;
            align-items: center;
            justify-content: center;
            height: 400px;
            background: var(--bg-secondary);
            border: 2px dashed var(--border-color);
            border-radius: var(--radius-lg);
            text-align: center;
        `;
        
        // Clear existing placeholder
        const existingPlaceholder = reportContainer.querySelector('.drift-report-placeholder');
        if (existingPlaceholder) {
            existingPlaceholder.remove();
        }
        
        reportContainer.appendChild(placeholder);
        
        // Reinitialize icons
        if (window.lucide) {
            lucide.createIcons();
        }
    }
}

function updateFeatureDriftTable() {
    const tableBody = document.getElementById('featureDriftTable');
    if (!tableBody) return;
    
    // Sample drift data
    const driftData = [
        {
            feature: 'price_lag_1',
            score: 0.15,
            status: 'good',
            lastChange: '2 hours ago'
        },
        {
            feature: 'volume_24h',
            score: 0.35,
            status: 'warning',
            lastChange: '1 hour ago'
        },
        {
            feature: 'market_cap',
            score: 0.12,
            status: 'good',
            lastChange: '3 hours ago'
        },
        {
            feature: 'price_change_24h',
            score: 0.28,
            status: 'warning',
            lastChange: '45 minutes ago'
        },
        {
            feature: 'rsi',
            score: 0.08,
            status: 'good',
            lastChange: '4 hours ago'
        }
    ];
    
    tableBody.innerHTML = driftData.map(item => {
        const scoreClass = item.score < 0.2 ? 'low' : item.score < 0.4 ? 'medium' : 'high';
        const statusClass = item.status;
        
        return `
            <tr>
                <td>${item.feature}</td>
                <td><span class="score-badge ${scoreClass}">${item.score.toFixed(2)}</span></td>
                <td><span class="status-badge ${statusClass}">${item.status.charAt(0).toUpperCase() + item.status.slice(1)}</span></td>
                <td>${item.lastChange}</td>
                <td><button class="action-btn" onclick="viewFeatureDetails('${item.feature}')">View Details</button></td>
            </tr>
        `;
    }).join('');
}

function refreshDriftReport() {
    console.log('Refreshing drift report...');
    const coinId = document.getElementById('coinSelect')?.value || 'bitcoin';
    loadDriftReport(coinId);
}

function downloadReport() {
    console.log('Downloading drift report...');
    // Implement download functionality
    showInfoMessage('Download functionality will be implemented');
}

function generateDriftReport() {
    console.log('Generating new drift report...');
    
    // Show loading state
    const placeholder = document.querySelector('.drift-report-placeholder');
    if (placeholder) {
        placeholder.innerHTML = `
            <div class="placeholder-content">
                <i data-lucide="loader" style="width: 48px; height: 48px; color: var(--color-primary); margin-bottom: 1rem; animation: spin 1s linear infinite;"></i>
                <h4>Generating Drift Report</h4>
                <p>This may take a few moments...</p>
            </div>
        `;
        
        // Reinitialize icons
        if (window.lucide) {
            lucide.createIcons();
        }
        
        // Simulate report generation
        setTimeout(() => {
            const coinId = document.getElementById('coinSelect')?.value || 'bitcoin';
            loadDriftReport(coinId);
        }, 3000);
    }
}

function viewFeatureDetails(feature) {
    console.log(`Viewing details for feature: ${feature}`);
    showInfoMessage(`Feature details for ${feature} will be implemented`);
}

// Utility functions
function showLoadingState() {
    const elements = document.querySelectorAll('.score-value, .count-value');
    elements.forEach(el => {
        el.style.opacity = '0.6';
    });
}

function hideLoadingState() {
    const elements = document.querySelectorAll('.score-value, .count-value');
    elements.forEach(el => {
        el.style.opacity = '1';
    });
}

function showErrorMessage(message) {
    console.error(message);
    // Could implement toast notification here
}

function showInfoMessage(message) {
    console.info(message);
    // Could implement toast notification here
}

// Make functions available globally
window.refreshDriftReport = refreshDriftReport;
window.downloadReport = downloadReport;
window.generateDriftReport = generateDriftReport;
window.viewFeatureDetails = viewFeatureDetails;

// Add CSS for drift-specific components
const style = document.createElement('style');
style.textContent = `
    .score-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .score-badge.low {
        background: rgba(16, 185, 129, 0.2);
        color: var(--color-success);
    }
    
    .score-badge.medium {
        background: rgba(245, 158, 11, 0.2);
        color: var(--color-warning);
    }
    
    .score-badge.high {
        background: rgba(239, 68, 68, 0.2);
        color: var(--color-error);
    }
    
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: capitalize;
    }
    
    .status-badge.good {
        background: rgba(16, 185, 129, 0.2);
        color: var(--color-success);
    }
    
    .status-badge.warning {
        background: rgba(245, 158, 11, 0.2);
        color: var(--color-warning);
    }
    
    .status-badge.critical {
        background: rgba(239, 68, 68, 0.2);
        color: var(--color-error);
    }
    
    .drift-iframe {
        width: 100%;
        height: 600px;
        border: none;
        border-radius: var(--radius-md);
        background: white;
    }
    
    .drift-table {
        width: 100%;
        border-collapse: collapse;
        background: var(--bg-card);
        border-radius: var(--radius-md);
        overflow: hidden;
    }
    
    .drift-table th,
    .drift-table td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    
    .drift-table th {
        background: var(--bg-secondary);
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    .drift-table tr:hover {
        background: var(--bg-card-hover);
    }
    
    .action-btn {
        background: transparent;
        border: 1px solid var(--border-color);
        color: var(--color-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .action-btn:hover {
        background: var(--color-primary);
        color: white;
    }
    
    .placeholder-content h4 {
        margin: 0 0 0.5rem 0;
        color: var(--text-primary);
    }
    
    .placeholder-content p {
        margin: 0 0 1.5rem 0;
        color: var(--text-secondary);
    }
`;
document.head.appendChild(style);