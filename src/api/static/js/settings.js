// Settings page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeSettingsPage();
});

function initializeSettingsPage() {
    console.log('Initializing Settings Page...');
    
    // Load current settings
    loadCurrentSettings();
    
    // Set up event listeners
    setupSettingsEventListeners();
}

function setupSettingsEventListeners() {
    // Toggle switches
    const toggleInputs = document.querySelectorAll('.toggle-input');
    toggleInputs.forEach(input => {
        input.addEventListener('change', handleToggleChange);
    });
    
    // Select dropdowns
    const selects = document.querySelectorAll('.setting-select');
    selects.forEach(select => {
        select.addEventListener('change', handleSelectChange);
    });
    
    // Input fields
    const inputs = document.querySelectorAll('.setting-input');
    inputs.forEach(input => {
        input.addEventListener('change', handleInputChange);
    });
    
    // Checkbox groups
    const checkboxes = document.querySelectorAll('.checkbox-label input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });
}

function loadCurrentSettings() {
    // In a real implementation, this would fetch settings from the API
    console.log('Loading current settings...');
    
    // Sample settings data
    const settings = {
        autoRefresh: true,
        theme: 'dark',
        defaultCoin: 'bitcoin',
        autoRetrain: false,
        predictionFrequency: '30',
        modelValidation: '0.2',
        dataSource: 'coingecko',
        historicalDataRange: '90',
        dataBackup: true,
        emailNotifications: true,
        emailAddress: 'user@example.com',
        notificationTypes: {
            accuracyDrops: true,
            dataDrift: true,
            systemErrors: false,
            dailyReports: false
        },
        apiRateLimit: 60,
        requestTimeout: 10,
        retryAttempts: 3
    };
    
    // Apply settings to UI
    applySettingsToUI(settings);
}

function applySettingsToUI(settings) {
    // Toggle switches
    const autoRefreshToggle = document.querySelector('input[type="checkbox"]');
    if (autoRefreshToggle) {
        autoRefreshToggle.checked = settings.autoRefresh;
    }
    
    // Select dropdowns
    const themeSelect = document.querySelector('.setting-select');
    if (themeSelect) {
        themeSelect.value = settings.theme;
    }
    
    // Apply other settings...
    console.log('Settings applied to UI');
}

function handleToggleChange(event) {
    const setting = event.target.closest('.setting-item');
    const label = setting.querySelector('label').textContent;
    const value = event.target.checked;
    
    console.log(`${label} changed to: ${value}`);
    
    // Handle specific toggle changes
    if (label.includes('Auto Refresh')) {
        handleAutoRefreshChange(value);
    } else if (label.includes('Auto Retrain')) {
        handleAutoRetrainChange(value);
    } else if (label.includes('Data Backup')) {
        handleDataBackupChange(value);
    } else if (label.includes('Email Notifications')) {
        handleEmailNotificationsChange(value);
    }
    
    // Show success message
    showSuccessMessage(`${label} ${value ? 'enabled' : 'disabled'}`);
}

function handleSelectChange(event) {
    const setting = event.target.closest('.setting-item');
    const label = setting.querySelector('label').textContent;
    const value = event.target.value;
    
    console.log(`${label} changed to: ${value}`);
    
    // Handle specific select changes
    if (label.includes('Theme')) {
        handleThemeChange(value);
    } else if (label.includes('Default Coin')) {
        handleDefaultCoinChange(value);
    } else if (label.includes('Data Source')) {
        handleDataSourceChange(value);
    }
    
    // Show success message
    showSuccessMessage(`${label} updated to ${value}`);
}

function handleInputChange(event) {
    const setting = event.target.closest('.setting-item');
    const label = setting.querySelector('label').textContent;
    const value = event.target.value;
    
    console.log(`${label} changed to: ${value}`);
    
    // Validate input based on type
    if (event.target.type === 'email') {
        if (!isValidEmail(value)) {
            showErrorMessage('Please enter a valid email address');
            return;
        }
    } else if (event.target.type === 'number') {
        const min = parseInt(event.target.min);
        const max = parseInt(event.target.max);
        const numValue = parseInt(value);
        
        if (numValue < min || numValue > max) {
            showErrorMessage(`Value must be between ${min} and ${max}`);
            return;
        }
    }
    
    // Show success message
    showSuccessMessage(`${label} updated to ${value}`);
}

function handleCheckboxChange(event) {
    const label = event.target.parentElement.querySelector('.checkbox-text').textContent;
    const value = event.target.checked;
    
    console.log(`${label} notification ${value ? 'enabled' : 'disabled'}`);
    
    // Show success message
    showSuccessMessage(`${label} notifications ${value ? 'enabled' : 'disabled'}`);
}

// Specific setting handlers
function handleAutoRefreshChange(enabled) {
    if (enabled) {
        // Start auto-refresh
        console.log('Auto-refresh enabled');
    } else {
        // Stop auto-refresh
        console.log('Auto-refresh disabled');
    }
}

function handleAutoRetrainChange(enabled) {
    if (enabled) {
        console.log('Auto-retrain enabled');
        showInfoMessage('Models will automatically retrain when drift is detected');
    } else {
        console.log('Auto-retrain disabled');
    }
}

function handleDataBackupChange(enabled) {
    if (enabled) {
        console.log('Data backup enabled');
        showInfoMessage('Daily data backups will be created automatically');
    } else {
        console.log('Data backup disabled');
        showWarningMessage('Data will not be backed up automatically');
    }
}

function handleEmailNotificationsChange(enabled) {
    const emailField = document.querySelector('.setting-input[type="email"]');
    const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
    
    if (emailField) {
        emailField.disabled = !enabled;
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.disabled = !enabled;
    });
    
    if (enabled) {
        showInfoMessage('Email notifications enabled. Configure your preferences below.');
    } else {
        showInfoMessage('Email notifications disabled');
    }
}

