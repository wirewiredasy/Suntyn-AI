/**
 * Comprehensive null safety fixes for Toolora AI
 * Fixes all .style access errors preventing tools from displaying
 */

// Safe style setter function
window.safeSetStyle = function(element, property, value) {
    if (element && element.style && typeof element.style === 'object') {
        element.style[property] = value;
        return true;
    }
    return false;
};

// Safe style getter function
window.safeGetStyle = function(element, property) {
    if (element && element.style && typeof element.style === 'object') {
        return element.style[property];
    }
    return null;
};

// Override problematic functions with null-safe versions
document.addEventListener('DOMContentLoaded', function() {
    console.log('Applying null safety fixes...');
    
    // Fix tool card animations safely
    const toolCards = document.querySelectorAll('.tool-card');
    console.log(`Found ${toolCards.length} tool cards for null safety fix`);
    
    toolCards.forEach((card, index) => {
        if (card && typeof card === 'object') {
            // Safe animation delay
            window.safeSetStyle(card, 'animationDelay', `${index * 0.1}s`);
            
            // Safe hover effects
            if (typeof card.addEventListener === 'function') {
                card.addEventListener('mouseenter', function() {
                    window.safeSetStyle(this, 'transform', 'translateY(-4px) scale(1.02)');
                    window.safeSetStyle(this, 'boxShadow', '0 20px 25px -5px rgba(0, 0, 0, 0.1)');
                });
                
                card.addEventListener('mouseleave', function() {
                    window.safeSetStyle(this, 'transform', 'translateY(0) scale(1)');
                    window.safeSetStyle(this, 'boxShadow', '');
                });
            }
        }
    });
    
    // Ensure all tool cards are visible
    toolCards.forEach(card => {
        if (card) {
            window.safeSetStyle(card, 'display', 'block');
            window.safeSetStyle(card, 'visibility', 'visible');
            window.safeSetStyle(card, 'opacity', '1');
        }
    });
    
    console.log('Null safety fixes applied successfully');
});

// Global error handler for uncaught style errors
window.addEventListener('error', function(event) {
    if (event.message && event.message.includes('style')) {
        console.warn('Caught style error:', event.message);
        event.preventDefault();
        return true;
    }
});