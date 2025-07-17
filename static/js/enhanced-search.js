/**
 * Enhanced Search Functionality for Toolora AI
 * Provides real-time search across all 85+ tools with fuzzy matching and categories
 */

class EnhancedToolSearch {
    constructor() {
        this.tools = [];
        this.searchIndex = new Map();
        this.minSearchLength = 2;
        this.maxResults = 8;
        this.init();
    }

    init() {
        this.loadTools();
        this.buildSearchIndex();
        this.setupSearchHandlers();
        console.log('Enhanced search functionality initialized');
    }

    loadTools() {
        // Complete tools database
        this.tools = [
            // PDF Tools
            { id: 'pdf-merge', name: 'PDF Merge', category: 'PDF', description: 'Merge multiple PDF files into one document', keywords: ['combine', 'join', 'merge', 'pdf'] },
            { id: 'pdf-split', name: 'PDF Split', category: 'PDF', description: 'Split PDF into multiple files or pages', keywords: ['split', 'divide', 'separate', 'pdf'] },
            { id: 'pdf-compress', name: 'PDF Compress', category: 'PDF', description: 'Reduce PDF file size without quality loss', keywords: ['compress', 'reduce', 'optimize', 'pdf'] },
            { id: 'pdf-to-word', name: 'PDF to Word', category: 'PDF', description: 'Convert PDF to Word document', keywords: ['convert', 'pdf', 'word', 'doc'] },
            { id: 'pdf-to-jpg', name: 'PDF to JPG', category: 'PDF', description: 'Convert PDF pages to JPG images', keywords: ['convert', 'pdf', 'jpg', 'image'] },
            { id: 'word-to-pdf', name: 'Word to PDF', category: 'PDF', description: 'Convert Word document to PDF', keywords: ['convert', 'word', 'pdf', 'doc'] },
            { id: 'jpg-to-pdf', name: 'JPG to PDF', category: 'PDF', description: 'Convert JPG images to PDF', keywords: ['convert', 'jpg', 'pdf', 'image'] },
            
            // Image Tools
            { id: 'image-compress', name: 'Image Compress', category: 'Image', description: 'Reduce image file size while maintaining quality', keywords: ['compress', 'optimize', 'reduce', 'image'] },
            { id: 'image-resize', name: 'Image Resize', category: 'Image', description: 'Resize images to specific dimensions', keywords: ['resize', 'scale', 'dimensions', 'image'] },
            { id: 'image-convert', name: 'Image Convert', category: 'Image', description: 'Convert images between different formats', keywords: ['convert', 'format', 'jpg', 'png', 'webp'] },
            { id: 'background-remover', name: 'Background Remover', category: 'Image', description: 'Remove background from images', keywords: ['background', 'remove', 'transparent', 'cut'] },
            { id: 'image-crop', name: 'Image Crop', category: 'Image', description: 'Crop images to desired size', keywords: ['crop', 'cut', 'trim', 'image'] },
            
            // Video Tools
            { id: 'video-to-mp3', name: 'Video to MP3', category: 'Video', description: 'Extract audio from video files', keywords: ['extract', 'audio', 'mp3', 'video'] },
            { id: 'video-trimmer', name: 'Video Trimmer', category: 'Video', description: 'Trim video clips with precision', keywords: ['trim', 'cut', 'clip', 'video'] },
            { id: 'video-compress', name: 'Video Compress', category: 'Video', description: 'Compress video files', keywords: ['compress', 'reduce', 'optimize', 'video'] },
            
            // AI Tools
            { id: 'resume-generator', name: 'Resume Generator', category: 'AI', description: 'Generate professional resumes with AI', keywords: ['resume', 'cv', 'generate', 'ai'] },
            { id: 'business-name-generator', name: 'Business Name Generator', category: 'AI', description: 'Generate creative business names', keywords: ['business', 'name', 'generate', 'company'] },
            { id: 'blog-title-generator', name: 'Blog Title Generator', category: 'AI', description: 'Generate catchy blog titles', keywords: ['blog', 'title', 'generate', 'content'] }
        ];
    }

