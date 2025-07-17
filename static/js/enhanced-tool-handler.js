
// Enhanced Tool Handler with Real API Integration
class EnhancedToolHandler {
    constructor() {
        this.apiBase = '/api/v2';
        this.currentTool = this.getCurrentTool();
        this.initializeHandler();
    }

    getCurrentTool() {
        const path = window.location.pathname;
        const toolMatch = path.match(/\/tools\/([^\/]+)/);
        return toolMatch ? toolMatch[1] : '';
    }

    initializeHandler() {
        console.log(`🚀 Initializing Enhanced Tool Handler for: ${this.currentTool}`);
        
        // Initialize file handling
        this.setupFileHandling();
        
        // Initialize form handling
        this.setupFormHandling();
        
        // Initialize API calls
        this.setupAPIIntegration();
    }

    setupFileHandling() {
        const fileInput = document.getElementById('file-input');
        const uploadZone = document.getElementById('upload-zone');
        const fileList = document.getElementById('file-list');

        if (!uploadZone || !fileInput) return;

        let selectedFiles = [];

        // Drag and drop handlers
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('border-blue-500', 'bg-blue-50');
        });

        uploadZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('border-blue-500', 'bg-blue-50');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('border-blue-500', 'bg-blue-50');
            this.handleFiles(e.dataTransfer.files);
        });

        uploadZone.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });

        this.handleFiles = (files) => {
            selectedFiles = Array.from(files);
            this.displayFiles(selectedFiles);
            this.updateProcessButton();
        };

        this.selectedFiles = selectedFiles;
    }

    displayFiles(files) {
        const fileList = document.getElementById('file-list');
        if (!fileList) return;

        fileList.innerHTML = '';
        fileList.classList.remove('hidden');

        files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-lg mb-2';
            fileItem.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i data-lucide="file" class="w-4 h-4 text-gray-500"></i>
                    <div>
                        <span class="text-sm text-gray-900">${file.name}</span>
                        <span class="text-xs text-gray-500 ml-2">(${this.formatFileSize(file.size)})</span>
                    </div>
                </div>
                <button type="button" onclick="enhancedToolHandler.removeFile(${index})" 
                        class="text-red-500 hover:text-red-700">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            `;
            fileList.appendChild(fileItem);
        });

        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    removeFile(index) {
        this.selectedFiles.splice(index, 1);
        this.displayFiles(this.selectedFiles);
        this.updateProcessButton();
    }

    updateProcessButton() {
        const processBtn = document.getElementById('process-btn');
        if (processBtn) {
            processBtn.disabled = this.selectedFiles.length === 0 && this.requiresFiles();
        }
    }

    requiresFiles() {
        const fileRequiredTools = [
            'pdf-merge', 'pdf-split', 'pdf-compress',
            'image-compress', 'image-resize', 'image-convert',
            'video-to-mp3', 'video-trimmer'
        ];
        return fileRequiredTools.includes(this.currentTool);
    }

    setupFormHandling() {
        const toolForm = document.getElementById('tool-form');
        if (!toolForm) return;

        toolForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.processFiles();
        });

        const resetBtn = document.getElementById('reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetForm();
            });
        }
    }

    async processFiles() {
        console.log(`🔄 Processing ${this.currentTool}...`);

        // Show processing section
        this.showProcessingSection();

        try {
            // Get API endpoint
            const endpoint = this.getAPIEndpoint();
            
            // Prepare form data
            const formData = new FormData();
            
            // Add files if required
            if (this.selectedFiles && this.selectedFiles.length > 0) {
                if (this.selectedFiles.length === 1) {
                    formData.append('file', this.selectedFiles[0]);
                } else {
                    this.selectedFiles.forEach(file => {
                        formData.append('files', file);
                    });
                }
            }

            // Add form fields
            const form = document.getElementById('tool-form');
            if (form) {
                const formFields = new FormData(form);
                for (let [key, value] of formFields.entries()) {
                    if (key !== 'files' && key !== 'file') {
                        formData.append(key, value);
                    }
                }
            }

            // Make API call
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error || 'Processing failed');
            }

        } catch (error) {
            console.error('Processing error:', error);
            this.showError('Network error occurred');
        }
    }

    getAPIEndpoint() {
        const endpoints = {
            'pdf-merge': `${this.apiBase}/pdf/merge`,
            'pdf-split': `${this.apiBase}/pdf/split`,
            'pdf-compress': `${this.apiBase}/pdf/compress`,
            'image-compress': `${this.apiBase}/image/compress`,
            'image-resize': `${this.apiBase}/image/resize`,
            'video-to-mp3': `${this.apiBase}/video/extract-audio`,
            'resume-generator': `${this.apiBase}/ai/generate-resume`,
            'business-name-generator': `${this.apiBase}/ai/generate-business-names`,
            'qr-generator': `${this.apiBase}/utility/generate-qr`
        };

        return endpoints[this.currentTool] || `${this.apiBase}/generic/${this.currentTool}`;
    }

    showProcessingSection() {
        const processingSection = document.getElementById('processing-section');
        const resultsSection = document.getElementById('results-section');

        if (processingSection) {
            processingSection.classList.remove('hidden');
            this.simulateProgress();
        }

        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
    }

    async simulateProgress() {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');

        if (!progressBar || !progressText) return;

        for (let i = 0; i <= 100; i += Math.random() * 15) {
            const progress = Math.min(i, 100);
            progressBar.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '%';
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }

    showResults(result) {
        const processingSection = document.getElementById('processing-section');
        const resultsSection = document.getElementById('results-section');
        const downloadLinks = document.getElementById('download-links');

        if (processingSection) {
            processingSection.classList.add('hidden');
        }

        if (resultsSection) {
            resultsSection.classList.remove('hidden');
        }

        if (downloadLinks) {
            let linksHTML = '';

            if (result.download_url) {
                linksHTML = `
                    <a href="${result.download_url}" 
                       class="inline-flex items-center px-6 py-3 bg-green-600 text-white font-medium rounded-xl hover:bg-green-700 transition-colors shadow-lg">
                        <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                        Download ${result.filename}
                    </a>
                `;
            } else if (result.files) {
                linksHTML = result.files.map(file => `
                    <a href="${file.download_url}" 
                       class="inline-flex items-center px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors mr-2 mb-2">
                        <i data-lucide="download" class="w-4 h-4 mr-2"></i>
                        ${file.filename}
                    </a>
                `).join('');
            } else if (result.business_names) {
                linksHTML = `
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        ${result.business_names.map(name => `
                            <div class="p-3 bg-gray-100 rounded-lg text-center">
                                ${name}
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            linksHTML += `
                <div class="mt-4">
                    <button onclick="enhancedToolHandler.resetForm()" 
                            class="text-blue-600 hover:text-blue-700 font-medium">
                        Process Another File
                    </button>
                </div>
            `;

            downloadLinks.innerHTML = linksHTML;

            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    showError(message) {
        const processingSection = document.getElementById('processing-section');
        const resultsSection = document.getElementById('results-section');

        if (processingSection) {
            processingSection.classList.add('hidden');
        }

        if (resultsSection) {
            resultsSection.classList.remove('hidden');
            resultsSection.innerHTML = `
                <div class="text-center space-y-6">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full">
                        <i data-lucide="alert-circle" class="w-8 h-8 text-red-600"></i>
                    </div>
                    <div>
                        <h3 class="text-xl font-semibold text-gray-900 mb-2">Error</h3>
                        <p class="text-red-600">${message}</p>
                    </div>
                    <button onclick="enhancedToolHandler.resetForm()" 
                            class="px-6 py-3 bg-gray-600 text-white font-medium rounded-xl hover:bg-gray-700 transition-colors">
                        Try Again
                    </button>
                </div>
            `;

            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    resetForm() {
        // Reset files
        this.selectedFiles = [];
        
        // Hide sections
        const processingSection = document.getElementById('processing-section');
        const resultsSection = document.getElementById('results-section');
        const fileList = document.getElementById('file-list');

        if (processingSection) processingSection.classList.add('hidden');
        if (resultsSection) resultsSection.classList.add('hidden');
        if (fileList) fileList.classList.add('hidden');

        // Reset form
        const form = document.getElementById('tool-form');
        if (form) form.reset();

        // Reset file input
        const fileInput = document.getElementById('file-input');
        if (fileInput) fileInput.value = '';

        // Update button state
        this.updateProcessButton();

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    setupAPIIntegration() {
        // Add any additional API setup here
        console.log('✅ API integration setup complete');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.enhancedToolHandler = new EnhancedToolHandler();
});

// Fallback for immediate access
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        if (!window.enhancedToolHandler) {
            window.enhancedToolHandler = new EnhancedToolHandler();
        }
    });
} else {
    if (!window.enhancedToolHandler) {
        window.enhancedToolHandler = new EnhancedToolHandler();
    }
}

console.log('🚀 Enhanced Tool Handler loaded');
