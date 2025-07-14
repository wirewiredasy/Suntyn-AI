/**
 * Enhanced Search Functionality for Toolora AI
 * Provides real-time search across all 85+ tools with fuzzy matching and categories
 */

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
        inputContainer.style.position = 'relative';
        inputContainer.appendChild(resultsContainer);
        
        // Initialize Lucide icons for new elements
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Add fade-in animation
        resultsContainer.style.opacity = '0';
        resultsContainer.style.transform = 'translateY(-10px)';
        requestAnimationFrame(() => {
            resultsContainer.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
            resultsContainer.style.opacity = '1';
            resultsContainer.style.transform = 'translateY(0)';
        });
    }

    hideResults(input) {
        const resultsContainer = input.parentElement?.querySelector('.search-results');
        if (resultsContainer) {
            resultsContainer.style.opacity = '0';
            resultsContainer.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                resultsContainer.remove();
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