
/**
 * Enhanced Tool Icons System - Fixed Version
 * All 85+ tools with proper icon mapping
 */

const TOOL_ICONS = {
    // PDF Tools (15)
    'pdf-merge': 'layers',
    'pdf-split': 'scissors', 
    'pdf-compress': 'archive',
    'pdf-to-word': 'file-text',
    'pdf-to-jpg': 'image',
    'word-to-pdf': 'file-plus',
    'jpg-to-pdf': 'file-image',
    'pdf-watermark': 'droplets',
    'pdf-annotator': 'edit-3',
    'pdf-page-numbers': 'hash',
    'pdf-unlock': 'unlock',
    'pdf-protect': 'lock',
    'pdf-rotate': 'rotate-cw',
    'pdf-extract-pages': 'file-minus',
    'pdf-chat': 'message-circle',
    'pdf-summarize': 'file-text',

    // Image Tools (15)
    'image-compress': 'minimize-2',
    'image-resize': 'maximize-2', 
    'image-convert': 'repeat',
    'image-crop': 'crop',
    'background-remover': 'eraser',
    'image-enhancer': 'sun',
    'image-watermark': 'droplets',
    'image-rotate': 'rotate-cw',
    'image-ocr': 'eye',
    'color-picker': 'palette',
    'social-crop': 'smartphone',
    'image-caption': 'type',
    'profile-pic-maker': 'user-circle',
    'meme-generator': 'smile',
    'text-to-image': 'image',

    // Video & Audio Tools (10)
    'video-to-mp3': 'music',
    'audio-remover': 'volume-x',
    'video-trimmer': 'scissors',
    'voice-remover': 'mic-off',
    'subtitle-generator': 'subtitles',
    'subtitle-merger': 'video',
    'video-compress': 'minimize',
    'video-converter': 'repeat',
    'dubbing-tool': 'mic',
    'shorts-cropper': 'smartphone',

    // AI Tools (15)
    'resume-generator': 'briefcase',
    'business-name-generator': 'building',
    'blog-title-generator': 'pen-tool',
    'product-description': 'package',
    'ad-copy-generator': 'megaphone',
    'script-writer': 'film',
    'bio-generator': 'user',
    'faq-generator': 'help-circle',
    'idea-explainer': 'lightbulb',
    'notes-summarizer': 'file-text',
    'notes-to-mcq': 'list',
    'chat-with-notes': 'message-square',
    'doc-translator': 'globe',
    'mindmap-creator': 'git-branch',
    'handwriting-to-text': 'edit',

    // Text Tools (8)
    'text-case-converter': 'type',
    'password-generator': 'key',
    'qr-generator': 'qr-code',
    'barcode-generator': 'scan',
    'url-shortener': 'link',
    'clipboard-notepad': 'clipboard',
    'signature-extractor': 'pen-tool',
    'whiteboard-saver': 'save',

    // Utility Tools (12)
    'file-renamer': 'edit-2',
    'zip-unzip': 'package',
    'currency-converter': 'dollar-sign',
    'age-bmi-calculator': 'calculator',
    'budget-planner': 'pie-chart',
    'loan-emi-calculator': 'credit-card',
    'gst-calculator': 'percent',
    'income-tax-estimator': 'trending-up',
    'flashcard-generator': 'book',
    'timetable-generator': 'calendar',
    'doc-to-slides': 'presentation',
    'syllabus-extractor': 'bookmark',

    // Government Tools (10)
    'aadhaar-masker': 'eye-off',
    'aadhaar-explainer': 'info',
    'pan-form-filler': 'file-plus',
    'ration-card-checker': 'check-circle',
    'govt-format-converter': 'refresh-cw',
    'legal-term-explainer': 'scale',
    'rent-agreement-reader': 'home',
    'stamp-paper-splitter': 'divide',
    'income-tax-calculator': 'calculator',
    'voter-id-validator': 'vote'
};

const CATEGORY_ICONS = {
    'pdf': 'file-text',
    'image': 'image', 
    'video': 'video',
    'ai': 'brain',
    'text': 'type',
    'utility': 'tool',
    'government': 'shield',
    'govt': 'shield',
    'student': 'graduation-cap',
    'finance': 'credit-card'
};

