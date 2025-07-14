/**
 * Enhanced Tool Handler - Comprehensive tool processing system
 * Handles all 85+ tools with advanced features and better UX
 */

class EnhancedToolHandler {
    constructor() {
        this.currentTool = null;
        this.uploadedFiles = [];
        this.processingQueue = [];
        this.maxFileSize = 50 * 1024 * 1024; // 50MB
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFileUpload();
        this.setupDragAndDrop();
        this.loadToolSpecificSettings();
    }

    setupEventListeners() {
        // File selection
        document.getElementById('file-select-btn')?.addEventListener('click', () => {
            document.getElementById('file-input').click();
        });

        // File input change
        document.getElementById('file-input')?.addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files);
        });

        // Process button
        document.getElementById('process-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.processFiles();
        });

        // Form submission
        document.getElementById('tool-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.processFiles();
        });
    }

    setupFileUpload() {
        const fileUploadArea = document.getElementById('file-upload-area');
        if (!fileUploadArea) return;

        // Enhanced drag and drop
        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            this.handleFileSelection(e.dataTransfer.files);
        });
    }

    setupDragAndDrop() {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            document.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });
    }

    loadToolSpecificSettings() {
        const toolName = document.querySelector('[data-tool-name]')?.dataset.toolName;
        if (!toolName) return;

        this.currentTool = toolName;
        this.setupToolSpecificOptions(toolName);
    }

    setupToolSpecificOptions(toolName) {
        const toolOptions = document.getElementById('tool-options');
        if (!toolOptions) return;

        // Show tool-specific options based on tool type
        const toolConfig = this.getToolConfig(toolName);
        if (toolConfig && toolConfig.options) {
            this.renderToolOptions(toolConfig.options, toolOptions);
        }
    }

    getToolConfig(toolName) {
        const configs = {
            // PDF Tools
            'pdf-merge': {
                acceptedTypes: ['.pdf'],
                maxFiles: 20,
                options: {
                    output_name: { type: 'text', label: 'Output Filename', default: 'merged_document' },
                    bookmark_pages: { type: 'checkbox', label: 'Add Page Bookmarks', default: false }
                }
            },
            'pdf-split': {
                acceptedTypes: ['.pdf'],
                maxFiles: 1,
                options: {
                    split_method: { 
                        type: 'select', 
                        label: 'Split Method', 
                        options: [
                            { value: 'pages', label: 'Split by Pages' },
                            { value: 'size', label: 'Split by File Size' },
                            { value: 'range', label: 'Extract Page Range' }
                        ]
                    },
                    page_range: { type: 'text', label: 'Page Range (e.g., 1-5,10-15)', default: '' }
                }
            },
            'pdf-compress': {
                acceptedTypes: ['.pdf'],
                maxFiles: 5,
                options: {
                    compression_level: {
                        type: 'select',
                        label: 'Compression Level',
                        options: [
                            { value: 'low', label: 'Low (Better Quality)' },
                            { value: 'medium', label: 'Medium (Balanced)' },
                            { value: 'high', label: 'High (Smaller Size)' }
                        ]
                    }
                }
            },
            
            // Image Tools
            'image-compress': {
                acceptedTypes: ['.jpg', '.jpeg', '.png', '.webp', '.bmp'],
                maxFiles: 10,
                options: {
                    quality: { type: 'range', label: 'Quality', min: 10, max: 100, default: 85 },
                    format: {
                        type: 'select',
                        label: 'Output Format',
                        options: [
                            { value: 'jpg', label: 'JPEG' },
                            { value: 'png', label: 'PNG' },
                            { value: 'webp', label: 'WebP' }
                        ]
                    }
                }
            },
            'image-resize': {
                acceptedTypes: ['.jpg', '.jpeg', '.png', '.webp', '.bmp'],
                maxFiles: 10,
                options: {
                    width: { type: 'number', label: 'Width (px)', default: 800 },
                    height: { type: 'number', label: 'Height (px)', default: 600 },
                    maintain_aspect: { type: 'checkbox', label: 'Maintain Aspect Ratio', default: true }
                }
            },
            'image-convert': {
                acceptedTypes: ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'],
                maxFiles: 10,
                options: {
                    format: {
                        type: 'select',
                        label: 'Convert To',
                        options: [
                            { value: 'jpg', label: 'JPEG' },
                            { value: 'png', label: 'PNG' },
                            { value: 'webp', label: 'WebP' },
                            { value: 'bmp', label: 'BMP' }
                        ]
                    }
                }
            },

            // Video Tools
            'video-to-mp3': {
                acceptedTypes: ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
                maxFiles: 3,
                options: {
                    quality: {
                        type: 'select',
                        label: 'Audio Quality',
                        options: [
                            { value: '128k', label: '128 kbps' },
                            { value: '192k', label: '192 kbps' },
                            { value: '320k', label: '320 kbps' }
                        ]
                    }
                }
            },
            'video-trimmer': {
                acceptedTypes: ['.mp4', '.avi', '.mov', '.wmv'],
                maxFiles: 1,
                options: {
                    start_time: { type: 'text', label: 'Start Time (mm:ss)', default: '00:00' },
                    end_time: { type: 'text', label: 'End Time (mm:ss)', default: '01:00' }
                }
            },

            // AI Tools
            'resume-generator': {
                acceptedTypes: [],
                maxFiles: 0,
                options: {
                    name: { type: 'text', label: 'Full Name', required: true },
                    email: { type: 'email', label: 'Email Address', required: true },
                    phone: { type: 'tel', label: 'Phone Number', required: true },
                    template: {
                        type: 'select',
                        label: 'Template Style',
                        options: [
                            { value: 'modern', label: 'Modern' },
                            { value: 'classic', label: 'Classic' },
                            { value: 'creative', label: 'Creative' }
                        ]
                    }
                }
            },
            'qr-generator': {
                acceptedTypes: [],
                maxFiles: 0,
                options: {
                    content: { type: 'textarea', label: 'QR Code Content', required: true },
                    size: { type: 'range', label: 'Size', min: 100, max: 1000, default: 300 },
                    format: {
                        type: 'select',
                        label: 'Format',
                        options: [
                            { value: 'png', label: 'PNG' },
                            { value: 'svg', label: 'SVG' }
                        ]
                    }
                }
            }
        };

        return configs[toolName] || {
            acceptedTypes: ['*'],
            maxFiles: 5,
            options: {}
        };
    }

    renderToolOptions(options, container) {
        const optionsHTML = Object.entries(options).map(([key, config]) => {
            switch (config.type) {
                case 'text':
                case 'email':
                case 'tel':
                case 'number':
                    return `
                        <div class="form-group">
                            <label class="form-label">${config.label}</label>
                            <input type="${config.type}" name="${key}" class="form-input" 
                                   value="${config.default || ''}" ${config.required ? 'required' : ''}>
                        </div>
                    `;
                case 'textarea':
                    return `
                        <div class="form-group">
                            <label class="form-label">${config.label}</label>
                            <textarea name="${key}" class="form-input" rows="3" 
                                      ${config.required ? 'required' : ''}>${config.default || ''}</textarea>
                        </div>
                    `;
                case 'select':
                    const options = config.options.map(opt => 
                        `<option value="${opt.value}">${opt.label}</option>`
                    ).join('');
                    return `
                        <div class="form-group">
                            <label class="form-label">${config.label}</label>
                            <select name="${key}" class="form-input">
                                ${options}
                            </select>
                        </div>
                    `;
                case 'checkbox':
                    return `
                        <div class="form-group">
                            <label class="form-label flex items-center">
                                <input type="checkbox" name="${key}" class="form-checkbox mr-2" 
                                       ${config.default ? 'checked' : ''}>
                                ${config.label}
                            </label>
                        </div>
                    `;
                case 'range':
                    return `
                        <div class="form-group">
                            <label class="form-label">${config.label}</label>
                            <input type="range" name="${key}" class="form-range" 
                                   min="${config.min}" max="${config.max}" value="${config.default}">
                            <span class="range-value">${config.default}</span>
                        </div>
                    `;
                default:
                    return '';
            }
        }).join('');

        container.innerHTML = `
            <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6">
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Tool Options</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    ${optionsHTML}
                </div>
            </div>
        `;
        container.classList.remove('hidden');

        // Add event listeners for range inputs
        container.querySelectorAll('input[type="range"]').forEach(range => {
            const valueSpan = range.nextElementSibling;
            range.addEventListener('input', (e) => {
                if (valueSpan) valueSpan.textContent = e.target.value;
            });
        });
    }

    handleFileSelection(files) {
        const fileList = document.getElementById('file-list');
        const processBtn = document.getElementById('process-btn');
        const toolOptions = document.getElementById('tool-options');
        
        if (!files || files.length === 0) return;

        // Clear previous files
        this.uploadedFiles = [];
        fileList.innerHTML = '';

        // Validate and process files
        Array.from(files).forEach((file, index) => {
            if (this.validateFile(file)) {
                this.uploadedFiles.push(file);
                this.renderFileItem(file, index, fileList);
            }
        });

        // Show options and enable process button if files are valid
        if (this.uploadedFiles.length > 0) {
            toolOptions.classList.remove('hidden');
            processBtn.disabled = false;
            processBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }

    validateFile(file) {
        const config = this.getToolConfig(this.currentTool);
        
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showError(`File "${file.name}" is too large. Maximum size is ${this.maxFileSize / (1024*1024)}MB`);
            return false;
        }

        // Check file type
        if (config.acceptedTypes && config.acceptedTypes.length > 0 && !config.acceptedTypes.includes('*')) {
            const fileExt = '.' + file.name.split('.').pop().toLowerCase();
            if (!config.acceptedTypes.includes(fileExt)) {
                this.showError(`File type "${fileExt}" is not supported for this tool`);
                return false;
            }
        }

        // Check file count
        if (config.maxFiles && this.uploadedFiles.length >= config.maxFiles) {
            this.showError(`Maximum ${config.maxFiles} files allowed for this tool`);
            return false;
        }

        return true;
    }

    renderFileItem(file, index, container) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-600 flex items-center justify-between';
        fileItem.innerHTML = `
            <div class="flex items-center">
                <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mr-3">
                    <i data-lucide="file" class="w-5 h-5 text-blue-600 dark:text-blue-400"></i>
                </div>
                <div>
                    <div class="font-medium text-gray-900 dark:text-white">${file.name}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">${this.formatFileSize(file.size)}</div>
                </div>
            </div>
            <button type="button" class="remove-file text-red-500 hover:text-red-700 p-1" data-index="${index}">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        `;
        
        container.appendChild(fileItem);
        
        // Add remove functionality
        fileItem.querySelector('.remove-file').addEventListener('click', (e) => {
            const index = parseInt(e.target.closest('.remove-file').dataset.index);
            this.removeFile(index);
        });
        
        // Refresh Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    removeFile(index) {
        this.uploadedFiles.splice(index, 1);
        this.refreshFileList();
        
        // Disable process button if no files
        if (this.uploadedFiles.length === 0) {
            const processBtn = document.getElementById('process-btn');
            processBtn.disabled = true;
            processBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    refreshFileList() {
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '';
        this.uploadedFiles.forEach((file, index) => {
            this.renderFileItem(file, index, fileList);
        });
    }

    async processFiles() {
        if (this.uploadedFiles.length === 0 && this.getToolConfig(this.currentTool).maxFiles > 0) {
            this.showError('Please select files to process');
            return;
        }

        this.showProcessingStatus();

        try {
            const formData = new FormData();
            
            // Add files
            this.uploadedFiles.forEach((file, index) => {
                formData.append('files', file);
            });

            // Add tool-specific options
            const toolForm = document.getElementById('tool-form');
            const formInputs = toolForm.querySelectorAll('input, select, textarea');
            formInputs.forEach(input => {
                if (input.name && input.name !== 'files') {
                    if (input.type === 'checkbox') {
                        formData.append(input.name, input.checked);
                    } else {
                        formData.append(input.name, input.value);
                    }
                }
            });

            // Add tool name
            formData.append('tool', this.currentTool);

            // Send to appropriate API endpoint
            const response = await this.callToolAPI(formData);
            
            if (response.success) {
                this.showResults(response);
            } else {
                this.showError(response.error || 'Processing failed');
            }
        } catch (error) {
            this.showError('An error occurred while processing files');
            console.error('Processing error:', error);
        }
    }

    async callToolAPI(formData) {
        const toolCategory = this.getToolCategory(this.currentTool);
        const endpoint = this.getAPIEndpoint(this.currentTool, toolCategory);
        
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    getToolCategory(toolName) {
        const categories = {
            'pdf': ['pdf-merge', 'pdf-split', 'pdf-compress', 'pdf-to-word', 'word-to-pdf'],
            'image': ['image-compress', 'image-resize', 'image-convert', 'image-crop'],
            'video': ['video-to-mp3', 'video-trimmer', 'video-compress'],
            'ai': ['resume-generator', 'business-name-generator', 'qr-generator']
        };

        for (const [category, tools] of Object.entries(categories)) {
            if (tools.includes(toolName)) {
                return category;
            }
        }
        return 'generic';
    }

    getAPIEndpoint(toolName, category) {
        const endpoints = {
            'pdf-merge': '/api/pdf/merge',
            'pdf-split': '/api/pdf/split',
            'pdf-compress': '/api/pdf/compress',
            'image-compress': '/api/image/compress',
            'image-resize': '/api/image/resize',
            'image-convert': '/api/image/convert',
            'video-to-mp3': '/api/video/extract-audio',
            'video-trimmer': '/api/video/trim',
            'resume-generator': '/api/ai/resume',
            'qr-generator': '/api/utility/qr-code'
        };

        return endpoints[toolName] || `/api/tools/${category}/${toolName}`;
    }

    showProcessingStatus() {
        document.getElementById('tool-form').classList.add('hidden');
        document.getElementById('processing-status').classList.remove('hidden');
        document.getElementById('results-section').classList.add('hidden');
        
        // Simulate progress
        this.simulateProgress();
    }

    simulateProgress() {
        const progressFill = document.getElementById('progress-fill');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 90) {
                progress = 90;
                clearInterval(interval);
            }
            progressFill.style.width = `${progress}%`;
        }, 200);
    }

    showResults(response) {
        document.getElementById('processing-status').classList.add('hidden');
        document.getElementById('results-section').classList.remove('hidden');
        
        const downloadLinks = document.getElementById('download-links');
        downloadLinks.innerHTML = '';

        if (response.files && response.files.length > 0) {
            response.files.forEach(file => {
                const downloadLink = document.createElement('a');
                downloadLink.href = file.download_url;
                downloadLink.className = 'inline-flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors mr-2 mb-2';
                downloadLink.innerHTML = `
                    <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                    Download ${file.filename}
                `;
                downloadLinks.appendChild(downloadLink);
            });
        } else if (response.download_url) {
            const downloadLink = document.createElement('a');
            downloadLink.href = response.download_url;
            downloadLink.className = 'inline-flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors';
            downloadLink.innerHTML = `
                <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                Download Result
            `;
            downloadLinks.appendChild(downloadLink);
        }

        // Refresh Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Complete progress bar
        document.getElementById('progress-fill').style.width = '100%';
    }

    showError(message) {
        // Hide processing status
        document.getElementById('processing-status').classList.add('hidden');
        document.getElementById('tool-form').classList.remove('hidden');
        
        // Show error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4 mb-4 animate__animated animate__shakeX';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 mr-3"></i>
                <span class="text-red-700 dark:text-red-300">${message}</span>
            </div>
        `;
        
        // Insert error at the top of the form
        const form = document.getElementById('tool-form');
        form.insertBefore(errorDiv, form.firstChild);
        
        // Remove error after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
        
        // Refresh Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedToolHandler();
});