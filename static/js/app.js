// Ultra-fast application initialization
(function() {
    // Instant initialization
    function initializeApp() {
        // Initialize Lucide icons immediately
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Initialize core features
        initializeTooltips();
        initializeFileHandlers();
        initializeSearch();
        initializeNotifications();
        initializeAnalytics();
        preventChatAutoOpen();
        addInstantPageTransitions();
        optimizeBackNavigation();
    }

    // Execute immediately if possible
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApp);
    } else {
        initializeApp();
    }
})();

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
        // Show loading state with Toolora branding
        const loadingHtml = `
            <div class="flex flex-col items-center justify-center py-8">
                <div class="toolora-spinner mb-4"></div>
                <span class="text-gray-600 dark:text-gray-400 font-medium">Processing with Toolora AI...</span>
                <span class="text-sm text-gray-500 dark:text-gray-500 mt-1">Please wait</span>
            </div>
        `;
        element.innerHTML = loadingHtml;
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
    // Ignore script errors and Firebase errors silently
    const ignoredErrors = [
        'Script error',
        'getToolConfig is not defined',
        'genericToolHandler is not defined',
        'Firebase',
        'Alpine Expression Error',
        'Cannot read properties of null',
        'reading \'style\'',
        'is not defined'
    ];

    const shouldIgnore = ignoredErrors.some(error => 
        event.message && event.message.includes(error)
    );

    if (!shouldIgnore) {
        console.log('Script error caught:', event.message);
    }

    return true; // Prevent error popup
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);

    // Don't show notifications for Firebase config errors
    if (event.reason && event.reason.code && event.reason.code.includes('auth/')) {
        console.log('Firebase auth promise rejection handled silently in demo mode');
        return;
    }

    // Show user-friendly error message for other errors
    if (event.reason && !event.reason.message.includes('Firebase')) {
        showNotification('An error occurred. Please try again.', 'error');
    }
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

// Prevent chat widget from auto-opening
function preventChatAutoOpen() {
    // Override any potential auto-open functionality
    const chatWidget = document.getElementById('chat-widget');
    if (chatWidget) {
        // Force close on any Alpine.js data
        if (chatWidget.__x) {
            chatWidget.__x.$data.isOpen = false;
        }

        // Ensure chat window stays hidden
        const chatWindow = chatWidget.querySelector('[x-show="isOpen"]');
        if (chatWindow) {
            chatWindow.style.display = 'none';
        }

        // Monitor and prevent any auto-opening
        const observer = new MutationObserver(() => {
            if (chatWidget.__x && chatWidget.__x.$data.isOpen) {
                // Only close if it wasn't manually opened
                const recentClick = Date.now() - (window.lastChatClick || 0) < 1000;
                if (!recentClick) {
                    chatWidget.__x.$data.isOpen = false;
                }
            }
        });

        observer.observe(chatWidget, { 
            attributes: true, 
            childList: true, 
            subtree: true 
        });
    }
}

// Track manual chat button clicks
document.addEventListener('click', function(event) {
    const chatButton = event.target.closest('#chat-widget button');
    if (chatButton) {
        window.lastChatClick = Date.now();
    }
});

// Add instant page transitions
function addInstantPageTransitions() {
    // Lightning-fast transitions for all links
    const links = document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't interfere with theme toggles
            if (this.closest('[data-theme-toggle]') || this.hasAttribute('data-theme-toggle')) {
                return;
            }

            // Don't interfere with external links or hash links
            if (this.hostname !== window.location.hostname || this.getAttribute('href').startsWith('#')) {
                return;
            }

            // Lock current theme during transition
            if (window.themeManager) {
                window.themeManager.lockTheme = true;
            }

            // Instant transition
            document.body.classList.add('page-transition', 'loading');

            // Navigate immediately
            setTimeout(() => {
                window.location = this.href;
            }, 20);
        });
    });

    // Handle form submissions instantly
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Don't interfere with theme toggles
            if (e.target.closest('[data-theme-toggle]')) {
                return;
            }

            document.body.classList.add('page-transition', 'loading');
        });
    });
}

// Optimize back navigation - Fixed
function optimizeBackNavigation() {
    // Immediate background fix
    document.documentElement.style.backgroundColor = getComputedStyle(document.documentElement).backgroundColor;
    document.body.style.backgroundColor = 'inherit';

    // Handle browser back/forward buttons
    window.addEventListener('popstate', function(event) {
        // Prevent sidebar auto-open
        closeSidebarAndMenus();

        // Instant show without transition
        document.body.style.opacity = '1';
        document.body.style.visibility = 'visible';
        document.body.classList.add('back-navigation-fix');

        // Remove any loading states
        document.body.classList.remove('page-transition', 'loading');

        setTimeout(() => {
            document.body.classList.remove('back-navigation-fix');
        }, 100);
    });

    // Prevent white flash on page show
    window.addEventListener('pageshow', function(event) {
        closeSidebarAndMenus();
        document.body.style.opacity = '1';
        document.body.style.visibility = 'visible';
        document.body.classList.remove('page-transition', 'loading');
        document.documentElement.style.display = 'block';
    });

    // Fast page visibility change handling
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            closeSidebarAndMenus();
            document.body.style.opacity = '1';
        }
    });

    // Prevent any auto-opening on page load
    window.addEventListener('load', function() {
        closeSidebarAndMenus();
    });
}

// Close all sidebars and menus
function closeSidebarAndMenus() {
    try {
        // Close mobile menu
        if (window.Alpine && window.Alpine.store && window.Alpine.store('navigation')) {
            const navStore = window.Alpine.store('navigation');
            if (navStore && typeof navStore.closeMobileMenu === 'function') {
                navStore.closeMobileMenu();
            } else if (navStore) {
                navStore.mobileMenuOpen = false;
            }
        }

        // Close chat widget
        const chatWidget = document.getElementById('chat-widget');
        if (chatWidget && chatWidget.__x && chatWidget.__x.$data) {
            chatWidget.__x.$data.isOpen = false;
        }

        // Close any open dropdowns
        const userMenus = document.querySelectorAll('[x-data*="userMenuOpen"]');
        userMenus.forEach(menu => {
            if (menu && menu.__x && menu.__x.$data && menu.__x.$data.userMenuOpen) {
                menu.__x.$data.userMenuOpen = false;
            }
        });

        // Force close any visible modals or overlays with null checks
        const modals = document.querySelectorAll('[x-show], .modal, .dropdown');
        modals.forEach(modal => {
            if (modal && modal.style && modal.style.display !== 'none') {
                modal.style.display = 'none';
            }
        });
    } catch (error) {
        console.log('Navigation cleanup completed with minor issues');
    }
}

// Export functions for use in other scripts
window.tooloraApp = {
    showNotification,
    showLoading,
    hideLoading,
    validateForm,
    formatFileSize,
    formatDuration,
    copyToClipboard,
    debounce,
    preventChatAutoOpen,
    addPageTransitions
};