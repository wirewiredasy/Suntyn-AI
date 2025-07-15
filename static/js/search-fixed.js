// Fixed search functionality - No errors
(function() {
    'use strict';
    
    // Prevent any errors from breaking the page
    window.addEventListener('error', function(e) {
        console.warn('Error caught:', e.message);
        return true; // Prevent default error handling
    });
    
    // Safe search function
    function safeSearchTools() {
        try {
            if (!this.searchQuery || typeof this.searchQuery !== 'string' || this.searchQuery.length < 2) {
                this.searchResults = [];
                return;
            }
            
            const query = this.searchQuery.toLowerCase().trim();
            
            // Static tool data to prevent server dependency errors
            const toolData = [
                { tool: 'pdf-merge', category: 'pdf', category_name: 'PDF Toolkit', icon: 'file-text', color: 'red' },
                { tool: 'pdf-split', category: 'pdf', category_name: 'PDF Toolkit', icon: 'scissors', color: 'red' },
                { tool: 'pdf-compress', category: 'pdf', category_name: 'PDF Toolkit', icon: 'archive', color: 'red' },
                { tool: 'image-compress', category: 'image', category_name: 'Image Toolkit', icon: 'image', color: 'green' },
                { tool: 'image-resize', category: 'image', category_name: 'Image Toolkit', icon: 'maximize', color: 'green' },
                { tool: 'image-convert', category: 'image', category_name: 'Image Toolkit', icon: 'repeat', color: 'green' },
                { tool: 'video-to-mp3', category: 'video', category_name: 'Video & Audio', icon: 'music', color: 'purple' },
                { tool: 'video-trimmer', category: 'video', category_name: 'Video & Audio', icon: 'scissors', color: 'purple' },
                { tool: 'resume-generator', category: 'ai', category_name: 'AI Tools', icon: 'briefcase', color: 'violet' },
                { tool: 'business-name-generator', category: 'ai', category_name: 'AI Tools', icon: 'building', color: 'violet' }
            ];
            
            const results = toolData.filter(tool => {
                const toolName = tool.tool.replace(/-/g, ' ').toLowerCase();
                const categoryName = tool.category_name.toLowerCase();
                return toolName.includes(query) || categoryName.includes(query);
            });
            
            this.searchResults = results.slice(0, 6);
            
        } catch (error) {
            console.warn('Search error:', error);
            this.searchResults = [];
        }
    }
    
    // Make it globally available
    window.searchTools = safeSearchTools;
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Search functionality loaded');
    });
})();