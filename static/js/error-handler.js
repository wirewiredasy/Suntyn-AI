
class ErrorHandler {
    constructor() {
        this.initializeErrorHandling();
    }

    initializeErrorHandling() {
        // Global error handler
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'javascript',
                message: event.message,
                filename: event.filename,
                line: event.lineno,
                column: event.colno,
                stack: event.error?.stack
            });
        });

        // Promise rejection handler
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'promise',
                message: event.reason?.message || 'Promise rejected',
                stack: event.reason?.stack
            });
        });

        // Network error handler
        this.setupNetworkErrorHandling();
    }

    handleError(errorInfo) {
        console.error('Error caught:', errorInfo);
        
        // Show user-friendly message
        this.showUserNotification('Something went wrong. Please try again.', 'error');
        
        // Log error for debugging
        this.logError(errorInfo);
    }

    setupNetworkErrorHandling() {
        // Override fetch to handle network errors
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch(...args);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response;
            } catch (error) {
                this.handleNetworkError(error);
                throw error;
            }
        };
    }

    handleNetworkError(error) {
        const message = error.message.includes('Failed to fetch') 
            ? 'Network error. Please check your connection.' 
            : 'Server error. Please try again later.';
        
        this.showUserNotification(message, 'error');
    }

    showUserNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 translate-x-full`;
        
        const bgColor = type === 'error' ? 'bg-red-500' : 
                       type === 'success' ? 'bg-green-500' : 
                       'bg-blue-500';
        
        notification.classList.add(bgColor, 'text-white');
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                <i data-lucide="${type === 'error' ? 'alert-circle' : type === 'success' ? 'check-circle' : 'info'}" class="w-5 h-5"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
        
        // Initialize lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    logError(errorInfo) {
        const errorLog = {
            ...errorInfo,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href,
            userId: window.tooloraAnalytics?.userId || 'anonymous'
        };
        
        // Store locally
        const errors = JSON.parse(localStorage.getItem('toolora_errors') || '[]');
        errors.push(errorLog);
        
        if (errors.length > 50) {
            errors.splice(0, errors.length - 50);
        }
        
        localStorage.setItem('toolora_errors', JSON.stringify(errors));
    }
}

// Initialize error handler
const errorHandler = new ErrorHandler();
window.errorHandler = errorHandler;
