
/**
 * Dynamic Icon Loader - Updates tool icons based on tool name
 */

class IconManager {
    constructor() {
        this.initialized = false;
        this.init();
    }

    init() {
        if (this.initialized) return;
        this.initialized = true;
        
        // Load tool icons script if not loaded
        if (typeof window.ToolIcons === 'undefined') {
            const script = document.createElement('script');
            script.src = '/static/js/tool-icons.js';
            script.onload = () => {
                this.updateToolIcons();
            };
            document.head.appendChild(script);
        } else {
            this.updateToolIcons();
        }
    }

    updateToolIcons() {
        if (typeof window.ToolIcons === 'undefined') return;
        
        // Update tool cards
        const toolCards = document.querySelectorAll('.tool-card');
        toolCards.forEach(card => {
            const toolName = card.getAttribute('data-tool');
            if (toolName) {
                const icon = card.querySelector('[data-lucide]');
                if (icon) {
                    const customIcon = window.ToolIcons.getToolIcon(toolName);
                    icon.setAttribute('data-lucide', customIcon);
                }
            }
        });
        
        // Update search results
        const searchResults = document.querySelectorAll('.search-result-item');
        searchResults.forEach(result => {
            const toolName = result.getAttribute('data-tool');
            if (toolName) {
                const icon = result.querySelector('[data-lucide]');
                if (icon) {
                    const customIcon = window.ToolIcons.getToolIcon(toolName);
                    icon.setAttribute('data-lucide', customIcon);
                }
            }
        });
        
        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

// Initialize icon manager when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (!window.iconManager) {
        window.iconManager = new IconManager();
    }
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// Export for external use
window.updateToolIcons = function() {
    if (typeof window.ToolIcons === 'undefined') return;
    
    // Update tool cards
    const toolCards = document.querySelectorAll('.tool-card');
    toolCards.forEach(card => {
        const toolName = card.getAttribute('data-tool');
        if (toolName) {
            const icon = card.querySelector('[data-lucide]');
            if (icon) {
                const customIcon = window.ToolIcons.getToolIcon(toolName);
                icon.setAttribute('data-lucide', customIcon);
            }
        }
    });
    
    // Update search results
    const searchResults = document.querySelectorAll('.search-result-item');
    searchResults.forEach(result => {
        const toolName = result.getAttribute('data-tool');
        if (toolName) {
            const icon = result.querySelector('[data-lucide]');
            if (icon) {
                const customIcon = window.ToolIcons.getToolIcon(toolName);
                icon.setAttribute('data-lucide', customIcon);
            }
        }
    });
    
    // Reinitialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
};

// Export for use
window.updateToolIcons = updateToolIcons;
