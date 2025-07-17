
/**
 * Enhanced Icon Loader - Fixes icon loading issues
 */

class ToolIconLoader {
    constructor() {
        this.initialized = false;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.init();
    }

    init() {
        if (this.initialized) return;
        this.initialized = true;
        
        console.log('🔄 Initializing Tool Icon Loader...');
        
        // Wait for DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.loadIcons());
        } else {
            this.loadIcons();
        }
        
        // Setup observers
        this.setupMutationObserver();
    }

    loadIcons() {
        try {
            // Ensure ToolIcons is available
            if (typeof window.ToolIcons === 'undefined') {
                console.log('⏳ ToolIcons not loaded yet, retrying...');
                if (this.retryCount < this.maxRetries) {
                    this.retryCount++;
                    setTimeout(() => this.loadIcons(), 500);
                }
                return;
            }

            this.updateAllToolIcons();
            this.ensureLucideIcons();
            
        } catch (error) {
            console.error('Error in loadIcons:', error);
        }
    }

    updateAllToolIcons() {
        console.log('🎨 Updating all tool icons...');
        
        // Update tool cards
        const toolCards = document.querySelectorAll('.tool-card');
        console.log(`Found ${toolCards.length} tool cards`);
        
        toolCards.forEach((card, index) => {
            try {
                this.updateToolCard(card, index);
            } catch (e) {
                console.warn(`Error updating tool card ${index}:`, e);
            }
        });
        
        // Update search results
        const searchResults = document.querySelectorAll('.search-result-item, .search-result');
        searchResults.forEach(result => {
            try {
                this.updateSearchResult(result);
            } catch (e) {
                console.warn('Error updating search result:', e);
            }
        });
        
        // Update category cards
        const categoryCards = document.querySelectorAll('.category-card');
        categoryCards.forEach(card => {
            try {
                this.updateCategoryCard(card);
            } catch (e) {
                console.warn('Error updating category card:', e);
            }
        });
    }

    updateToolCard(card, index) {
        if (!card) return;
        
        // Get tool name from various sources
        const toolName = this.extractToolName(card);
        
        if (!toolName) {
            console.warn(`No tool name found for card ${index}`);
            return;
        }
        
        // Find icon element
        const iconElement = this.findIconElement(card);
        
        if (iconElement && window.ToolIcons) {
            const iconName = window.ToolIcons.getToolIcon(toolName);
            this.setIcon(iconElement, iconName);
            
            // Ensure proper styling
            this.ensureIconStyling(iconElement);
            
            console.log(`✅ Updated icon for ${toolName}: ${iconName}`);
        } else {
            console.warn(`No icon element found for ${toolName}`);
        }
    }

    updateSearchResult(result) {
        if (!result) return;
        
        const toolName = this.extractToolName(result);
        const iconElement = this.findIconElement(result);
        
        if (iconElement && toolName && window.ToolIcons) {
            const iconName = window.ToolIcons.getToolIcon(toolName);
            this.setIcon(iconElement, iconName);
            this.ensureIconStyling(iconElement);
        }
    }

    updateCategoryCard(card) {
        if (!card) return;
        
        const category = card.getAttribute('data-category') || 
                        card.querySelector('[data-category]')?.getAttribute('data-category');
        
        const iconElement = this.findIconElement(card);
        
        if (iconElement && category && window.ToolIcons) {
            const iconName = window.ToolIcons.getCategoryIcon(category);
            this.setIcon(iconElement, iconName);
            this.ensureIconStyling(iconElement);
        }
    }

    extractToolName(element) {
        // Try multiple ways to get tool name
        return element.getAttribute('data-tool') ||
               element.getAttribute('data-tool-name') ||
               element.querySelector('[data-tool]')?.getAttribute('data-tool') ||
               element.querySelector('.tool-title, h3, h4')?.textContent?.toLowerCase().replace(/\s+/g, '-') ||
               element.querySelector('a')?.href?.split('/').pop() ||
               null;
    }

    findIconElement(container) {
        // Try multiple selectors for icon elements
        return container.querySelector('[data-lucide]') ||
               container.querySelector('.tool-icon') ||
               container.querySelector('.icon') ||
               container.querySelector('i[class*="lucide"]') ||
               container.querySelector('svg') ||
               container.querySelector('.category-icon');
    }

    setIcon(element, iconName) {
        if (!element || !iconName) return;
        
        // Set the icon
        element.setAttribute('data-lucide', iconName);
        
        // Remove old classes that might interfere
        element.classList.remove('hidden', 'opacity-0');
        
        // Ensure visibility
        element.style.display = '';
        element.style.visibility = 'visible';
    }

    ensureIconStyling(element) {
        if (!element) return;
        
        // Add proper classes for consistent styling
        const classes = ['w-6', 'h-6', 'text-current', 'flex-shrink-0'];
        classes.forEach(cls => {
            if (!element.classList.contains(cls)) {
                element.classList.add(cls);
            }
        });
        
        // Ensure proper positioning
        if (element.parentElement) {
            const parent = element.parentElement;
            if (!parent.classList.contains('flex') && !parent.classList.contains('inline-flex')) {
                parent.classList.add('flex', 'items-center', 'gap-2');
            }
        }
    }

    ensureLucideIcons() {
        try {
            if (typeof lucide !== 'undefined' && lucide.createIcons) {
                lucide.createIcons();
                console.log('🎨 Lucide icons refreshed');
            } else {
                console.warn('Lucide not available, scheduling retry...');
                setTimeout(() => {
                    if (typeof lucide !== 'undefined' && lucide.createIcons) {
                        lucide.createIcons();
                        console.log('🎨 Lucide icons refreshed (delayed)');
                    }
                }, 1000);
            }
        } catch (error) {
            console.error('Error refreshing Lucide icons:', error);
        }
    }

    setupMutationObserver() {
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;
            
            mutations.forEach(mutation => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) { // Element node
                            if (this.isToolElement(node)) {
                                shouldUpdate = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldUpdate) {
                console.log('🔄 New tool elements detected, updating icons...');
                setTimeout(() => this.updateAllToolIcons(), 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    isToolElement(element) {
        return element.classList?.contains('tool-card') ||
               element.classList?.contains('search-result-item') ||
               element.classList?.contains('category-card') ||
               element.querySelector?.('.tool-card') ||
               element.hasAttribute?.('data-tool');
    }

    // Force refresh method
    forceRefresh() {
        console.log('🔄 Force refreshing all icons...');
        this.retryCount = 0;
        this.loadIcons();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (!window.toolIconLoader) {
        window.toolIconLoader = new ToolIconLoader();
    }
});

// Global refresh function
window.refreshToolIcons = function() {
    if (window.toolIconLoader) {
        window.toolIconLoader.forceRefresh();
    } else {
        window.toolIconLoader = new ToolIconLoader();
    }
};

// Export for external use
window.ToolIconLoader = ToolIconLoader;

console.log('🔄 Tool Icon Loader initialized');
