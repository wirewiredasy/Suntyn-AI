// Tool API endpoint mappings for Toolora AI
const TOOL_ENDPOINTS = {
    // PDF Tools
    'pdf-merge': '/api/pdf/merge',
    'pdf-split': '/api/pdf/split', 
    'pdf-compress': '/api/pdf/compress',
    'pdf-watermark': '/api/pdf/watermark',
    'pdf-to-word': '/api/pdf/to-word',
    'word-to-pdf': '/api/pdf/from-word',
    'pdf-to-jpg': '/api/pdf/to-image',
    'jpg-to-pdf': '/api/pdf/from-image',
    
    // Image Tools
    'image-compress': '/api/image/compress',
    'image-resize': '/api/image/resize',
    'image-convert': '/api/image/convert',
    'image-crop': '/api/image/crop',
    'image-rotate': '/api/image/rotate',
    'image-watermark': '/api/image/watermark',
    'background-remover': '/api/image/remove-background',
    'image-enhancer': '/api/image/enhance',
    
    // Video Tools
    'video-to-mp3': '/api/video/extract-audio',
    'audio-remover': '/api/video/remove-audio',
    'video-trimmer': '/api/video/trim',
    'video-compress': '/api/video/compress',
    'video-converter': '/api/video/convert',
    'shorts-cropper': '/api/video/crop-vertical',
    
    // AI Tools
    'resume-generator': '/api/ai/generate-resume',
    'business-name-generator': '/api/ai/generate-business-names',
    'blog-title-generator': '/api/ai/generate-blog-titles',
    'product-description': '/api/ai/generate-product-description',
    'ad-copy-generator': '/api/ai/generate-ad-copy',
    'faq-generator': '/api/ai/generate-faq',
    'script-writer': '/api/ai/write-script',
    'bio-generator': '/api/ai/generate-bio',
    
    // Utility Tools
    'qr-generator': '/api/utility/generate-qr',
    'barcode-generator': '/api/utility/generate-barcode',
    'password-generator': '/api/utility/generate-password',
    'text-case-converter': '/api/utility/convert-text-case',
    'url-shortener': '/api/utility/shorten-url',
    'age-bmi-calculator': '/api/utility/calculate-age-bmi',
    
    // Government Tools
    'aadhaar-masker': '/api/govt/mask-aadhaar',
    'pan-form-filler': '/api/govt/fill-pan-form',
    'ration-card-checker': '/api/govt/check-ration-card',
    'doc-translator': '/api/govt/translate-document',
    
    // Finance Tools
    'loan-emi-calculator': '/api/finance/calculate-emi',
    'gst-calculator': '/api/finance/calculate-gst',
    'currency-converter': '/api/finance/convert-currency',
    'budget-planner': '/api/finance/plan-budget',
    'income-tax-estimator': '/api/finance/estimate-tax',
    
    // Student Tools
    'handwriting-to-text': '/api/student/ocr-handwriting',
    'notes-summarizer': '/api/student/summarize-notes',
    'flashcard-generator': '/api/student/generate-flashcards',
    'notes-to-mcq': '/api/student/notes-to-mcq',
    'chat-with-notes': '/api/student/chat-notes',
    'timetable-generator': '/api/student/generate-timetable',
    'syllabus-extractor': '/api/student/extract-syllabus'
};

// Get API endpoint for a tool
function getToolEndpoint(toolName) {
    return TOOL_ENDPOINTS[toolName] || `/api/tools/generic/${toolName}`;
}

// Helper function to determine if tool requires files
function toolRequiresFiles(toolName) {
    const noFileTools = [
        'resume-generator', 'business-name-generator', 'blog-title-generator',
        'password-generator', 'qr-generator', 'age-bmi-calculator',
        'loan-emi-calculator', 'gst-calculator', 'currency-converter',
        'text-case-converter', 'url-shortener'
    ];
    return !noFileTools.includes(toolName);
}

// Helper function to get accepted file types for a tool
function getAcceptedFileTypes(toolName) {
    const fileTypeMap = {
        // PDF tools
        'pdf-merge': '.pdf',
        'pdf-split': '.pdf',
        'pdf-compress': '.pdf',
        'pdf-watermark': '.pdf',
        'pdf-to-word': '.pdf',
        'pdf-to-jpg': '.pdf',
        'word-to-pdf': '.doc,.docx',
        'jpg-to-pdf': '.jpg,.jpeg,.png',
        
        // Image tools
        'image-compress': '.jpg,.jpeg,.png,.bmp,.webp',
        'image-resize': '.jpg,.jpeg,.png,.bmp,.webp',
        'image-convert': '.jpg,.jpeg,.png,.bmp,.webp',
        'image-crop': '.jpg,.jpeg,.png,.bmp,.webp',
        'background-remover': '.jpg,.jpeg,.png',
        
        // Video tools
        'video-to-mp3': '.mp4,.avi,.mov,.wmv,.flv,.mkv',
        'video-trimmer': '.mp4,.avi,.mov,.wmv,.flv,.mkv',
        'video-compress': '.mp4,.avi,.mov,.wmv,.flv,.mkv',
        'audio-remover': '.mp4,.avi,.mov,.wmv,.flv,.mkv',
        
        // Document tools
        'handwriting-to-text': '.jpg,.jpeg,.png,.pdf',
        'notes-summarizer': '.pdf,.txt,.doc,.docx',
        'doc-translator': '.pdf,.txt,.doc,.docx'
    };
    
    return fileTypeMap[toolName] || '.pdf,.jpg,.jpeg,.png,.mp4,.doc,.docx,.txt';
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TOOL_ENDPOINTS, getToolEndpoint, toolRequiresFiles, getAcceptedFileTypes };
}