    buildSearchIndex() {
        this.tools.forEach(tool => {
            const searchTerms = [
                tool.name.toLowerCase(),
                tool.category.toLowerCase(),
                tool.description.toLowerCase(),
                ...tool.keywords
            ];

            searchTerms.forEach(term => {
                const words = term.split(/\s+/);
                words.forEach(word => {
                    if (word.length >= 2) {
                        if (!this.searchIndex.has(word)) {
                            this.searchIndex.set(word, new Set());
                        }
                        this.searchIndex.get(word).add(tool);
                    }
                });
            });
        });
    }

    fuzzySearch(query) {
        const normalizedQuery = query.toLowerCase().trim();
        if (normalizedQuery.length < this.minSearchLength) return [];

        const results = new Map();
        const queryWords = normalizedQuery.split(/\s+/);

        queryWords.forEach(queryWord => {
            // Exact matches
            if (this.searchIndex.has(queryWord)) {
                this.searchIndex.get(queryWord).forEach(tool => {
                    if (!results.has(tool.id)) {
                        results.set(tool.id, { tool, score: 0 });
                    }
                    results.get(tool.id).score += 10;
                });
            }

            // Partial matches
            this.searchIndex.forEach((tools, indexWord) => {
                if (indexWord.includes(queryWord) || queryWord.includes(indexWord)) {
                    tools.forEach(tool => {
                        if (!results.has(tool.id)) {
                            results.set(tool.id, { tool, score: 0 });
                        }
                        results.get(tool.id).score += 5;
                    });
                }
            });

            // Fuzzy matches (edit distance)
            this.searchIndex.forEach((tools, indexWord) => {
                const distance = this.levenshteinDistance(queryWord, indexWord);
                if (distance <= 2 && distance > 0) {
                    tools.forEach(tool => {
                        if (!results.has(tool.id)) {
                            results.set(tool.id, { tool, score: 0 });
                        }
                        results.get(tool.id).score += Math.max(1, 3 - distance);
                    });
                }
            });
        });

        return Array.from(results.values())
            .sort((a, b) => b.score - a.score)
            .slice(0, this.maxResults)
            .map(result => result.tool);
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i-1) === str1.charAt(j-1)) {
                    matrix[i][j] = matrix[i-1][j-1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i-1][j-1] + 1,
                        matrix[i][j-1] + 1,
                        matrix[i-1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    setupSearchHandlers() {
        document.addEventListener('DOMContentLoaded', () => {
            const searchInputs = document.querySelectorAll('input[placeholder*="Search"]');
            
            searchInputs.forEach(input => {
                this.attachSearchToInput(input);
            });
        });

        // Global search function
        window.enhancedSearch = (query) => {
            return this.fuzzySearch(query);
        };
    }

    attachSearchToInput(input) {
        let debounceTimer;
        
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const query = e.target.value;
                const results = this.fuzzySearch(query);
                this.displayResults(results, input);
            }, 300);
        });

        input.addEventListener('focus', () => {
            if (input.value.length >= this.minSearchLength) {
                const results = this.fuzzySearch(input.value);
                this.displayResults(results, input);
            }
        });
    }

    displayResults(results, input) {
        // Remove existing dropdown
        const existingDropdown = document.querySelector('.search-dropdown');
        if (existingDropdown) {
            existingDropdown.remove();
        }

        if (results.length === 0) return;

        // Create dropdown
        const dropdown = document.createElement('div');
        dropdown.className = 'search-dropdown absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-y-auto';

        results.forEach((tool, index) => {
            const item = document.createElement('a');
            item.href = `/tools/${tool.id}`;
            item.className = 'flex items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 last:border-b-0 transition-colors';

            item.innerHTML = `
                <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center mr-3">
                    <span class="text-blue-600 dark:text-blue-400 font-bold text-sm">${tool.category[0]}</span>
                </div>
                <div class="flex-1">
                    <div class="font-medium text-gray-900 dark:text-white">
                        ${tool.name}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                        ${tool.category} • ${tool.description}
                    </div>
                </div>
            `;

            dropdown.appendChild(item);
        });

        // Position dropdown
        const container = input.closest('.relative') || input.parentElement;
        if (container && !container.style.position) {
            container.style.position = 'relative';
        }
        if (container) {
            container.appendChild(dropdown);
        }

        // Close on click outside
        const closeHandler = (e) => {
            if (!container.contains(e.target)) {
                dropdown.remove();
                document.removeEventListener('click', closeHandler);
            }
        };

        setTimeout(() => {
            document.addEventListener('click', closeHandler);
        }, 100);
    }
}