function handleThemeChange(theme) {
    console.log(`Theme changed to: ${theme}`);
    
    // In a real implementation, this would apply the theme
    if (theme === 'light') {
        showInfoMessage('Light theme will be applied on next page load');
    } else if (theme === 'auto') {
        showInfoMessage('Theme will follow system preferences');
    }
}

function handleDefaultCoinChange(coin) {
    console.log(`Default coin changed to: ${coin}`);
    showInfoMessage(`${coin.charAt(0).toUpperCase() + coin.slice(1)} will be the default coin`);
}

function handleDataSourceChange(source) {
    console.log(`Data source changed to: ${source}`);
    
    if (source === 'coinmarketcap') {
        showInfoMessage('CoinMarketCap API will be used for data');
    } else if (source === 'binance') {
        showInfoMessage('Binance API will be used for data');
    } else {
        showInfoMessage('CoinGecko API will be used for data');
    }
}

function saveSettings() {
    console.log('Saving all settings...');
    
    // Show loading state
    const saveBtn = document.querySelector('.save-btn');
    if (saveBtn) {
        const originalText = saveBtn.innerHTML;
        saveBtn.innerHTML = '<i data-lucide="loader"></i> Saving...';
        saveBtn.disabled = true;
        
        // Reinitialize icons
        if (window.lucide) {
            lucide.createIcons();
        }
        
        // Simulate saving
        setTimeout(() => {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
            
            // Reinitialize icons
            if (window.lucide) {
                lucide.createIcons();
            }
            
            showSuccessMessage('Settings saved successfully');
        }, 2000);
    }
    
    // In real implementation, collect all settings and send to API
    const settingsData = collectAllSettings();
    console.log('Settings to save:', settingsData);
}

function resetSettings() {
    console.log('Resetting settings to defaults...');
    
    // Show confirmation dialog
    if (confirm('Are you sure you want to reset all settings to defaults? This action cannot be undone.')) {
        // Show loading state
        const resetBtn = document.querySelector('.reset-btn');
        if (resetBtn) {
            const originalText = resetBtn.innerHTML;
            resetBtn.innerHTML = '<i data-lucide="loader"></i> Resetting...';
            resetBtn.disabled = true;
            
            // Reinitialize icons
            if (window.lucide) {
                lucide.createIcons();
            }
            
            // Simulate reset
            setTimeout(() => {
                resetBtn.innerHTML = originalText;
                resetBtn.disabled = false;
                
                // Reinitialize icons
                if (window.lucide) {
                    lucide.createIcons();
                }
                
                // Reset UI to defaults
                resetUIToDefaults();
                showSuccessMessage('Settings reset to defaults');
            }, 2000);
        }
    }
}

