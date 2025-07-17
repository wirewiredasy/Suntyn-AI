// Enhanced search functionality for Suntyn AI
(function() {
    'use strict';
    
    // Tool database
    const tools = [
        { tool: 'pdf-merge', category: 'pdf', category_name: 'PDF Toolkit', icon: 'layers', color: 'red' },
        { tool: 'pdf-split', category: 'pdf', category_name: 'PDF Toolkit', icon: 'scissors', color: 'red' },
        { tool: 'pdf-compress', category: 'pdf', category_name: 'PDF Toolkit', icon: 'archive', color: 'red' },
        { tool: 'pdf-to-word', category: 'pdf', category_name: 'PDF Toolkit', icon: 'file-text', color: 'red' },
        { tool: 'word-to-pdf', category: 'pdf', category_name: 'PDF Toolkit', icon: 'file-pdf', color: 'red' },
        { tool: 'image-compress', category: 'image', category_name: 'Image Toolkit', icon: 'minimize-2', color: 'green' },
        { tool: 'image-resize', category: 'image', category_name: 'Image Toolkit', icon: 'maximize-2', color: 'green' },
        { tool: 'image-convert', category: 'image', category_name: 'Image Toolkit', icon: 'repeat', color: 'green' },
        { tool: 'background-remover', category: 'image', category_name: 'Image Toolkit', icon: 'eraser', color: 'green' },
        { tool: 'video-trimmer', category: 'video', category_name: 'Video & Audio', icon: 'scissors', color: 'purple' },
        { tool: 'video-to-mp3', category: 'video', category_name: 'Video & Audio', icon: 'music', color: 'purple' },
        { tool: 'audio-remover', category: 'video', category_name: 'Video & Audio', icon: 'volume-x', color: 'purple' },
        { tool: 'resume-generator', category: 'ai', category_name: 'AI Tools', icon: 'briefcase', color: 'violet' },
        { tool: 'business-name-generator', category: 'ai', category_name: 'AI Tools', icon: 'building', color: 'violet' },
        { tool: 'blog-title-generator', category: 'ai', category_name: 'AI Tools', icon: 'pen-tool', color: 'violet' },
        { tool: 'qr-generator', category: 'utility', category_name: 'Utility Tools', icon: 'qr-code', color: 'slate' },
        { tool: 'password-generator', category: 'utility', category_name: 'Utility Tools', icon: 'key', color: 'slate' },
        { tool: 'age-bmi-calculator', category: 'utility', category_name: 'Utility Tools', icon: 'calculator', color: 'slate' }
    ];
    
    // Search function
    window.performSearch = function(query) {
        if (!query || query.length < 2) return [];
        
        const searchTerm = query.toLowerCase();
        const results = tools.filter(tool => {
            const toolName = tool.tool.replace(/-/g, ' ').toLowerCase();
            const categoryName = tool.category_name.toLowerCase();
            
            return toolName.includes(searchTerm) || 
                   categoryName.includes(searchTerm) ||
                   tool.tool.toLowerCase().includes(searchTerm);
        });
        
        return results.slice(0, 8);
    };
    
    console.log('Search functionality ready');
})();