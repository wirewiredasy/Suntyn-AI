// Safe search functionality without syntax errors
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Prevent script errors from breaking the page
    window.addEventListener('error', function(e) {
        console.warn('Script error caught:', e.message);
        return true;
    });
    
    // Tool database
    const toolsDatabase = [
        { tool: 'pdf-merge', category: 'pdf', category_name: 'PDF Toolkit', icon: 'layers', color: 'red' },
        { tool: 'pdf-split', category: 'pdf', category_name: 'PDF Toolkit', icon: 'scissors', color: 'red' },
        { tool: 'pdf-compress', category: 'pdf', category_name: 'PDF Toolkit', icon: 'archive', color: 'red' },
        { tool: 'image-compress', category: 'image', category_name: 'Image Toolkit', icon: 'minimize-2', color: 'green' },
        { tool: 'image-resize', category: 'image', category_name: 'Image Toolkit', icon: 'maximize-2', color: 'green' },
        { tool: 'image-convert', category: 'image', category_name: 'Image Toolkit', icon: 'repeat', color: 'green' },
        { tool: 'video-trimmer', category: 'video', category_name: 'Video & Audio', icon: 'scissors', color: 'purple' },
        { tool: 'video-to-mp3', category: 'video', category_name: 'Video & Audio', icon: 'music', color: 'purple' },
        { tool: 'resume-generator', category: 'ai', category_name: 'AI Tools', icon: 'briefcase', color: 'violet' },
        { tool: 'qr-generator', category: 'utility', category_name: 'Utility Tools', icon: 'qr-code', color: 'slate' }
    ];
    
    // Global search function
    window.performSearch = function(query) {
        try {
            if (!query || query.length < 2) return [];
            
            const searchTerm = query.toLowerCase();
            const results = toolsDatabase.filter(function(tool) {
                const toolName = tool.tool.replace(/-/g, ' ').toLowerCase();
                const categoryName = tool.category_name.toLowerCase();
                
                return toolName.includes(searchTerm) || 
                       categoryName.includes(searchTerm) ||
                       tool.tool.toLowerCase().includes(searchTerm);
            });
            
            return results.slice(0, 8);
        } catch (error) {
            console.warn('Search error:', error.message);
            return [];
        }
    };
    
    // Search functionality initialized
});