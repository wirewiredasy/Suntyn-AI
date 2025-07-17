/**
 * Professional Mode - Disable Authentication for Better UX
 * Removes Firebase redirects and authentication requirements
 */

// Execute immediately to prevent Firebase issues
(function() {
    'use strict';
    
    // Block Firebase configuration immediately
    window.firebaseConfig = null;
    
    // Override Firebase if it exists
    if (typeof window.firebase !== 'undefined') {
        window.firebase = null;
    }
    
    console.log('🚀 Firebase authentication disabled for professional experience');
})();

// When DOM loads, ensure tools are accessible
window.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Professional Mode: Authentication disabled for better user experience');
    
    // Remove Firebase scripts that cause redirects
    const firebaseScripts = document.querySelectorAll('script[src*="firebase"]');
    firebaseScripts.forEach(script => {
        script.remove();
    });
    
    // Override Firebase functions if they exist
    if (typeof firebase !== 'undefined') {
        firebase.auth = function() {
            return {
                onAuthStateChanged: () => {},
                signInWithRedirect: () => {},
                signInWithPopup: () => {},
                signOut: () => Promise.resolve()
            };
        };
    }
    
    // Ensure all tools are accessible
    const toolLinks = document.querySelectorAll('a[href*="/tools/"]');
    toolLinks.forEach(link => {
        link.style.pointerEvents = 'auto';
        link.removeAttribute('disabled');
    });
    
    // Force show all tool cards
    setTimeout(() => {
        const toolCards = document.querySelectorAll('.tool-card');
        toolCards.forEach(card => {
            if (card && card.style) {
                card.style.display = 'block';
                card.style.visibility = 'visible';
                card.style.opacity = '1';
            }
        });
        console.log(`✅ ${toolCards.length} tools made accessible in professional mode`);
    }, 1000);
});

// Block Firebase configuration to prevent issues
window.firebaseConfig = null;
window.firebase = null;

console.log('🚀 Professional Mode Initialized - All tools accessible without authentication');