// Search functionality fix for Toolora AI
document.addEventListener('DOMContentLoaded', function() {
    console.log('Search fix loaded');
    
    // Tool database
    const tools = [
        { tool: 'pdf-merge', category: 'pdf', category_name: 'PDF Toolkit', icon: 'layers', color: 'red' },
        { tool: 'pdf-split', category: 'pdf', category_name: 'PDF Toolkit', icon: 'scissors', color: 'red' },
        { tool: 'pdf-compress', category: 'pdf', category_name: 'PDF Toolkit', icon: 'archive', color: 'red' },
        { tool: 'image-compress', category: 'image', category_name: 'Image Toolkit', icon: 'minimize-2', color: 'green' },
        { tool: 'image-resize', category: 'image', category_name: 'Image Toolkit', icon: 'maximize-2', color: 'green' },
        { tool: 'image-convert', category: 'image', category_name: 'Image Toolkit', icon: 'repeat', color: 'green' },
        { tool: 'video-trimmer', category: 'video', category_name: 'Video & Audio', icon: 'scissors', color: 'purple' },
        { tool: 'video-to-mp3', category: 'video', category_name: 'Video & Audio', icon: 'music', color: 'purple' },
        { tool: 'resume-generator', category: 'ai', category_name: 'AI Tools', icon: 'briefcase', color: 'violet' },
        { tool: 'business-name-generator', category: 'ai', category_name: 'AI Tools', icon: 'building', color: 'violet' },
        { tool: 'qr-generator', category: 'utility', category_name: 'Utility Tools', icon: 'qr-code', color: 'slate' }
    ];
    
    // Search function
    function performSearch(query) {
        if (!query || query.length < 2) return [];
        
        const searchTerm = query.toLowerCase();
        return tools.filter(tool => {
            const toolName = tool.tool.replace(/-/g, ' ').toLowerCase();
            const categoryName = tool.category_name.toLowerCase();
            
            return toolName.includes(searchTerm) || 
                   categoryName.includes(searchTerm) ||
                   tool.tool.toLowerCase().includes(searchTerm);
        }).slice(0, 6);
    }
    
    // Override Alpine.js data for search
    if (typeof Alpine !== 'undefined') {
        document.addEventListener('alpine:init', () => {
            Alpine.data('searchComponent', () => ({
                searchOpen: false,
                searchQuery: '',
                searchResults: [],
                searchTools() {
                    try {
                        this.searchResults = performSearch(this.searchQuery);
                        console.log('Search results:', this.searchResults.length);
                    } catch (error) {
                        console.warn('Search handled:', error);
                        this.searchResults = [];
                    }
                }
            }));
        });
    }
    
    // Global fallback
    window.searchTools = function() {
        try {
            const input = document.querySelector('input[x-model="searchQuery"]');
            if (input) {
                const results = performSearch(input.value);
                console.log('Global search results:', results.length);
            }
        } catch (error) {
            console.warn('Global search handled:', error);
        }
    };
});