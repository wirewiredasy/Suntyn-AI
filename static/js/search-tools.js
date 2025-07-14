// Enhanced search functionality for tools
class ToolSearchManager {
    constructor() {
        this.tools = [];
        this.searchIndex = new Map();
        this.initializeSearch();
    }

    initializeSearch() {
        // Load tools from config
        this.loadToolsFromConfig();
        this.buildSearchIndex();
        this.setupSearchHandlers();
    }

    loadToolsFromConfig() {
        // This would be populated from the server-side config
        this.tools = [
            // PDF Tools
            { name: 'pdf-merge', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Combine multiple PDF files into one document' },
            { name: 'pdf-split', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Split PDF into multiple files or pages' },
            { name: 'pdf-compress', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Reduce PDF file size without quality loss' },
            { name: 'pdf-to-word', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Convert PDF to Word document' },
            { name: 'word-to-pdf', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Convert Word document to PDF' },
            { name: 'pdf-to-jpg', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Convert PDF pages to JPG images' },
            { name: 'jpg-to-pdf', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Convert JPG images to PDF' },
            { name: 'pdf-watermark', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Add watermark to PDF documents' },
            { name: 'pdf-page-numbers', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Add page numbers to PDF' },
            { name: 'pdf-unlock', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Remove password from PDF' },
            { name: 'pdf-protect', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Add password protection to PDF' },
            { name: 'pdf-rotate', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Rotate PDF pages' },
            { name: 'pdf-extract-pages', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Extract specific pages from PDF' },
            { name: 'pdf-chat', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Chat with PDF using AI' },
            { name: 'pdf-summarize', category: 'pdf', categoryName: 'PDF Toolkit', icon: 'file-text', color: 'red', description: 'Summarize PDF content with AI' },
            
            // Image Tools
            { name: 'image-compress', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Reduce image file size while maintaining quality' },
            { name: 'image-resize', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Resize images to specific dimensions' },
            { name: 'image-convert', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Convert images between formats' },
            { name: 'image-crop', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Crop images to specific dimensions' },
            { name: 'image-rotate', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Rotate images by specified angle' },
            { name: 'image-ocr', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Extract text from images' },
            { name: 'background-remover', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Remove background from images' },
            { name: 'meme-generator', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Create memes with text overlays' },
            { name: 'image-watermark', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Add watermark to images' },
            { name: 'signature-extractor', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Extract signatures from documents' },
            { name: 'image-enhancer', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Enhance image quality with AI' },
            { name: 'color-picker', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Pick colors from images' },
            { name: 'social-crop', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Crop images for social media' },
            { name: 'image-caption', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Generate captions for images' },
            { name: 'profile-pic-maker', category: 'image', categoryName: 'Image Toolkit', icon: 'image', color: 'green', description: 'Create professional profile pictures' },
            
            // Video Tools
            { name: 'video-to-mp3', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Extract audio from video files' },
            { name: 'audio-remover', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Remove audio from video files' },
            { name: 'video-trimmer', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Trim video clips with precision' },
            { name: 'voice-remover', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Remove vocals from audio' },
            { name: 'subtitle-generator', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Generate subtitles for videos' },
            { name: 'subtitle-merger', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Merge subtitles with video' },
            { name: 'video-compress', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Compress video files' },
            { name: 'video-converter', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Convert video formats' },
            { name: 'dubbing-tool', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Add voice dubbing to videos' },
            { name: 'shorts-cropper', category: 'video', categoryName: 'Video & Audio', icon: 'video', color: 'purple', description: 'Crop videos for shorts format' },
            
            // AI Tools
            { name: 'resume-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate professional resumes with AI' },
            { name: 'business-name-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate creative business names' },
            { name: 'blog-title-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate catchy blog titles' },
            { name: 'product-description', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate product descriptions' },
            { name: 'script-writer', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Write scripts for videos' },
            { name: 'ad-copy-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate advertising copy' },
            { name: 'faq-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate FAQ sections' },
            { name: 'idea-explainer', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Explain complex ideas simply' },
            { name: 'bio-generator', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Generate professional bios' },
            { name: 'doc-to-slides', category: 'ai', categoryName: 'AI Tools', icon: 'brain', color: 'violet', description: 'Convert documents to slides' },
            
            // Add more tools from other categories...
        ];
    }

    buildSearchIndex() {
        this.tools.forEach(tool => {
            const searchTerms = [
                tool.name.toLowerCase(),
                tool.name.replace('-', ' ').toLowerCase(),
                tool.description.toLowerCase(),
                tool.categoryName.toLowerCase(),
                tool.category.toLowerCase()
            ];

            searchTerms.forEach(term => {
                const words = term.split(' ');
                words.forEach(word => {
                    if (word.length > 2) {
                        if (!this.searchIndex.has(word)) {
                            this.searchIndex.set(word, new Set());
                        }
                        this.searchIndex.get(word).add(tool);
                    }
                });
            });
        });
    }

    search(query) {
        if (!query || query.length < 2) {
            return [];
        }

        const normalizedQuery = query.toLowerCase().trim();
        const queryWords = normalizedQuery.split(/\s+/);
        const results = new Map();

        queryWords.forEach(word => {
            // Exact matches
            if (this.searchIndex.has(word)) {
                this.searchIndex.get(word).forEach(tool => {
                    if (!results.has(tool.name)) {
                        results.set(tool.name, { tool, score: 0 });
                    }
                    results.get(tool.name).score += 10;
                });
            }

            // Partial matches
            this.searchIndex.forEach((tools, indexWord) => {
                if (indexWord.includes(word) && indexWord !== word) {
                    tools.forEach(tool => {
                        if (!results.has(tool.name)) {
                            results.set(tool.name, { tool, score: 0 });
                        }
                        results.get(tool.name).score += 5;
                    });
                }
            });
        });

        // Sort by score and return top results
        return Array.from(results.values())
            .sort((a, b) => b.score - a.score)
            .slice(0, 10)
            .map(result => result.tool);
    }

    setupSearchHandlers() {
        // Global search functionality
        window.searchTools = (query) => {
            if (!query) return [];
            return this.search(query);
        };

        // Initialize search on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeSearchUI();
        });
    }

    initializeSearchUI() {
        // Add search functionality to existing search inputs
        const searchInputs = document.querySelectorAll('input[type="text"]');
        searchInputs.forEach(input => {
            if (input.placeholder && input.placeholder.toLowerCase().includes('search')) {
                this.attachSearchToInput(input);
            }
        });
    }

    attachSearchToInput(input) {
        let searchTimeout;
        
        input.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = e.target.value;
                const results = this.search(query);
                this.displaySearchResults(results, input);
            }, 300);
        });

        input.addEventListener('focus', () => {
            if (input.value) {
                const results = this.search(input.value);
                this.displaySearchResults(results, input);
            }
        });
    }

    displaySearchResults(results, input) {
        // Remove existing results
        const existingResults = document.querySelector('.search-results-dropdown');
        if (existingResults) {
            existingResults.remove();
        }

        if (results.length === 0) return;

        // Create results dropdown
        const dropdown = document.createElement('div');
        dropdown.className = 'search-results-dropdown absolute w-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-y-auto';
        
        results.forEach(tool => {
            const item = document.createElement('a');
            item.href = `/tools/${tool.name}`;
            item.className = 'block px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 last:border-b-0';
            
            item.innerHTML = `
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-lg bg-${tool.color}-100 dark:bg-${tool.color}-900 flex items-center justify-center">
                        <i data-lucide="${tool.icon}" class="w-4 h-4 text-${tool.color}-600 dark:text-${tool.color}-400"></i>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-900 dark:text-white">
                            ${tool.name.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">
                            ${tool.categoryName} • ${tool.description}
                        </div>
                    </div>
                </div>
            `;
            
            dropdown.appendChild(item);
        });

        // Position dropdown
        const inputRect = input.getBoundingClientRect();
        const container = input.closest('.relative') || input.parentElement;
        container.style.position = 'relative';
        container.appendChild(dropdown);

        // Initialize Lucide icons
        if (window.lucide) {
            window.lucide.createIcons();
        }

        // Close dropdown when clicking outside
        const closeDropdown = (e) => {
            if (!container.contains(e.target)) {
                dropdown.remove();
                document.removeEventListener('click', closeDropdown);
            }
        };
        
        setTimeout(() => {
            document.addEventListener('click', closeDropdown);
        }, 100);
    }
}

// Initialize search manager
const toolSearchManager = new ToolSearchManager();

// Export for use in Alpine.js components
window.toolSearchManager = toolSearchManager;