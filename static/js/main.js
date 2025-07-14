/**
 * Main JavaScript for Toolora AI
 * Handles page transitions, animations, and global functionality
 */

// Global app object
window.ToolaraApp = {
    init: function() {
        this.setupPageTransitions();
        this.setupDarkMode();
        this.setupChatWidget();
        this.setupToolClicks();
        this.setupAnimations();
        this.setupFormHandlers();
    },

    setupPageTransitions: function() {
        // Add smooth page transitions
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (link && link.href && link.href.startsWith(window.location.origin)) {
                // Add loading animation if needed
                if (link.href !== window.location.href) {
                    document.body.style.opacity = '0.9';
                    setTimeout(() => {
                        document.body.style.opacity = '1';
                    }, 200);
                }
            }
        });
    },

    setupDarkMode: function() {
        // Dark mode is already handled by Alpine.js
        // This is just for additional features
        const darkModeToggle = document.querySelector('[data-toggle="dark-mode"]');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', function() {
                document.documentElement.classList.toggle('dark');
            });
        }
    },

    setupChatWidget: function() {
        // Chat widget functionality
        window.chatWidget = () => ({
            isOpen: false,
            messages: [],
            newMessage: '',
            
            init() {
                this.messages = [
                    {
                        id: 1,
                        sender: 'bot',
                        text: 'Hello! How can I help you today?',
                        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                    }
                ];
            },
            
            toggleChat() {
                this.isOpen = !this.isOpen;
                if (this.isOpen) {
                    this.$nextTick(() => {
                        const input = this.$refs.messageInput;
                        if (input) input.focus();
                    });
                }
            },
            
            sendMessage() {
                if (this.newMessage.trim()) {
                    this.messages.push({
                        id: Date.now(),
                        sender: 'user',
                        text: this.newMessage,
                        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                    });
                    
                    // Auto-reply (demo)
                    setTimeout(() => {
                        this.messages.push({
                            id: Date.now() + 1,
                            sender: 'bot',
                            text: 'Thank you for your message! Our team will get back to you soon.',
                            time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                        });
                    }, 1000);
                    
                    this.newMessage = '';
                }
            }
        });
    },

    setupToolClicks: function() {
        // Handle tool card clicks
        document.addEventListener('click', function(e) {
            const toolCard = e.target.closest('.tool-card');
            if (toolCard) {
                const toolName = toolCard.dataset.tool;
                const toolCategory = toolCard.dataset.category;
                
                // Analytics tracking
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'tool_click', {
                        tool_name: toolName,
                        tool_category: toolCategory
                    });
                }
                
                // Console log for debugging
                console.log('Tool used:', toolName);
                
                // Add click animation
                toolCard.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    toolCard.style.transform = '';
                }, 150);
            }
        });

        // Handle "Use Tool" button clicks
        document.addEventListener('click', function(e) {
            const useToolBtn = e.target.closest('.use-tool-btn');
            if (useToolBtn) {
                e.preventDefault();
                const toolName = useToolBtn.dataset.tool;
                
                // Add loading state
                useToolBtn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin mr-2"></i>Loading...';
                
                // Navigate to tool
                setTimeout(() => {
                    window.location.href = `/tools/${toolName}`;
                }, 500);
            }
        });
    },

    setupAnimations: function() {
        // Setup intersection observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        // Observe elements with animation classes
        document.querySelectorAll('[class*="animate-"]').forEach(el => {
            observer.observe(el);
        });
    },

    setupFormHandlers: function() {
        // Handle form submissions
        document.addEventListener('submit', function(e) {
            const form = e.target;
            if (form.classList.contains('tool-form')) {
                e.preventDefault();
                
                // Add loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin mr-2"></i>Processing...';
                    submitBtn.disabled = true;
                }
                
                // Process form (this would be replaced with actual form handling)
                setTimeout(() => {
                    if (submitBtn) {
                        submitBtn.innerHTML = 'Process Files';
                        submitBtn.disabled = false;
                    }
                }, 2000);
            }
        });
    }
};

// Analytics functions
window.trackPageView = function(page) {
    console.log('Page view:', page);
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            page_path: page
        });
    }
};

window.trackEvent = function(eventName, parameters) {
    console.log('Event:', eventName, parameters);
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, parameters);
    }
};

// Page transition function (to replace the missing addPageTransitions)
window.addPageTransitions = function() {
    console.log('Page transitions initialized');
    ToolaraApp.setupPageTransitions();
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    ToolaraApp.init();
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// Export for global access
window.ToolaraApp = ToolaraApp;