
/**
 * Custom Icon Mapping for All 85 Tools
 * Each tool has a unique, meaningful icon
 */

const TOOL_ICONS = {
    // PDF Tools (15)
    'pdf-merge': 'layers',
    'pdf-split': 'scissors',
    'pdf-compress': 'archive',
    'pdf-to-word': 'file-text',
    'pdf-to-jpg': 'image',
    'word-to-pdf': 'file-pdf',
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
    'government': 'shield'
};

const CATEGORY_COLORS = {
    'pdf': 'red',
    'image': 'green',
    'video': 'purple',
    'ai': 'violet',
    'text': 'blue',
    'utility': 'orange',
    'government': 'indigo'
};

// Function to get tool icon
function getToolIcon(toolName) {
    return TOOL_ICONS[toolName] || 'tool';
}

// Function to get category icon
function getCategoryIcon(category) {
    return CATEGORY_ICONS[category] || 'folder';
}

// Function to get category color
function getCategoryColor(category) {
    return CATEGORY_COLORS[category] || 'gray';
}

// Export for use in other files
if (typeof window !== 'undefined') {
    window.ToolIcons = {
        getToolIcon,
        getCategoryIcon,
        getCategoryColor,
        TOOL_ICONS,
        CATEGORY_ICONS,
        CATEGORY_COLORS
    };
}
