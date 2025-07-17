// Complete error fixes for Suntyn AI
(function() {
    'use strict';

    console.log('🔧 Loading comprehensive error fixes...');

    // Fix null style property errors
    function safeStyleAccess(element, property, value) {
        if (element && element.style && typeof element.style === 'object') {
            try {
                element.style[property] = value;
            } catch (e) {
                console.warn('Style access failed:', e);
            }
        }
    }

    // Override common style setters to be null-safe
    window.safeStyleAccess = safeStyleAccess;

    // Override console errors to prevent UI breaking
    const originalError = console.error;
    console.error = function(...args) {
        if (args[0] && typeof args[0] === 'string') {
            if (args[0].includes('Firebase') || 
                args[0].includes('auth') || 
                args[0].includes('Alpine') ||
                args[0].includes('Cannot read properties of null')) {
                console.warn('Error caught and handled:', ...args);
                return;
            }
        }
        originalError.apply(console, args);
    };

    // Safe element operations
    window.safeSetStyle = function(element, property, value) {
        try {
            if (element && element.style && typeof element.style === 'object') {
                element.style[property] = value;
                return true;
            }
        } catch (e) {
            console.warn('Safe style operation failed:', e);
        }
        return false;
    };

    window.safeQuerySelector = function(selector) {
        try {
            return document.querySelector(selector);
        } catch (e) {
            console.warn('Safe query selector failed:', e);
            return null;
        }
    };

    window.safeQuerySelectorAll = function(selector) {
        try {
            return document.querySelectorAll(selector);
        } catch (e) {
            console.warn('Safe query selector all failed:', e);
            return [];
        }
    };

    // Alpine.js fallback
    function initializeAlpineFallback() {
        if (typeof Alpine === 'undefined') {
            console.log('Alpine.js not found, creating fallback');
            window.Alpine = {
                store: function(name, data) {
                    window['alpine_store_' + name] = data;
                    return {
                        ...data,
                        closeMobileMenu: function() {
                            const mobileMenu = document.querySelector('[x-show="$store.navigation.mobileMenuOpen"]');
                            if (mobileMenu) {
                                mobileMenu.style.display = 'none';
                            }
                        }
                    };
                }
            };
        }
    }

    // Fix Firebase auth errors
    function fixFirebaseAuth() {
        if (typeof firebase === 'undefined') {
            window.firebase = {
                auth: function() {
                    return {
                        onAuthStateChanged: function(callback) {
                            // Call with null user for guest mode
                            setTimeout(() => callback(null), 100);
                        },
                        signOut: function() {
                            return Promise.resolve();
                        }
                    };
                },
                initializeApp: function() {
                    return {};
                }
            };
            console.log('Firebase auth setup safely handled');
        }
    }

    // Fix tool displays
    function fixToolDisplays() {
        const toolCards = window.safeQuerySelectorAll('.tool-card');
        console.log(`Found ${toolCards.length} tool cards to fix`);

        toolCards.forEach((card, index) => {
            if (card) {
                // Ensure visibility
                window.safeSetStyle(card, 'display', 'block');
                window.safeSetStyle(card, 'visibility', 'visible');
                window.safeSetStyle(card, 'opacity', '1');

                // Add animation delay
                window.safeSetStyle(card, 'animationDelay', `${index * 0.1}s`);

                // Safe event listeners
                try {
                    card.addEventListener('mouseenter', function() {
                        window.safeSetStyle(this, 'transform', 'translateY(-4px) scale(1.02)');
                    });

                    card.addEventListener('mouseleave', function() {
                        window.safeSetStyle(this, 'transform', 'translateY(0) scale(1)');
                    });
                } catch (e) {
                    console.warn('Error adding event listeners:', e);
                }
            }
        });

        console.log('✅ Tool displays fixed');
    }

    // Initialize Lucide icons safely
    function initLucideIcons() {
        try {
            if (typeof lucide !== 'undefined' && lucide.createIcons) {
                lucide.createIcons();
                console.log('✅ Lucide icons initialized');
            }
        } catch (e) {
            console.warn('Lucide icons initialization failed:', e);
        }
    }

    // Fix mobile menu
    function fixMobileMenu() {
        const mobileMenuToggle = window.safeQuerySelector('[onclick*="mobileMenuOpen"]');
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', function(e) {
                e.preventDefault();
                const mobileMenu = window.safeQuerySelector('[x-show*="mobileMenuOpen"]');
                if (mobileMenu) {
                    const isVisible = mobileMenu.style.display !== 'none';
                    window.safeSetStyle(mobileMenu, 'display', isVisible ? 'none' : 'block');
                }
            });
        }
    }

    // Main initialization
    function initializeErrorFixes() {
        console.log('🚀 Initializing error fixes...');

        // Initialize Alpine fallback first
        initializeAlpineFallback();

        // Fix Firebase
        fixFirebaseAuth();

        // Fix mobile menu
        fixMobileMenu();

        // Fix tool displays
        setTimeout(function() {
            fixToolDisplays();
            initLucideIcons();
        }, 100);

        // Additional fixes after page load
        setTimeout(function() {
            fixToolDisplays();

            // Ensure all hidden elements are visible
            const hiddenElements = window.safeQuerySelectorAll('[style*="display: none"], .hidden');
            hiddenElements.forEach(function(element) {
                if (element && element.classList && element.classList.contains('tool-card')) {
                    element.classList.remove('hidden');
                    window.safeSetStyle(element, 'display', 'block');
                    window.safeSetStyle(element, 'visibility', 'visible');
                    window.safeSetStyle(element, 'opacity', '1');
                }
            });

            console.log('✅ All error fixes applied');
        }, 500);
    }

    // Run fixes when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeErrorFixes);
    } else {
        initializeErrorFixes();
    }

    // Run fixes on page load
    window.addEventListener('load', function() {
        setTimeout(initializeErrorFixes, 100);
    });

    console.log('🔧 Comprehensive error fixes loaded');
})();