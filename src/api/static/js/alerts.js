// Alerts page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeAlertsPage();
});

function initializeAlertsPage() {
    console.log('Initializing Alerts Page...');
    
    // Load initial alerts data
    loadAlertsData();
    
    // Set up event listeners
    setupAlertsEventListeners();
    
    // Set up auto-refresh
    setInterval(loadAlertsData, 30000); // Refresh every 30 seconds
}

function setupAlertsEventListeners() {
    // Filter buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', handleFilterChange);
    });
    
    // Alert action buttons
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('acknowledge')) {
            acknowledgeAlert(event.target);
        } else if (event.target.classList.contains('resolve')) {
            resolveAlert(event.target);
        }
    });
    
    // Configuration inputs
    const thresholdInputs = document.querySelectorAll('.threshold-input');
    thresholdInputs.forEach(input => {
        input.addEventListener('change', updateThreshold);
    });
    
    // Email toggle
    const emailToggle = document.querySelector('.toggle-input');
    if (emailToggle) {
        emailToggle.addEventListener('change', toggleEmailNotifications);
    }
    
    // Test email button
    const testBtn = document.querySelector('.test-btn');
    if (testBtn) {
        testBtn.addEventListener('click', sendTestEmail);
    }
}

function handleFilterChange(event) {
    const filter = event.target.dataset.filter;
    const buttons = event.target.parentElement.querySelectorAll('.filter-btn');
    
    // Update active state
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter alerts
    filterAlerts(filter);
}

function filterAlerts(filter) {
    const alertItems = document.querySelectorAll('.alert-item');
    
    alertItems.forEach(item => {
        if (filter === 'all') {
            item.style.display = 'flex';
        } else {
            const hasClass = item.classList.contains(filter);
            item.style.display = hasClass ? 'flex' : 'none';
        }
    });
}

async function loadAlertsData() {
    try {
        // Update alert stats
        updateAlertStats();
        
        // Load recent alerts
        loadRecentAlerts();
        
    } catch (error) {
        console.error('Error loading alerts data:', error);
    }
}

function updateAlertStats() {
    // Sample stats - in real implementation, fetch from API
    const stats = {
        activeAlerts: 3,
        triggeredToday: 7,
        emailsSent: 5,
        responseTime: '2.3s'
    };
    
    // Update the stats display
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length >= 4) {
        statCards[0].querySelector('.stat-value').textContent = stats.activeAlerts;
        statCards[1].querySelector('.stat-value').textContent = stats.triggeredToday;
        statCards[2].querySelector('.stat-value').textContent = stats.emailsSent;
        statCards[3].querySelector('.stat-value').textContent = stats.responseTime;
    }
}

