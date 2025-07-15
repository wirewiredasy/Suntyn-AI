// Enhanced search functionality with proper error handling
(function() {
    'use strict';
    
    // Tool database for search
    const toolDatabase = [
        // PDF Tools
        { tool: 'pdf-merge', category: 'pdf', category_name: 'PDF Toolkit', icon: 'layers', color: 'red', keywords: ['merge', 'combine', 'join'] },
        { tool: 'pdf-split', category: 'pdf', category_name: 'PDF Toolkit', icon: 'scissors', color: 'red', keywords: ['split', 'separate', 'divide'] },
        { tool: 'pdf-compress', category: 'pdf', category_name: 'PDF Toolkit', icon: 'archive', color: 'red', keywords: ['compress', 'reduce', 'size'] },
        { tool: 'pdf-to-word', category: 'pdf', category_name: 'PDF Toolkit', icon: 'file-text', color: 'red', keywords: ['convert', 'word', 'doc'] },
        { tool: 'word-to-pdf', category: 'pdf', category_name: 'PDF Toolkit', icon: 'file-pdf', color: 'red', keywords: ['convert', 'word', 'pdf'] },
        
        // Image Tools  
        { tool: 'image-compress', category: 'image', category_name: 'Image Toolkit', icon: 'minimize-2', color: 'green', keywords: ['compress', 'reduce', 'optimize'] },
        { tool: 'image-resize', category: 'image', category_name: 'Image Toolkit', icon: 'maximize-2', color: 'green', keywords: ['resize', 'scale', 'dimensions'] },
        { tool: 'image-convert', category: 'image', category_name: 'Image Toolkit', icon: 'repeat', color: 'green', keywords: ['convert', 'format', 'jpg', 'png'] },
        { tool: 'background-remover', category: 'image', category_name: 'Image Toolkit', icon: 'eraser', color: 'green', keywords: ['background', 'remove', 'transparent'] },
        
        // Video Tools
        { tool: 'video-to-mp3', category: 'video', category_name: 'Video & Audio', icon: 'music', color: 'purple', keywords: ['audio', 'extract', 'mp3', 'sound'] },
        { tool: 'video-trimmer', category: 'video', category_name: 'Video & Audio', icon: 'scissors', color: 'purple', keywords: ['trim', 'cut', 'edit'] },
        { tool: 'audio-remover', category: 'video', category_name: 'Video & Audio', icon: 'volume-x', color: 'purple', keywords: ['mute', 'silent', 'remove'] },
        
        // AI Tools
        { tool: 'resume-generator', category: 'ai', category_name: 'AI Tools', icon: 'briefcase', color: 'violet', keywords: ['resume', 'cv', 'generate'] },
        { tool: 'business-name-generator', category: 'ai', category_name: 'AI Tools', icon: 'building', color: 'violet', keywords: ['business', 'name', 'company'] },
        { tool: 'blog-title-generator', category: 'ai', category_name: 'AI Tools', icon: 'pen-tool', color: 'violet', keywords: ['blog', 'title', 'headline'] }
    ];
    
    // Enhanced search function
    function enhancedSearchTools() {
        try {
            if (!this.searchQuery || typeof this.searchQuery !== 'string' || this.searchQuery.length < 2) {
                this.searchResults = [];
                return;
            }
            
            const query = this.searchQuery.toLowerCase().trim();
            const results = [];
            
            toolDatabase.forEach(tool => {
                const toolName = tool.tool.replace(/-/g, ' ').toLowerCase();
                const categoryName = tool.category_name.toLowerCase();
                const keywords = tool.keywords.join(' ').toLowerCase();
                
                // Check if query matches tool name, category, or keywords
                if (toolName.includes(query) || 
                    categoryName.includes(query) || 
                    keywords.includes(query) ||
                    tool.tool.toLowerCase().includes(query)) {
                    results.push(tool);
                }
            });
            
            // Sort by relevance (exact matches first)
            results.sort((a, b) => {
                const aToolName = a.tool.replace(/-/g, ' ').toLowerCase();
                const bToolName = b.tool.replace(/-/g, ' ').toLowerCase();
                
                const aExact = aToolName.startsWith(query) ? 1 : 0;
                const bExact = bToolName.startsWith(query) ? 1 : 0;
                
                return bExact - aExact;
            });
            
            this.searchResults = results.slice(0, 8);
            
        } catch (error) {
            console.warn('Search error handled:', error);
            this.searchResults = [];
        }
    }
    
    // Make it globally available
    window.searchTools = enhancedSearchTools;
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Enhanced search functionality loaded');
        
        // Initialize Lucide icons if available
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    });
})();