/**
 * Ultra-Smooth Navigation System for Toolora AI
 * Eliminates white flash and provides buttery smooth animations
 */

class UltraSmoothNavigation {
    constructor() {
        this.isTransitioning = false;
        this.init();
    }

    init() {
        this.setupInstantLoading();
        this.setupSmoothNavigation();
        this.setupBackNavigation();
        this.setupPerformanceOptimizations();
    }

    setupInstantLoading() {
        // Detect slow connection
        const isSlowConnection = navigator.connection && 
                               (navigator.connection.effectiveType === 'slow-2g' || 
                                navigator.connection.effectiveType === '2g' ||
                                navigator.connection.downlink < 1);

        // Mobile and slow connection optimizations
        const isMobile = window.innerWidth <= 768 || /Mobi|Android/i.test(navigator.userAgent);

        const transitionDuration = isSlowConnection ? '0.05s' : (isMobile ? '0.1s' : '0.15s');

        // Immediate anti-flash system with adaptive timing
        const style = document.createElement('style');
        style.textContent = `
            html, body {
                background-color: ${document.documentElement.classList.contains('dark') ? '#111827' : '#f9fafb'} !important;
                visibility: visible !important;
                transition: opacity ${transitionDuration} ease, background-color ${transitionDuration} ease !important;
            }
            body {
                opacity: 0 !important;
            }
            body.loaded {
                opacity: 1 !important;
            }
        `;
        document.head.appendChild(style);

        // Force body visibility after minimal delay
        requestAnimationFrame(() => {
            document.body.style.visibility = 'visible';
            document.body.classList.add('loaded');
        });
    }

    setupSmoothNavigation() {
        // Intercept all navigation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');

            // Skip external links and hash links
            if (!href.startsWith('/') || href.startsWith('#')) return;

            // Skip if already transitioning
            if (this.isTransitioning) return;

            e.preventDefault();
            this.smoothNavigate(href);
        });
    }

    smoothNavigate(url) {
        this.isTransitioning = true;

        // Create smooth transition overlay
        this.createTransitionOverlay();

        // Minimal transition effect
        document.body.style.transform = 'translateY(-1px)';
        document.body.style.opacity = '0.98';
        document.body.style.transition = 'all 0.1s ease';

        // Navigate immediately
        requestAnimationFrame(() => {
            window.location.href = url;
        });

        // Reset state
        setTimeout(() => {
            this.isTransitioning = false;
        }, 100);
    }

    createTransitionOverlay() {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            z-index: 10000;
            animation: progressBar 0.3s ease-out;
        `;

        document.body.appendChild(overlay);

        // Remove after animation
        setTimeout(() => overlay.remove(), 300);
    }

    setupBackNavigation() {
        // Handle browser back/forward
        window.addEventListener('pageshow', (event) => {
            // Force immediate visibility
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.transform = 'none';
            document.body.style.transition = 'none';

            // Close any open menus
            this.closeAllMenus();

            // Add smooth back animation
            if (event.persisted) {
                document.body.classList.add('back-nav-smooth');
                setTimeout(() => {
                    document.body.classList.remove('back-nav-smooth');
                }, 200);
            }
        });

        // Handle popstate
        window.addEventListener('popstate', () => {
            this.closeAllMenus();
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
        });
    }

    closeAllMenus() {
        // Close mobile menu
        if (window.Alpine && window.Alpine.store) {
            const nav = window.Alpine.store('navigation');
            if (nav) nav.mobileMenuOpen = false;
        }

        // Close chat widget
        const chatWidget = document.getElementById('chat-widget');
        if (chatWidget && chatWidget.__x) {
            chatWidget.__x.$data.isOpen = false;
        }

        // Close any dropdowns
        document.querySelectorAll('[x-show]').forEach(el => {
            if (el.__x && el.__x.$data.isOpen !== undefined) {
                el.__x.$data.isOpen = false;
            }
        });
    }

    setupPerformanceOptimizations() {
        // Add CSS for animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes progressBar {
                0% { width: 0%; }
                100% { width: 100%; opacity: 0; }
            }

            .back-nav-smooth {
                animation: smoothBackNav 0.2s ease-out;
            }

            @keyframes smoothBackNav {
                from { opacity: 0.95; transform: translateY(-2px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Prevent any flash during transitions */
            body.transitioning {
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);

        // Preload next pages
        this.preloadPages(['/tools/', '/about', '/contact']);
    }

    preloadPages(urls) {
        urls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = url;
            document.head.appendChild(link);
        });
    }
}

// Initialize immediately
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.ultraSmoothNav = new UltraSmoothNavigation();
    });
} else {
    window.ultraSmoothNav = new UltraSmoothNavigation();
}

// Export for global access
window.UltraSmoothNavigation = UltraSmoothNavigation;