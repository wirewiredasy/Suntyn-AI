/**
 * Main JavaScript for Toolora AI
 * Handles page transitions, animations, and global functionality
 */

// Enhanced Global app object with SPA features
window.ToolaraApp = {
    isNavigating: false,

    init: function() {
        this.setupSPANavigation();
        this.setupInstantPageLoad();
        this.setupDarkMode();
        this.setupChatWidget();
        this.setupToolClicks();
        this.setupAnimations();
        this.setupFormHandlers();
        this.optimizePerformance();
    },

    setupSPANavigation: function() {
        // Enhanced SPA navigation with better loading states
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && link.href && link.href.startsWith(window.location.origin) && !link.target) {
                const href = link.href;

                // Skip if same page
                if (href === window.location.href) return;

                // Skip external links
                if (link.hostname !== window.location.hostname) return;

                // Skip if already navigating
                if (this.isNavigating) return;

                e.preventDefault();
                this.navigateToPage(href);
            }
        });

        // Prefetch critical pages on hover
        document.addEventListener('mouseover', (e) => {
            const link = e.target.closest('a[href^="/"]');
            if (link && !link.dataset.prefetched) {
                this.prefetchPage(link.href);
                link.dataset.prefetched = 'true';
            }
        });
    },

    navigateToPage: function(url) {
        if (this.isNavigating) return;

        this.isNavigating = true;

        // Create smooth navigation overlay
        this.createNavOverlay();

        // Enhanced transition with dark background preservation
        document.body.style.opacity = '0.95';
        document.body.style.transform = 'translateY(-2px)';
        document.body.classList.add('page-transition', 'loading');

        // Preserve background color during transition
        const currentBg = getComputedStyle(document.body).backgroundColor;
        document.body.style.backgroundColor = currentBg;

        // Navigate with minimal delay for smooth transition
        setTimeout(() => {
            window.location.href = url;
        }, 50);

        // Reset state
        setTimeout(() => {
            this.isNavigating = false;
            document.body.classList.remove('page-transition', 'loading');
        }, 100);
    },

    prefetchPage: function(url) {
        // Prefetch pages for faster navigation
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);

        // Also prefetch as DNS lookup
        const dns = document.createElement('link');
        dns.rel = 'dns-prefetch';
        dns.href = url;
        document.head.appendChild(dns);
    },

    createNavOverlay: function() {
        // Remove existing overlay
        const existingOverlay = document.querySelector('.nav-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }

        // Create new overlay
        const overlay = document.createElement('div');
        overlay.className = 'nav-overlay';
        document.body.appendChild(overlay);

        // Remove after animation
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 800);
    },

    setupInstantPageLoad: function() {
        // Ultra-fast page load system
        document.addEventListener('DOMContentLoaded', () => {
            // Instant visibility
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.classList.add('loaded');

            // Preload critical pages
            this.preloadCriticalPages();
        });

        // Enhanced back navigation with smooth animation
        window.addEventListener('pageshow', (e) => {
            // Immediate visibility with proper background
            const isDark = document.documentElement.classList.contains('dark');
            document.body.style.backgroundColor = isDark ? '#111827' : '#f9fafb';
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.transform = 'none';
            document.body.classList.remove('page-transition', 'loading');
            document.body.classList.add('loaded', 'back-nav-smooth');

            // Force close any open menus
            if (window.Alpine && window.Alpine.store('navigation')) {
                window.Alpine.store('navigation').mobileMenuOpen = false;
            }

            // Re-initialize icons
            if (typeof lucide !== 'undefined') {
                requestAnimationFrame(() => lucide.createIcons());
            }

            // Remove animation class after animation
            setTimeout(() => {
                document.body.classList.remove('back-nav-smooth');
            }, 200);
        });

        // Handle visibility change smoothly
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                document.body.style.opacity = '1';
                document.body.classList.add('loaded');
            }
        });
    },

    addRippleEffect: function(element, event) {
        // Add ripple effect to clicked element
        element.classList.add('clicked');

        // Remove the class after animation
        setTimeout(() => {
            element.classList.remove('clicked');
        }, 600);
    },

    preloadCriticalPages: function() {
        const criticalPages = ['/tools/', '/about', '/contact'];
        criticalPages.forEach(page => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = page;
            document.head.appendChild(link);
        });
    },

    optimizePerformance: function() {
        // Debounce resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                // Handle resize
            }, 100);
        });

        // Optimize scroll events
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                // Handle scroll
            }, 16); // 60fps
        }, { passive: true });
    },

    setupDarkMode: function() {
        // Dark mode toggle functionality
        const darkModeToggle = document.querySelector('[x-on\\:click="darkMode = !darkMode"]');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', function() {
                document.documentElement.classList.toggle('dark');
            });
        }
    },

    setupMobileMenu: function() {
        // Fix mobile menu functionality
        document.addEventListener('alpine:init', () => {
            Alpine.store('navigation', {
                mobileMenuOpen: false,
                toggleMobileMenu() {
                    this.mobileMenuOpen = !this.mobileMenuOpen;
                }
            });
        });
    },

    setupChatWidget: function() {
        // Lazy load chat widget for better performance
        setTimeout(() => {
            window.chatWidget = () => ({
                isOpen: false,
                messages: [],
                newMessage: '',
                initialized: false,

                init() {
                    if (!this.initialized) {
                        this.messages = [
                            {
                                id: 1,
                                sender: 'bot',
                                text: 'Hello! How can I help you today?',
                                time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                            }
                        ];
                        this.initialized = true;
                    }
                },

                toggleChat() {
                    this.isOpen = !this.isOpen;

                    // Initialize on first open
                    if (this.isOpen && !this.initialized) {
                        this.init();
                    }

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

                        const userMessage = this.newMessage;
                        this.newMessage = '';

                        // Auto-reply with slight delay
                        setTimeout(() => {
                            this.messages.push({
                                id: Date.now() + 1,
                                sender: 'bot',
                                text: 'Thank you for your message! Our team will get back to you soon.',
                                time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                            });

                            // Auto-scroll to bottom
                            this.$nextTick(() => {
                                const chatMessages = document.getElementById('chat-messages');
                                if (chatMessages) {
                                    chatMessages.scrollTop = chatMessages.scrollHeight;
                                }
                            });
                        }, 800);
                    }
                }
            });
        }, 2000); // Load chat after 2 seconds
    },

    setupToolClicks: function() {
        // Handle tool card clicks with smooth animations
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

                // Enhanced click animation with ripple
                ToolaraApp.addRippleEffect(toolCard, e);

                // Smooth scale animation
                toolCard.style.transform = 'translateY(-2px) scale(0.98) translateZ(0)';

                setTimeout(() => {
                    toolCard.style.transform = '';
                }, 200);
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