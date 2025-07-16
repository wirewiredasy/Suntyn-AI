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
        this.setupMobileSidebar();
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
                },
                closeMobileMenu() {
                    this.mobileMenuOpen = false;
                }
            });
        });

        // Add mobile menu event handlers
        document.addEventListener('click', (e) => {
            const mobileToggle = e.target.closest('[data-mobile-toggle]');
            if (mobileToggle) {
                e.preventDefault();
                window.dispatchEvent(new CustomEvent('toggle-mobile-menu'));
            }
        });

        // Close mobile menu on navigation
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('a[href]');
            if (navLink && navLink.closest('.mobile-menu')) {
                setTimeout(() => {
                    window.dispatchEvent(new CustomEvent('close-mobile-menu'));
                }, 100);
            }
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


    setupMobileSidebar: function() {
        // Enhanced mobile sidebar functionality with smooth animations
        document.addEventListener('alpine:init', () => {
            Alpine.store('navigation', {
                mobileMenuOpen: false,
                
                toggleMobileMenu() {
                    this.mobileMenuOpen = !this.mobileMenuOpen;
                    
                    // Enhanced body scroll prevention
                    if (this.mobileMenuOpen) {
                        document.body.style.overflow = 'hidden';
                        document.documentElement.style.overflow = 'hidden';
                        // Add blur effect to main content
                        const mainContent = document.querySelector('main');
                        if (mainContent) {
                            mainContent.style.filter = 'blur(2px)';
                            mainContent.style.transition = 'filter 0.3s ease';
                        }
                    } else {
                        document.body.style.overflow = '';
                        document.documentElement.style.overflow = '';
                        // Remove blur effect
                        const mainContent = document.querySelector('main');
                        if (mainContent) {
                            mainContent.style.filter = '';
                        }
                    }
                },
                
                closeMobileMenu() {
                    this.mobileMenuOpen = false;
                    document.body.style.overflow = '';
                    document.documentElement.style.overflow = '';
                    
                    // Remove blur effect
                    const mainContent = document.querySelector('main');
                    if (mainContent) {
                        mainContent.style.filter = '';
                    }
                }
            });
        });

        // Enhanced smooth scroll handling for header
        this.setupSmoothHeaderScroll();

        // Enhanced swipe to close functionality
        let startX = 0;
        let currentX = 0;
        let isSwipe = false;
        let sidebarPanel = null;

        document.addEventListener('touchstart', (e) => {
            if (window.Alpine && window.Alpine.store('navigation').mobileMenuOpen) {
                startX = e.touches[0].clientX;
                isSwipe = true;
                sidebarPanel = document.querySelector('.mobile-sidebar-panel');
            }
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!isSwipe || !sidebarPanel) return;
            
            currentX = e.touches[0].clientX;
            const diffX = startX - currentX;
            
            // Live swipe feedback
            if (diffX > 0) {
                const percentage = Math.min(diffX / 200, 1);
                sidebarPanel.style.transform = `translateX(-${percentage * 100}%)`;
                sidebarPanel.style.opacity = 1 - (percentage * 0.5);
            }
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            if (!isSwipe || !sidebarPanel) return;
            
            const diffX = startX - currentX;
            
            // Swipe left to close (threshold: 80px)
            if (diffX > 80 && window.Alpine && window.Alpine.store('navigation').mobileMenuOpen) {
                window.Alpine.store('navigation').closeMobileMenu();
            } else {
                // Snap back if swipe wasn't enough
                sidebarPanel.style.transform = '';
                sidebarPanel.style.opacity = '';
            }
            
            isSwipe = false;
            sidebarPanel = null;
        }, { passive: true });

        // Close sidebar on route change with animation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && link.closest('.mobile-sidebar-content')) {
                // Add click ripple effect
                this.addRippleEffect(link, e);
                
                setTimeout(() => {
                    if (window.Alpine && window.Alpine.store('navigation')) {
                        window.Alpine.store('navigation').closeMobileMenu();
                    }
                }, 150);
            }
        });
    },

    setupSmoothHeaderScroll: function() {
        let lastScrollY = window.scrollY;
        let ticking = false;
        const header = document.querySelector('.sticky-header');
        
        if (!header) return;

        function updateHeader() {
            const currentScrollY = window.scrollY;
            
            // Add/remove scrolled class based on scroll position
            if (currentScrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            // Hide/show header based on scroll direction
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                // Scrolling down & past threshold - hide header
                header.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up or at top - show header
                header.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
            ticking = false;
        }

        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateHeader);
                ticking = true;
            }
        }

        // Use passive scroll listener for better performance
        window.addEventListener('scroll', requestTick, { passive: true });
        
        // Show header when mouse moves to top
        document.addEventListener('mousemove', (e) => {
            if (e.clientY < 60) {
                header.style.transform = 'translateY(0)';
            }
        });
    },


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

        // Initialize popular tools animations
        this.initPopularToolsAnimations();
    },

    initPopularToolsAnimations: function() {
        const popularToolCards = document.querySelectorAll('.popular-tool-card');
        
        // Add stagger animation on page load
        popularToolCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0) scale(1)';
            }, index * 100);
        });

        // Add hover effects
        popularToolCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.03)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
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