const CATEGORY_COLORS = {
    'pdf': 'red',
    'image': 'green',
    'video': 'purple', 
    'ai': 'violet',
    'text': 'blue',
    'utility': 'orange',
    'government': 'indigo',
    'govt': 'indigo',
    'student': 'emerald',
    'finance': 'yellow'
};

// Enhanced icon functions
function getToolIcon(toolName) {
    if (!toolName) return 'tool';
    
    // Clean tool name
    const cleanName = toolName.toLowerCase().trim().replace(/\s+/g, '-');
    
    // Return icon or fallback
    return TOOL_ICONS[cleanName] || 'tool';
}

function getCategoryIcon(category) {
    if (!category) return 'folder';
    
    const cleanCategory = category.toLowerCase().trim();
    return CATEGORY_ICONS[cleanCategory] || 'folder';
}

function getCategoryColor(category) {
    if (!category) return 'gray';
    
    const cleanCategory = category.toLowerCase().trim();
    return CATEGORY_COLORS[cleanCategory] || 'gray';
}

// Initialize icons for all tool cards
function initializeToolIcons() {
    console.log('🎨 Initializing tool icons...');
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeToolIcons);
        return;
    }
    
    try {
        // Update all tool cards
        const toolCards = document.querySelectorAll('.tool-card, [data-tool]');
        console.log(`Found ${toolCards.length} tool cards to update`);
        
        toolCards.forEach((card, index) => {
            try {
                const toolName = card.getAttribute('data-tool') || 
                               card.querySelector('[data-tool]')?.getAttribute('data-tool') ||
                               card.querySelector('.tool-title, h3')?.textContent?.toLowerCase().replace(/\s+/g, '-');
                
                if (toolName) {
                    const iconElement = card.querySelector('[data-lucide], .tool-icon, i');
                    if (iconElement) {
                        const iconName = getToolIcon(toolName);
                        iconElement.setAttribute('data-lucide', iconName);
                        
                        // Add some styling
                        iconElement.classList.add('w-6', 'h-6', 'text-current');
                        
                        console.log(`✅ Updated icon for ${toolName}: ${iconName}`);
                    }
                }
            } catch (e) {
                console.warn(`Error updating icon for card ${index}:`, e);
            }
        });
        
        // Update category icons
        const categoryElements = document.querySelectorAll('[data-category]');
        categoryElements.forEach(element => {
            try {
                const category = element.getAttribute('data-category');
                const iconElement = element.querySelector('[data-lucide], .category-icon');
                if (iconElement && category) {
                    const iconName = getCategoryIcon(category);
                    iconElement.setAttribute('data-lucide', iconName);
                }
            } catch (e) {
                console.warn('Error updating category icon:', e);
            }
        });
        
        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
            console.log('🎨 Lucide icons reinitialized');
        } else {
            console.warn('Lucide not available, retrying in 1 second...');
            setTimeout(() => {
                if (typeof lucide !== 'undefined' && lucide.createIcons) {
                    lucide.createIcons();
                    console.log('🎨 Lucide icons initialized (delayed)');
                }
            }, 1000);
        }
        
    } catch (error) {
        console.error('Error initializing tool icons:', error);
    }
}

// Auto-update icons when new content is added
function setupIconObserver() {
    const observer = new MutationObserver((mutations) => {
        let shouldUpdate = false;
        
        mutations.forEach(mutation => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        if (node.classList?.contains('tool-card') || 
                            node.querySelector?.('.tool-card') ||
                            node.hasAttribute?.('data-tool')) {
                            shouldUpdate = true;
                        }
                    }
                });
            }
        });
        
        if (shouldUpdate) {
            setTimeout(initializeToolIcons, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Export for global use
if (typeof window !== 'undefined') {
    window.ToolIcons = {
        getToolIcon,
        getCategoryIcon, 
        getCategoryColor,
        initializeToolIcons,
        TOOL_ICONS,
        CATEGORY_ICONS,
        CATEGORY_COLORS
    };
    
    // Auto-initialize
    initializeToolIcons();
    setupIconObserver();
}

// For Node.js compatibility
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getToolIcon,
        getCategoryIcon,
        getCategoryColor,
        TOOL_ICONS,
        CATEGORY_ICONS,
        CATEGORY_COLORS
    };
}

console.log('🎨 Tool Icons System loaded successfully');
