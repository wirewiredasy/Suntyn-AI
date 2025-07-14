// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize file handlers
    initializeFileHandlers();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize notification system
    initializeNotifications();
    
    // Initialize analytics
    initializeAnalytics();
});

// Tooltip initialization
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const text = event.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip absolute z-50 px-2 py-1 text-sm bg-gray-900 text-white rounded shadow-lg';
    tooltip.textContent = text;
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    event.target._tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target._tooltip) {
        document.body.removeChild(event.target._tooltip);
        delete event.target._tooltip;
    }
}

// File handling utilities
function initializeFileHandlers() {
    // Add drag and drop functionality to all drop zones
    const dropZones = document.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', handleDrop);
    });
}

function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function handleDragEnter(event) {
    event.preventDefault();
    event.target.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    if (!event.target.contains(event.relatedTarget)) {
        event.target.classList.remove('dragover');
    }
}

function handleDrop(event) {
    event.preventDefault();
    event.target.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        // Trigger file input change event
        const fileInput = event.target.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    }
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(handleSearch, 300));
    });
}

function handleSearch(event) {
    const query = event.target.value.toLowerCase();
    const target = event.target.getAttribute('data-search');
    const items = document.querySelectorAll(target);
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDuration(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hrs > 0) {
        return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'absolute';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        } catch (error) {
            document.body.removeChild(textArea);
            return Promise.reject(error);
        }
    }
}

// Notification system
function initializeNotifications() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notifications')) {
        const container = document.createElement('div');
        container.id = 'notifications';
        container.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notifications');
    const notification = document.createElement('div');
    
    const colors = {
        info: 'bg-blue-600',
        success: 'bg-green-600',
        warning: 'bg-yellow-600',
        error: 'bg-red-600'
    };
    
    const icons = {
        info: 'info',
        success: 'check-circle',
        warning: 'alert-triangle',
        error: 'alert-circle'
    };
    
    notification.className = `toast flex items-center space-x-3 ${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg max-w-sm`;
    notification.innerHTML = `
        <i data-lucide="${icons[type]}" class="w-5 h-5"></i>
        <span class="flex-1">${message}</span>
        <button onclick="this.parentElement.remove()" class="text-white hover:text-gray-200">
            <i data-lucide="x" class="w-4 h-4"></i>
        </button>
    `;
    
    container.appendChild(notification);
    
    // Re-initialize icons for the new notification
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Auto-remove notification
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.add('fade-out');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, duration);
    }
}

// Loading states
function showLoading(element, text = 'Loading...') {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        element.innerHTML = `
            <div class="flex items-center justify-center space-x-2">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span>${text}</span>
            </div>
        `;
        element.disabled = true;
    }
}

function hideLoading(element, originalText = 'Submit') {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// Form validation
function validateForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(input);
        }
        
        // Email validation
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                showFieldError(input, 'Please enter a valid email address');
                isValid = false;
            }
        }
        
        // Password validation
        if (input.type === 'password' && input.value) {
            if (input.value.length < 6) {
                showFieldError(input, 'Password must be at least 6 characters long');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

function showFieldError(input, message) {
    clearFieldError(input);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error text-red-500 text-sm mt-1';
    errorElement.textContent = message;
    
    input.parentElement.appendChild(errorElement);
    input.classList.add('border-red-500');
}

function clearFieldError(input) {
    const errorElement = input.parentElement.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
    input.classList.remove('border-red-500');
}

// Analytics
function initializeAnalytics() {
    // Track page views
    trackPageView();
    
    // Track tool usage
    trackToolUsage();
    
    // Track user interactions
    trackUserInteractions();
}

function trackPageView() {
    const page = window.location.pathname;
    console.log('Page view:', page);
    
    // Send to analytics service
    // This would typically send to Google Analytics, Mixpanel, etc.
}

function trackToolUsage() {
    // Track when tools are used
    const toolButtons = document.querySelectorAll('[data-tool]');
    toolButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const toolName = event.target.getAttribute('data-tool');
            console.log('Tool used:', toolName);
        });
    });
}

function trackUserInteractions() {
    // Track button clicks
    const buttons = document.querySelectorAll('button[data-track]');
    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            const action = event.target.getAttribute('data-track');
            console.log('User interaction:', action);
        });
    });
}

// Progressive Web App functionality
function initializePWA() {
    // Service worker registration
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered:', registration);
            })
            .catch(error => {
                console.log('SW registration failed:', error);
            });
    }
    
    // Install prompt
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (event) => {
        event.preventDefault();
        deferredPrompt = event;
        
        // Show install button
        const installButton = document.getElementById('install-button');
        if (installButton) {
            installButton.style.display = 'block';
            installButton.addEventListener('click', () => {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    }
                    deferredPrompt = null;
                });
            });
        }
    });
}

// Performance monitoring
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', () => {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log('Page load time:', loadTime + 'ms');
    });
    
    // Monitor resource loading
    const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            if (entry.duration > 1000) {
                console.log('Slow resource:', entry.name, entry.duration + 'ms');
            }
        });
    });
    
    observer.observe({entryTypes: ['resource']});
}

// Error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    
    // Show user-friendly error message
    showNotification('An error occurred. Please try again.', 'error');
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Show user-friendly error message
    showNotification('An error occurred. Please try again.', 'error');
});

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + K for search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('[data-modal]');
        modals.forEach(modal => {
            if (modal.style.display !== 'none') {
                modal.style.display = 'none';
            }
        });
    }
});

// Export functions for use in other scripts
window.tooloraApp = {
    showNotification,
    showLoading,
    hideLoading,
    validateForm,
    formatFileSize,
    formatDuration,
    copyToClipboard,
    debounce
};