// Initialize enhanced search
const enhancedToolSearch = new EnhancedToolSearch();
window.enhancedToolSearch = enhancedToolSearch;

class EnhancedSearch {
    constructor() {
        this.tools = [];
        this.categories = {};
        this.searchCache = new Map();
        this.init();
    }

    async init() {
        await this.loadToolsData();
        this.setupSearchHandlers();
        this.initializeSearchUI();
    }

    async loadToolsData() {
        // Load tools from config data (passed from backend)
        if (typeof window.toolsConfig !== 'undefined') {
            this.categories = window.toolsConfig;
        }

        // Build searchable tools array
        this.tools = [];
        Object.entries(this.categories).forEach(([categoryId, categoryData]) => {
            categoryData.tools.forEach(tool => {
                this.tools.push({
                    name: tool,
                    displayName: tool.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()),
                    category: categoryId,
                    categoryName: categoryData.name,
                    icon: categoryData.icon,
                    color: categoryData.color,
                    description: this.getToolDescription(tool),
                    keywords: this.generateKeywords(tool, categoryData.name)
                });
            });
        });
    }

    getToolDescription(tool) {
        const descriptions = {
            'pdf-merge': 'Combine multiple PDF files into one document seamlessly',
            'pdf-split': 'Split PDF into multiple files or individual pages',
            'pdf-compress': 'Reduce PDF file size without quality loss using advanced compression',
            'pdf-to-word': 'Convert PDF files to editable Word documents',
            'word-to-pdf': 'Convert Word documents to professional PDF files',
            'pdf-to-jpg': 'Convert PDF pages to high-quality JPG images',
            'jpg-to-pdf': 'Convert JPG images to PDF documents',
            'pdf-watermark': 'Add custom watermarks to PDF documents',
            'pdf-page-numbers': 'Add page numbers to PDF documents',
            'pdf-unlock': 'Remove password protection from PDF files',
            'pdf-protect': 'Add password protection to PDF files',
            'pdf-rotate': 'Rotate PDF pages to correct orientation',
            'pdf-extract-pages': 'Extract specific pages from PDF documents',
            'pdf-chat': 'Chat with your PDF using AI technology',
            'pdf-summarize': 'Generate AI-powered summaries of PDF content',
            'image-compress': 'Reduce image file size while maintaining quality',
            'image-resize': 'Resize images to specific dimensions perfectly',
            'image-convert': 'Convert between different image formats',
            'image-crop': 'Crop images to focus on important areas',
            'image-rotate': 'Rotate images to correct orientation',
            'image-ocr': 'Extract text from images using OCR technology',
            'background-remover': 'Remove backgrounds from images automatically',
            'meme-generator': 'Create hilarious memes with custom text',
            'image-watermark': 'Add watermarks to protect your images',
            'signature-extractor': 'Extract signatures from documents',
            'image-enhancer': 'Enhance image quality with AI technology',
            'color-picker': 'Pick colors from images and get color codes',
            'social-crop': 'Crop images for social media platforms',
            'image-caption': 'Generate captions for images using AI',
            'profile-pic-maker': 'Create professional profile pictures',
            'video-to-mp3': 'Extract audio from video files as MP3',
            'audio-remover': 'Remove audio tracks from video files',
            'video-trimmer': 'Trim and cut video clips with precision',
            'voice-remover': 'Remove vocals from audio files',
            'subtitle-generator': 'Generate subtitles for videos automatically',
            'subtitle-merger': 'Merge subtitle files with videos',
            'video-compress': 'Compress videos to reduce file size',
            'video-converter': 'Convert videos between different formats',
            'dubbing-tool': 'Add dubbing to videos professionally',
            'shorts-cropper': 'Crop videos for social media shorts',
            'resume-generator': 'Create professional resumes with AI assistance',
            'business-name-generator': 'Generate unique business names using AI',
            'blog-title-generator': 'Create engaging blog titles with AI',
            'product-description': 'Write compelling product descriptions',
            'script-writer': 'Generate scripts for videos and presentations',
            'ad-copy-generator': 'Create persuasive advertising copy',
            'faq-generator': 'Generate FAQ sections for websites',
            'idea-explainer': 'Explain complex ideas in simple terms',
            'bio-generator': 'Create professional bios for social media',
            'doc-to-slides': 'Convert documents to presentation slides',
            'qr-generator': 'Generate QR codes for various purposes',
            'barcode-generator': 'Create barcodes for products',
            'text-case-converter': 'Convert text between different cases',
            'age-bmi-calculator': 'Calculate age and BMI accurately',
            'password-generator': 'Generate secure passwords',
            'clipboard-notepad': 'Digital notepad for quick notes',
            'file-renamer': 'Rename multiple files efficiently',
            'url-shortener': 'Create short URLs for sharing',
            'text-to-image': 'Convert text to images with styling',
            'zip-unzip': 'Compress and extract ZIP files',
            'loan-emi-calculator': 'Calculate loan EMI and interest',
            'gst-calculator': 'Calculate GST for Indian businesses',
            'currency-converter': 'Convert between world currencies',
            'budget-planner': 'Plan and track your budget',
            'income-tax-estimator': 'Estimate income tax calculations'
        };
        return descriptions[tool] || `Professional ${tool.replace('-', ' ')} tool for your needs`;
    }

    generateKeywords(tool, categoryName) {
        const baseKeywords = [
            tool,
            tool.replace('-', ' '),
            categoryName.toLowerCase(),
            ...tool.split('-'),
            ...categoryName.split(' ').map(word => word.toLowerCase())
        ];

        // Add specific keywords based on tool type
        const additionalKeywords = {
            'pdf': ['document', 'file', 'portable', 'adobe'],
            'image': ['photo', 'picture', 'graphic', 'visual'],
            'video': ['movie', 'clip', 'recording', 'media'],
            'ai': ['artificial', 'intelligence', 'smart', 'auto'],
            'govt': ['government', 'official', 'document', 'indian'],
            'student': ['education', 'study', 'learning', 'academic'],
            'finance': ['money', 'calculation', 'financial', 'economy'],
            'utility': ['tool', 'helper', 'general', 'misc']
        };

        Object.entries(additionalKeywords).forEach(([category, keywords]) => {
            if (tool.includes(category) || categoryName.toLowerCase().includes(category)) {
                baseKeywords.push(...keywords);
            }
        });

        return [...new Set(baseKeywords)];
    }

    setupSearchHandlers() {
        // Homepage search
        const homeSearchInput = document.querySelector('input[placeholder*="Search from 85+ tools"]');
        if (homeSearchInput) {
            this.attachSearchToInput(homeSearchInput, 'home');
        }

        // Tools page search
        const toolsSearchInput = document.querySelector('input[placeholder*="Search tools"]');
        if (toolsSearchInput) {
            this.attachSearchToInput(toolsSearchInput, 'tools');
        }
    }

    attachSearchToInput(input, context) {
        let debounceTimer;
        
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const query = e.target.value.trim();
                if (query.length >= 2) {
                    const results = this.search(query);
                    this.displayResults(results, input, context);
                } else {
                    this.hideResults(input);
                }
            }, 200);
        });

        input.addEventListener('focus', (e) => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                const results = this.search(query);
                this.displayResults(results, input, context);
            }
        });

        // Hide results when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !input.nextElementSibling?.contains(e.target)) {
                this.hideResults(input);
            }
        });
    }

    search(query) {
        // Check cache first
        const cacheKey = query.toLowerCase();
        if (this.searchCache.has(cacheKey)) {
            return this.searchCache.get(cacheKey);
        }

        const searchTerms = query.toLowerCase().split(' ').filter(term => term.length > 0);
        const results = [];

        this.tools.forEach(tool => {
            let score = 0;
            
            // Exact name match (highest priority)
            if (tool.name.toLowerCase() === query.toLowerCase()) {
                score += 100;
            }
            
            // Display name match
            if (tool.displayName.toLowerCase() === query.toLowerCase()) {
                score += 90;
            }
            
            // Check if all search terms are found
            const allTermsFound = searchTerms.every(term => {
                return tool.keywords.some(keyword => 
                    keyword.toLowerCase().includes(term) || 
                    this.fuzzyMatch(keyword.toLowerCase(), term)
                );
            });
            
            if (allTermsFound) {
                // Calculate relevance score
                searchTerms.forEach(term => {
                    // Exact keyword match
                    if (tool.keywords.some(keyword => keyword.toLowerCase() === term)) {
                        score += 50;
                    }
                    
                    // Partial keyword match
                    if (tool.keywords.some(keyword => keyword.toLowerCase().includes(term))) {
                        score += 30;
                    }
                    
                    // Category match
                    if (tool.categoryName.toLowerCase().includes(term)) {
                        score += 20;
                    }
                    
                    // Description match
                    if (tool.description.toLowerCase().includes(term)) {
                        score += 10;
                    }
                });
                
                results.push({ ...tool, score });
            }
        });

        // Sort by relevance score and limit results
        const sortedResults = results
            .sort((a, b) => b.score - a.score)
            .slice(0, 8);

        // Cache results
        this.searchCache.set(cacheKey, sortedResults);
        
        return sortedResults;
    }

    fuzzyMatch(str, pattern) {
        const patternLength = pattern.length;
        const strLength = str.length;
        
        if (patternLength > strLength) return false;
        if (patternLength === strLength) return str === pattern;
        
        let patternIndex = 0;
        for (let strIndex = 0; strIndex < strLength && patternIndex < patternLength; strIndex++) {
            if (str[strIndex] === pattern[patternIndex]) {
                patternIndex++;
            }
        }
        
        return patternIndex === patternLength;
    }

    displayResults(results, input, context) {
        // Remove existing results
        this.hideResults(input);
        
        if (results.length === 0) return;

        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-results absolute w-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-y-auto';
        resultsContainer.style.top = '100%';
        
        results.forEach((result, index) => {
            const resultElement = document.createElement('a');
            resultElement.href = `/tools/${result.name}`;
            resultElement.className = 'flex items-center space-x-4 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 last:border-b-0 transition-colors duration-200';
            
            resultElement.innerHTML = `
                <div class="w-10 h-10 rounded-xl bg-${result.color}-100 dark:bg-${result.color}-900 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="${result.icon}" class="w-5 h-5 text-${result.color}-600 dark:text-${result.color}-400"></i>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="font-semibold text-gray-900 dark:text-white">${result.displayName}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400 truncate">${result.description}</div>
                </div>
                <div class="text-xs text-${result.color}-600 dark:text-${result.color}-400 bg-${result.color}-50 dark:bg-${result.color}-900 px-2 py-1 rounded-full">
                    ${result.categoryName}
                </div>
            `;
            
            resultsContainer.appendChild(resultElement);
        });

        // Position container
        const inputContainer = input.parentElement;
        if (inputContainer) {
            inputContainer.style.position = 'relative';
            inputContainer.appendChild(resultsContainer);
        }
        
        // Initialize Lucide icons for new elements
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Add fade-in animation
        if (resultsContainer.style) {
            resultsContainer.style.opacity = '0';
            resultsContainer.style.transform = 'translateY(-10px)';
            requestAnimationFrame(() => {
                resultsContainer.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                resultsContainer.style.opacity = '1';
                resultsContainer.style.transform = 'translateY(0)';
            });
        }
    }

    hideResults(input) {
        const resultsContainer = input.parentElement?.querySelector('.search-results');
        if (resultsContainer && resultsContainer.style) {
            resultsContainer.style.opacity = '0';
            resultsContainer.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (resultsContainer && resultsContainer.parentElement) {
                    resultsContainer.remove();
                }
            }, 200);
        }
    }

    initializeSearchUI() {
        // Add loading states and enhanced UX
        document.querySelectorAll('input[type="text"]').forEach(input => {
            if (input.placeholder?.includes('Search')) {
                input.addEventListener('focus', () => {
                    input.parentElement?.classList.add('ring-2', 'ring-blue-500');
                });
                
                input.addEventListener('blur', () => {
                    setTimeout(() => {
                        input.parentElement?.classList.remove('ring-2', 'ring-blue-500');
                    }, 200);
                });
            }
        });
    }
}

// Initialize enhanced search when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.enhancedSearch = new EnhancedSearch();
});

// Export for global access
window.EnhancedSearch = EnhancedSearch;