function loadRecentAlerts() {
    const alertsList = document.getElementById('alertsList');
    if (!alertsList) return;
    
    // Sample alerts data
    const alerts = [
        {
            id: 1,
            type: 'high',
            icon: 'alert-circle',
            title: 'Model Accuracy Drop - Bitcoin',
            description: 'Accuracy dropped to 78%, below threshold of 80%',
            time: '15 minutes ago',
            status: 'active'
        },
        {
            id: 2,
            type: 'medium',
            icon: 'trending-down',
            title: 'Data Drift Detected - Ethereum',
            description: 'Volume feature shows significant drift (score: 0.45)',
            time: '1 hour ago',
            status: 'active'
        },
        {
            id: 3,
            type: 'low',
            icon: 'info',
            title: 'Scheduled Retraining - Bitcoin',
            description: 'Model retraining completed successfully',
            time: '3 hours ago',
            status: 'acknowledged'
        },
        {
            id: 4,
            type: 'medium',
            icon: 'zap',
            title: 'High Prediction Error - Cardano',
            description: 'Prediction error exceeded 15% threshold',
            time: '5 hours ago',
            status: 'resolved'
        }
    ];
    
    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.type} ${alert.status}" data-alert-id="${alert.id}">
            <div class="alert-icon">
                <i data-lucide="${alert.icon}"></i>
            </div>
            <div class="alert-content">
                <div class="alert-title">${alert.title}</div>
                <div class="alert-desc">${alert.description}</div>
                <div class="alert-time">${alert.time}</div>
            </div>
            <div class="alert-actions">
                ${alert.status === 'active' ? `
                    <button class="action-btn acknowledge">Acknowledge</button>
                    <button class="action-btn resolve">Resolve</button>
                ` : `
                    <span class="status-badge">${alert.status.charAt(0).toUpperCase() + alert.status.slice(1)}</span>
                `}
            </div>
        </div>
    `).join('');
    
    // Reinitialize Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
}

function acknowledgeAlert(button) {
    const alertItem = button.closest('.alert-item');
    const alertId = alertItem.dataset.alertId;
    
    console.log(`Acknowledging alert ${alertId}`);
    
    // Update UI
    alertItem.classList.add('acknowledged');
    const actionsDiv = alertItem.querySelector('.alert-actions');
    actionsDiv.innerHTML = '<span class="status-badge">Acknowledged</span>';
    
    // In real implementation, send API request
    showSuccessMessage('Alert acknowledged successfully');
}

function resolveAlert(button) {
    const alertItem = button.closest('.alert-item');
    const alertId = alertItem.dataset.alertId;
    
    console.log(`Resolving alert ${alertId}`);
    
    // Update UI
    alertItem.classList.add('resolved');
    alertItem.classList.remove('acknowledged');
    const actionsDiv = alertItem.querySelector('.alert-actions');
    actionsDiv.innerHTML = '<span class="status-badge">Resolved</span>';
    
    // In real implementation, send API request
    showSuccessMessage('Alert resolved successfully');
}

function updateThreshold(event) {
    const input = event.target;
    const value = input.value;
    const label = input.previousElementSibling.textContent;
    
    console.log(`Updated ${label} threshold to ${value}`);
    
    // In real implementation, send API request to update configuration
    showSuccessMessage(`${label} threshold updated to ${value}`);
}

function toggleEmailNotifications(event) {
    const enabled = event.target.checked;
    console.log(`Email notifications ${enabled ? 'enabled' : 'disabled'}`);
    
    // Enable/disable email input
    const emailField = document.querySelector('.email-field');
    if (emailField) {
        emailField.disabled = !enabled;
    }
    
    // In real implementation, send API request
    showSuccessMessage(`Email notifications ${enabled ? 'enabled' : 'disabled'}`);
}

function sendTestEmail() {
    const emailField = document.querySelector('.email-field');
    const email = emailField ? emailField.value : '';
    
    if (!email) {
        showErrorMessage('Please enter an email address first');
        return;
    }
    
    console.log(`Sending test email to ${email}`);
    
    // Show loading state
    const testBtn = document.querySelector('.test-btn');
    if (testBtn) {
        const originalText = testBtn.textContent;
        testBtn.textContent = 'Sending...';
        testBtn.disabled = true;
        
        // Simulate sending
        setTimeout(() => {
            testBtn.textContent = originalText;
            testBtn.disabled = false;
            showSuccessMessage('Test email sent successfully');
        }, 2000);
    }
}

function openAlertConfig() {
    const modal = document.getElementById('alertConfigModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeAlertConfig() {
    const modal = document.getElementById('alertConfigModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function saveAlert() {
    const form = document.getElementById('alertForm');
    if (!form) return;
    
    const formData = new FormData(form);
    const alertData = Object.fromEntries(formData);
    
    console.log('Saving new alert:', alertData);
    
    // In real implementation, send API request
    showSuccessMessage('Alert created successfully');
    closeAlertConfig();
    
    // Reload alerts
    loadRecentAlerts();
}

// Utility functions
function showSuccessMessage(message) {
    showToast(message, 'success');
}

function showErrorMessage(message) {
    showToast(message, 'error');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-circle' : 'info'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--color-success)' : type === 'error' ? 'var(--color-error)' : 'var(--color-primary)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
    
    // Reinitialize Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
}

// Make functions available globally
window.openAlertConfig = openAlertConfig;
window.closeAlertConfig = closeAlertConfig;
window.saveAlert = saveAlert;

// Add CSS for alerts-specific components
const style = document.createElement('style');
style.textContent = `
    .alert-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .alert-item:hover {
        background: var(--bg-card-hover);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    .alert-item.high {
        border-left: 4px solid var(--color-error);
    }
    
    .alert-item.medium {
        border-left: 4px solid var(--color-warning);
    }
    
    .alert-item.low {
        border-left: 4px solid var(--color-success);
    }
    
    .alert-item.acknowledged {
        opacity: 0.7;
    }
    
    .alert-item.resolved {
        opacity: 0.5;
    }
    
    .alert-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .alert-item.high .alert-icon {
        background: rgba(239, 68, 68, 0.2);
        color: var(--color-error);
    }
    
    .alert-item.medium .alert-icon {
        background: rgba(245, 158, 11, 0.2);
        color: var(--color-warning);
    }
    
    .alert-item.low .alert-icon {
        background: rgba(16, 185, 129, 0.2);
        color: var(--color-success);
    }
    
    .alert-content {
        flex: 1;
    }
    
    .alert-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .alert-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .alert-time {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    .alert-actions {
        display: flex;
        gap: 0.5rem;
        flex-shrink: 0;
    }
    
    .action-btn {
        background: transparent;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .action-btn:hover {
        background: var(--color-primary);
        border-color: var(--color-primary);
        color: white;
    }
    
    .action-btn.acknowledge:hover {
        background: var(--color-warning);
        border-color: var(--color-warning);
    }
    
    .action-btn.resolve:hover {
        background: var(--color-success);
        border-color: var(--color-success);
    }
    
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
        background: var(--bg-secondary);
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
    }
    
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1000;
        align-items: center;
        justify-content: center;
    }
    
    .modal-content {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        width: 90%;
        max-width: 500px;
        max-height: 90vh;
        overflow-y: auto;
    }
    
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .modal-header h3 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .modal-close {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 0.25rem;
        transition: all 0.2s ease;
    }
    
    .modal-close:hover {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }
    
    .modal-body {
        padding: 1.5rem;
    }
    
    .modal-footer {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        padding: 1.5rem;
        border-top: 1px solid var(--border-color);
    }
    
    .form-group {
        margin-bottom: 1rem;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .form-select,
    .form-input {
        width: 100%;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 0.25rem;
        color: var(--text-primary);
        padding: 0.75rem;
        font-size: 0.9rem;
    }
    
    .form-select:focus,
    .form-input:focus {
        outline: none;
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.1);
    }
    
    .btn-primary,
    .btn-secondary {
        padding: 0.75rem 1.5rem;
        border-radius: 0.25rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
    }
    
    .btn-primary {
        background: var(--color-primary);
        color: white;
    }
    
    .btn-primary:hover {
        background: var(--color-primary-dark);
    }
    
    .btn-secondary {
        background: transparent;
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .btn-secondary:hover {
        background: var(--bg-tertiary);
    }
    
    .toggle-label {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        cursor: pointer;
    }
    
    .toggle-input {
        position: relative;
        width: 44px;
        height: 24px;
        appearance: none;
        background: var(--bg-tertiary);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .toggle-input:checked {
        background: var(--color-primary);
        border-color: var(--color-primary);
    }
    
    .toggle-slider {
        position: absolute;
        top: 2px;
        left: 2px;
        width: 18px;
        height: 18px;
        background: white;
        border-radius: 50%;
        transition: transform 0.2s ease;
        pointer-events: none;
    }
    
    .toggle-input:checked + .toggle-slider {
        transform: translateX(20px);
    }
`;
document.head.appendChild(style);