function collectAllSettings() {
    const settings = {};
    
    // Collect toggle settings
    const toggles = document.querySelectorAll('.toggle-input');
    toggles.forEach(toggle => {
        const label = toggle.closest('.setting-item').querySelector('label').textContent;
        settings[label] = toggle.checked;
    });
    
    // Collect select settings
    const selects = document.querySelectorAll('.setting-select');
    selects.forEach(select => {
        const label = select.closest('.setting-item').querySelector('label').textContent;
        settings[label] = select.value;
    });
    
    // Collect input settings
    const inputs = document.querySelectorAll('.setting-input');
    inputs.forEach(input => {
        const label = input.closest('.setting-item').querySelector('label').textContent;
        settings[label] = input.value;
    });
    
    return settings;
}

function resetUIToDefaults() {
    // Reset all form elements to their default values
    const form = document.querySelector('.settings-container');
    if (form) {
        // Reset toggles
        const toggles = form.querySelectorAll('.toggle-input');
        toggles.forEach(toggle => {
            toggle.checked = false; // or default value
        });
        
        // Reset selects
        const selects = form.querySelectorAll('.setting-select');
        selects.forEach(select => {
            select.selectedIndex = 0;
        });
        
        // Reset inputs
        const inputs = form.querySelectorAll('.setting-input');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Reset checkboxes
        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
    }
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showSuccessMessage(message) {
    showToast(message, 'success');
}

function showErrorMessage(message) {
    showToast(message, 'error');
}

function showInfoMessage(message) {
    showToast(message, 'info');
}

function showWarningMessage(message) {
    showToast(message, 'warning');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
        success: 'check-circle',
        error: 'alert-circle',
        warning: 'alert-triangle',
        info: 'info'
    };
    
    const colors = {
        success: 'var(--color-success)',
        error: 'var(--color-error)',
        warning: 'var(--color-warning)',
        info: 'var(--color-primary)'
    };
    
    toast.innerHTML = `
        <i data-lucide="${icons[type]}"></i>
        <span>${message}</span>
    `;
    
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
        box-shadow: var(--shadow-lg);
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
    
    // Reinitialize Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
}

// Make functions available globally
window.saveSettings = saveSettings;
window.resetSettings = resetSettings;

// Add CSS for settings-specific components
const style = document.createElement('style');
style.textContent = `
    .settings-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .settings-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .settings-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .settings-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .card-header h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .card-icon {
        width: 20px;
        height: 20px;
        color: var(--color-primary);
    }
    
    .settings-content {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .setting-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .setting-info {
        flex: 1;
    }
    
    .setting-info label {
        display: block;
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .setting-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .setting-select,
    .setting-input {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 0.25rem;
        color: var(--text-primary);
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        min-width: 120px;
    }
    
    .setting-select:focus,
    .setting-input:focus {
        outline: none;
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.1);
    }
    
    .toggle-label {
        display: flex;
        align-items: center;
        cursor: pointer;
        position: relative;
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
    
    .toggle-input::after {
        content: '';
        position: absolute;
        top: 2px;
        left: 2px;
        width: 18px;
        height: 18px;
        background: white;
        border-radius: 50%;
        transition: transform 0.2s ease;
    }
    
    .toggle-input:checked::after {
        transform: translateX(20px);
    }
    
    .checkbox-group {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }
    
    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }
    
    .checkbox-label input[type="checkbox"] {
        width: 16px;
        height: 16px;
        accent-color: var(--color-primary);
    }
    
    .checkbox-text {
        font-size: 0.9rem;
        color: var(--text-primary);
    }
    
    .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border-color-light);
    }
    
    .info-item:last-child {
        border-bottom: none;
    }
    
    .info-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .info-value {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .settings-footer {
        display: flex;
        gap: 1rem;
        justify-content: center;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
    }
    
    .save-btn,
    .reset-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        font-size: 0.95rem;
    }
    
    .save-btn {
        background: var(--color-primary);
        color: white;
    }
    
    .save-btn:hover {
        background: var(--color-primary-dark);
        transform: translateY(-1px);
    }
    
    .save-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    .reset-btn {
        background: transparent;
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .reset-btn:hover {
        background: var(--bg-tertiary);
        border-color: var(--color-primary);
    }
    
    .reset-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
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
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @media (max-width: 768px) {
        .settings-grid {
            grid-template-columns: 1fr;
        }
        
        .setting-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.75rem;
        }
        
        .setting-select,
        .setting-input {
            width: 100%;
        }
        
        .settings-footer {
            flex-direction: column;
            align-items: center;
        }
        
        .save-btn,
        .reset-btn {
            width: 100%;
            max-width: 300px;
            justify-content: center;
        }
    }
`;
document.head.appendChild(style);