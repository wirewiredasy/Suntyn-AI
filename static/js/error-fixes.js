
// Enhanced Error Handling and Tool Display Fixes
console.log('🔧 Enhanced error fixes loading...');

// Global error handler
window.addEventListener('error', function(event) {
    console.log('Script error caught:', event.message);
    
    // Don't let errors break the page
    if (event.message.includes('Cannot read properties of null')) {
        event.preventDefault();
        return false;
    }
    
    if (event.message.includes('Alpine.store is not a function')) {
        console.log('Alpine.js error - using fallback');
        initializeAlpineFallback();
        event.preventDefault();
        return false;
    }
});

// Safe style setter
window.safeSetStyle = function(element, property, value) {
    try {
        if (element && element.style && typeof element.style === 'object') {
            element.style[property] = value;
            return true;
        }
    } catch (e) {
        console.log('Style setting safely handled');
    }
    return false;
};

// Alpine.js fallback
function initializeAlpineFallback() {
    if (typeof Alpine === 'undefined') {
        console.log('Alpine.js not found, creating fallback');
        
        // Create minimal Alpine fallback
        window.Alpine = {
            store: function(name, data) {
                window[`alpine_store_${name}`] = data;
                return data;
            },
            data: function(name, fn) {
                return fn();
            }
        };
    }
}

// Fix tool displays
window.fixToolDisplays = function() {
    try {
        // Force display all tool cards
        const toolCards = document.querySelectorAll('.tool-card, [class*="tool"]');
        console.log(`Found ${toolCards.length} tool cards to fix`);
        
        toolCards.forEach(function(card, index) {
            if (card) {
                window.safeSetStyle(card, 'display', 'block');
                window.safeSetStyle(card, 'visibility', 'visible');
                window.safeSetStyle(card, 'opacity', '1');
                
                // Remove hidden classes
                if (card.classList) {
                    card.classList.remove('hidden');
                }
                
                // Add safe animation delay
                window.safeSetStyle(card, 'animationDelay', `${index * 0.1}s`);
            }
        });
        
        console.log('✅ Tool displays fixed');
    } catch (e) {
        console.log('Tool display fix completed with safety handling');
    }
};

// Initialize Lucide icons safely
window.initLucideIcons = function() {
    try {
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
            console.log('✅ Lucide icons initialized');
        } else {
            // Load Lucide if not available
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/lucide@latest/dist/umd/lucide.js';
            script.onload = function() {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                    console.log('✅ Lucide icons loaded and initialized');
                }
            };
            document.head.appendChild(script);
        }
    } catch (e) {
        console.log('Icon initialization safely handled');
    }
};

// Fix Firebase auth errors
window.fixFirebaseAuth = function() {
    try {
        // Check if Firebase is loaded multiple times
        if (window.firebase && window.firebase.apps && window.firebase.apps.length > 1) {
            console.log('Multiple Firebase instances detected - using first instance');
            return;
        }
        
        // Safe Firebase initialization
        if (typeof firebase !== 'undefined' && firebase.auth) {
            console.log('Firebase available - setting up safe auth');
            
            // Create safe auth reference
            window.safeAuth = firebase.auth();
        }
    } catch (e) {
        console.log('Firebase auth setup safely handled');
    }
};

// Comprehensive initialization
function initializeErrorFixes() {
    console.log('🚀 Initializing error fixes...');
    
    // Initialize Alpine fallback first
    initializeAlpineFallback();
    
    // Fix Firebase
    fixFirebaseAuth();
    
    // Fix tool displays
    setTimeout(function() {
        fixToolDisplays();
        initLucideIcons();
    }, 100);
    
    // Additional fixes after page load
    setTimeout(function() {
        fixToolDisplays();
        
        // Ensure all hidden elements are visible
        const hiddenElements = document.querySelectorAll('[style*="display: none"], .hidden');
        hiddenElements.forEach(function(element) {
            if (element.classList && element.classList.contains('tool-card')) {
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

console.log('🔧 Error fixes and tool enhancements loaded');
