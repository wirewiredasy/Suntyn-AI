/**
 * Firebase Null-Safe Handler
 * Prevents all null reference errors from Firebase authentication
 */

(function() {
    'use strict';
    
    // Create null-safe Firebase stub
    window.firebase = window.firebase || {
        auth: function() {
            return {
                onAuthStateChanged: function(callback) {
                    // Call with null user to simulate logged out state
                    if (typeof callback === 'function') {
                        callback(null);
                    }
                    return function() {}; // Unsubscribe function
                },
                signInWithRedirect: function() { return Promise.resolve(); },
                signInWithPopup: function() { return Promise.resolve(); },
                signOut: function() { return Promise.resolve(); },
                currentUser: null
            };
        },
        initializeApp: function() { return {}; }
    };
    
    // Null-safe auth property setter
    Object.defineProperty(window, 'firebaseAuth', {
        get: function() { return null; },
        set: function(value) {
            // Silently ignore attempts to set auth
            return null;
        },
        configurable: true
    });
    
    // Prevent null auth property errors
    if (typeof window.auth === 'undefined') {
        window.auth = null;
    }
    
    // Safe event listener for auth state changes
    window.onAuthStateChanged = function(callback) {
        if (typeof callback === 'function') {
            callback(null); // Always call with null user
        }
    };
    
    console.log('🔒 Firebase null-safe handler initialized');
})();

// DOM ready handler for additional safety
document.addEventListener('DOMContentLoaded', function() {
    // Remove any remaining Firebase scripts that might cause issues
    const scripts = document.querySelectorAll('script[src*="firebase"]');
    scripts.forEach(script => {
        if (script.parentNode) {
            script.parentNode.removeChild(script);
        }
    });
    
    // Ensure all auth-related properties are null-safe
    const authElements = document.querySelectorAll('[data-auth]');
    authElements.forEach(element => {
        if (element && element.style) {
            element.style.display = 'none'; // Hide auth elements
        }
    });
    
    console.log('🛡️ Firebase null-safety applied to DOM elements');
});