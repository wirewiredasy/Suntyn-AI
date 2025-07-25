// Tool Manager - Initialize immediately
(function() {
    // Initialize global functions first
    window.getToolConfig = function(toolName) {
        const configs = {
            'pdf-merge': {
                acceptedTypes: '.pdf',
                maxFiles: 50,
                minFiles: 2,
                supportedFormats: ['application/pdf'],
                processingMessage: 'Merging PDFs...',
                successMessage: 'PDFs merged successfully!'
            },
            'image-compress': {
                acceptedTypes: 'image/*',
                maxFiles: 20,
                minFiles: 1,
                supportedFormats: ['image/jpeg', 'image/png', 'image/webp'],
                processingMessage: 'Compressing images...',
                successMessage: 'Images compressed successfully!'
            },
            'video-to-mp3': {
                acceptedTypes: 'video/*',
                maxFiles: 5,
                minFiles: 1,
                supportedFormats: ['video/mp4', 'video/avi', 'video/mov'],
                processingMessage: 'Extracting audio...',
                successMessage: 'Audio extracted successfully!'
            }
        };

        return configs[toolName] || {
            acceptedTypes: '*',
            maxFiles: 10,
            minFiles: 1,
            supportedFormats: [],
            processingMessage: 'Processing...',
            successMessage: 'Process completed successfully!'
        };
    };

    // Global tool handler function
    window.genericToolHandler = function(toolName) {
        console.log(`Processing tool: ${toolName}`);
        
        // Show processing notification
        showToolNotification(`Processing ${toolName}...`, 'info');
        
        // Simulate processing
        setTimeout(() => {
            showToolNotification(`${toolName} processed successfully!`, 'success');
        }, 2000);
    };

    function showToolNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 translate-x-full`;

        const bgColor = type === 'error' ? 'bg-red-500' : 
                       type === 'success' ? 'bg-green-500' : 
                       'bg-blue-500';

        notification.classList.add(bgColor, 'text-white');
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">×</button>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }

    // Initialize Alpine.js data if Alpine is available
    document.addEventListener('alpine:init', () => {
        Alpine.data('toolHandler', () => ({
            files: [],
            processing: false,
            progress: 0,
            results: [],
            dragover: false,

            addFiles(fileList) {
                this.files = Array.from(fileList);
            },

            removeFile(index) {
                this.files.splice(index, 1);
            },

            async processFiles() {
                if (this.files.length === 0) return;

                this.processing = true;
                this.progress = 0;
                this.results = [];

                try {
                    for (let i = 0; i <= 100; i += 10) {
                        this.progress = i;
                        await new Promise(resolve => setTimeout(resolve, 100));
                    }

                    this.results = this.files.map((file, index) => ({
                        id: index,
                        name: `processed_${file.name}`,
                        downloadUrl: '#',
                        size: '1.2 MB'
                    }));
                } catch (error) {
                    console.error('Processing error:', error);
                } finally {
                    this.processing = false;
                }
            }
        }));
    });

    // Fallback for when Alpine is not available
    if (!window.Alpine) {
        // Create a simple fallback object
        window.toolHandlerData = {
            files: [],
            processing: false,
            progress: 0,
            results: [],
            dragover: false
        };
    }

    console.log('Tool Manager Initialized');

    // Get current tool name from page
    const currentTool = window.location.pathname.split('/').pop();
    console.log('Current tool:', currentTool);

// Tool-specific configurations
function getToolConfig(toolName) {
    const configs = {
        'pdf-merge': {
            acceptedTypes: '.pdf',
            maxFiles: 50,
            minFiles: 2,
            supportedFormats: ['application/pdf'],
            processingMessage: 'Merging PDFs...',
            successMessage: 'PDFs merged successfully!'
        },
        'image-compress': {
            acceptedTypes: 'image/*',
            maxFiles: 20,
            minFiles: 1,
            supportedFormats: ['image/jpeg', 'image/png', 'image/webp'],
            processingMessage: 'Compressing images...',
            successMessage: 'Images compressed successfully!'
        },
        'video-to-mp3': {
            acceptedTypes: 'video/*',
            maxFiles: 5,
            minFiles: 1,
            supportedFormats: ['video/mp4', 'video/avi', 'video/mov'],
            processingMessage: 'Extracting audio...',
            successMessage: 'Audio extracted successfully!'
        },
        'resume-generator': {
            acceptedTypes: '',
            maxFiles: 0,
            minFiles: 0,
            supportedFormats: [],
            processingMessage: 'Generating resume...',
            successMessage: 'Resume generated successfully!'
        }
    };

    return configs[toolName] || {
        acceptedTypes: '*',
        maxFiles: 10,
        minFiles: 1,
        supportedFormats: [],
        processingMessage: 'Processing...',
        successMessage: 'Process completed successfully!'
    };
}

function applyToolConfig(config, fileInput, fileUploadArea) {
    if (fileInput && config.acceptedTypes) {
        fileInput.setAttribute('accept', config.acceptedTypes);
    }

    if (fileUploadArea) {
        const existingText = fileUploadArea.querySelector('p');
        if (existingText && config.supportedFormats.length > 0) {
            const formatText = config.supportedFormats.map(f => f.split('/')[1].toUpperCase()).join(', ');
            existingText.textContent = `Drag and drop your files here, or click to browse (${formatText} supported)`;
        }
    }
}



    // Enhanced file upload and processing
    if (currentTool && currentTool !== '' && currentTool !== 'tools') {
        setupToolProcessing(currentTool);
    }

    // Setup generic tool handlers
    setupGenericToolHandlers();
});

function setupGenericToolHandlers() {
    // Handle demo mode for tools
    const demoButtons = document.querySelectorAll('.demo-btn');
    demoButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const toolName = this.dataset.tool;
            showDemoResult(toolName);
        });
    });
}

function showDemoResult(toolName) {
    const demoResults = {
        'pdf-merge': 'PDF files merged successfully!',
        'image-compress': 'Image compressed by 60%!',
        'video-to-mp3': 'Audio extracted successfully!',
        'resume-generator': 'Professional resume generated!',
        'qr-generator': 'QR code generated successfully!'
    };

    const message = demoResults[toolName] || 'Tool processed successfully!';

    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Tool endpoint helper
function getToolEndpoint(toolName) {
    const endpoints = {
        'pdf-merge': '/api/pdf/merge',
        'pdf-split': '/api/pdf/split',
        'pdf-compress': '/api/pdf/compress',
        'image-compress': '/api/image/compress',
        'image-resize': '/api/image/resize',
        'video-to-mp3': '/api/video/extract-audio',
        'video-trimmer': '/api/video/trim',
        'resume-generator': '/api/ai/generate-resume',
        'qr-generator': '/api/utility/generate-qr'
    };

    return endpoints[toolName] || `/api/tools/generic/${toolName}`;
}

function setupToolProcessing(toolName) {
    // Tool-specific initialization
    const toolConfig = getToolConfig(toolName);

    const fileInput = document.getElementById('file-input');
    const fileSelectBtn = document.getElementById('file-select-btn');
    const processBtn = document.getElementById('process-btn');
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileList = document.getElementById('file-list');
    const toolForm = document.getElementById('tool-form');

    // Apply tool-specific configurations
    if (toolConfig) {
        applyToolConfig(toolConfig, fileInput, fileUploadArea);
    }

    let selectedFiles = [];

    // Helper functions
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        fileUploadArea.classList.add('drag-over');
    }

    function unhighlight(e) {
        fileUploadArea.classList.remove('drag-over');
    }

    function handleDrop(e) {
        preventDefaults(e);
        unhighlight(e);
        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    }

    function handleFiles(files) {
        selectedFiles = files;
        displayFiles(files);
        if (processBtn) {
            processBtn.disabled = false;
        }
    }

    function displayFiles(files) {
        if (fileList) {
            fileList.innerHTML = '';
            files.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item p-2 bg-gray-100 rounded mb-2';
                fileItem.innerHTML = `
                    <span class="file-name">${file.name}</span>
                    <span class="file-size text-sm text-gray-500">(${formatFileSize(file.size)})</span>
                `;
                fileList.appendChild(fileItem);
            });
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async function processFiles() {
        if (selectedFiles.length === 0) {
            alert('Please select files first');
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        // Add tool options if any
        const optionsForm = document.getElementById('tool-options');
        if (optionsForm) {
            const formData2 = new FormData(optionsForm);
            for (let [key, value] of formData2.entries()) {
                formData.append(key, value);
            }
        }

        try {
            const endpoint = getToolEndpoint(toolName);
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                showResults(result);
            } else {
                showError(result.error || 'Processing failed');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        }
    }

    function showResults(result) {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.style.display = 'block';
            if (result.download_url) {
                const downloadLink = document.createElement('a');
                downloadLink.href = result.download_url;
                downloadLink.download = result.filename || 'processed_file';
                downloadLink.className = 'bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600';
                downloadLink.textContent = 'Download Result';

                const downloadSection = document.getElementById('download-links');
                if (downloadSection) {
                    downloadSection.innerHTML = '';
                    downloadSection.appendChild(downloadLink);
                }
            }
        }
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
        errorDiv.textContent = message;

        const container = document.querySelector('.container') || document.body;
        container.insertBefore(errorDiv, container.firstChild);

        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    // File selection handling
    if (fileSelectBtn) {
        fileSelectBtn.addEventListener('click', () => {
            fileInput?.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            handleFiles(Array.from(e.target.files));
        });
    }

    // Drag and drop
    if (fileUploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileUploadArea.addEventListener(eventName, preventDefaults);
        });

        fileUploadArea.addEventListener('dragover', highlight);
        fileUploadArea.addEventListener('dragleave', unhighlight);
        fileUploadArea.addEventListener('drop', handleDrop);
    }

    // Process button
    if (processBtn) {
        processBtn.addEventListener('click', (e) => {
            e.preventDefault();
            processFiles();
        });
    }

    // Form submission
    if (toolForm) {
        toolForm.addEventListener('submit', (e) => {
            e.preventDefault();
            processFiles();
        });
    }
}

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        fileUploadArea?.classList.add('dragover');
    }

    function unhighlight() {
        fileUploadArea?.classList.remove('dragover');
    }

    function handleDrop(e) {
        unhighlight();
        const dt = e.dataTransfer;
        const files = Array.from(dt.files);
        handleFiles(files);
    }

    function handleFiles(files) {
        selectedFiles = files;
        displayFiles();

        if (selectedFiles.length > 0) {
            if (processBtn) {
                processBtn.disabled = false;
                processBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            }

            const toolOptions = document.getElementById('tool-options');
            if (toolOptions) {
                toolOptions.classList.remove('hidden');
            }
        }
    }

    function displayFiles() {
        if (!fileList) return;

        fileList.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg mb-2';
            fileItem.innerHTML = `
                <div class="flex items-center">
                    <i data-lucide="file" class="w-5 h-5 text-gray-400 mr-3"></i>
                    <div>
                        <span class="text-sm font-medium text-gray-900 dark:text-white">${file.name}</span>
                        <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">(${formatFileSize(file.size)})</span>
                    </div>
                </div>
                <button type="button" onclick="removeFile(${index})" class="text-red-500 hover:text-red-700">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            `;
            fileList.appendChild(fileItem);
        });

        // Re-initialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    window.removeFile = function(index) {
        selectedFiles.splice(index, 1);
        displayFiles();

        if (selectedFiles.length === 0 && processBtn) {
            processBtn.disabled = true;
            processBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    };

    async function processFiles() {
        console.log('Processing files for tool:', toolName);

        showProcessingStatus();

        try {
            const formData = new FormData();

            // Add files to form data
            if (selectedFiles.length > 0) {
                if (selectedFiles.length === 1) {
                    formData.append('file', selectedFiles[0]);
                } else {
                    selectedFiles.forEach(file => {
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

            // Get API endpoint
            const endpoint = getAPIEndpoint(toolName);
            console.log('Calling endpoint:', endpoint);

            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            console.log('API result:', result);

            hideProcessingStatus();

            if (result.success) {
                showResults(result);
            } else {
                showError(result.error || 'Processing failed');
            }

        } catch (error) {
            console.error('Processing error:', error);
            hideProcessingStatus();
            showError(error.message || 'An error occurred during processing');
        }
    }

    function getAPIEndpoint(toolName) {
        // Use tool-endpoints.js mapping if available
        if (typeof getToolEndpoint === 'function') {
            return getToolEndpoint(toolName);
        }

        // Direct mapping for common tools
        const endpoints = {
            'pdf-merge': '/api/pdf/merge',
            'pdf-split': '/api/pdf/split',
            'pdf-compress': '/api/pdf/compress',
            'image-compress': '/api/image/compress',
            'image-resize': '/api/image/resize',
            'image-convert': '/api/image/convert',
            'video-to-mp3': '/api/video/extract-audio',
            'video-trimmer': '/api/video/trim',
            'resume-generator': '/api/ai/generate-resume',
            'business-name-generator': '/api/ai/generate-business-names'
        };

        return endpoints[toolName] || `/api/tools/generic/${toolName}`;
    }

    function showProcessingStatus() {
        const statusDiv = document.getElementById('processing-status') || createStatusDiv();
        statusDiv.innerHTML = `
            <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
                <div class="flex items-center">
                    <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
                    <span class="text-blue-800 dark:text-blue-200">Processing your files...</span>
                </div>
            </div>
        `;
        statusDiv.classList.remove('hidden');
    }

    function hideProcessingStatus() {
        const statusDiv = document.getElementById('processing-status');
        if (statusDiv) {
            statusDiv.classList.add('hidden');
        }
    }

    function showResults(result) {
        const resultsDiv = document.getElementById('results-section') || createResultsDiv();
        let resultsHTML = '';

        if (result.download_url) {
            resultsHTML = `
                <div class="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-2">Processing Complete!</h3>
                    <a href="${result.download_url}" download="${result.filename}" 
                       class="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg">
                        <i data-lucide="download" class="w-4 h-4 mr-2"></i>
                        Download ${result.filename}
                    </a>
                </div>
            `;
        } else if (result.files) {
            const fileLinks = result.files.map(file => `
                <a href="${file.download_url}" download="${file.filename}" 
                   class="inline-flex items-center px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg mr-2 mb-2">
                    <i data-lucide="download" class="w-4 h-4 mr-2"></i>
                    ${file.filename}
                </a>
            `).join('');

            resultsHTML = `
                <div class="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-3">Processing Complete!</h3>
                    <div class="flex flex-wrap">
                        ${fileLinks}
                    </div>
                </div>
            `;
        } else if (result.business_names) {
            const namesList = result.business_names.map(name => `
                <div class="bg-white dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-600">
                    ${name}
                </div>
            `).join('');

            resultsHTML = `
                <div class="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-3">Generated Business Names</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                        ${namesList}
                    </div>
                </div>
            `;
        } else {
            resultsHTML = `
                <div class="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-2">Success!</h3>
                    <p class="text-green-700 dark:text-green-300">${result.message || 'Tool processed successfully'}</p>
                </div>
            `;
        }

        resultsDiv.innerHTML = resultsHTML;
        resultsDiv.classList.remove('hidden');

        // Re-initialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    function showError(message) {
        const resultsDiv = document.getElementById('results-section') || createResultsDiv();
        resultsDiv.innerHTML = `
            <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
                <div class="flex items-center">
                    <i data-lucide="alert-circle" class="w-5 h-5 text-red-600 dark:text-red-400 mr-3"></i>
                    <div>
                        <h3 class="text-lg font-semibold text-red-800 dark:text-red-200">Error</h3>
                        <p class="text-red-700 dark:text-red-300">${message}</p>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.classList.remove('hidden');

        // Re-initialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    function createStatusDiv() {
        const div = document.createElement('div');
        div.id = 'processing-status';
        div.className = 'hidden mb-4';

        const form = document.getElementById('tool-form');
        if (form) {
            form.parentNode.insertBefore(div, form.nextSibling);
        }

        return div;
    }

    function createResultsDiv() {
        const div = document.createElement('div');
        div.id = 'results-section';
        div.className = 'hidden mt-6';

        const container = document.querySelector('.container') || document.body;
        container.appendChild(div);

        return div;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

// Tool Manager - Initialize tool functionality
class ToolManager {
    constructor() {
        this.initializeTools();
        this.setupGlobalFunctions();
    }

    initializeTools() {
        console.log('Tool Manager Initialized');

        // Get current tool from URL
        const currentTool = this.getCurrentTool();
        console.log('Current tool:', currentTool);

        if (currentTool) {
            this.setupToolHandler(currentTool);
        }
    }

    setupGlobalFunctions() {
        // Define missing Alpine.js data
        window.Alpine = window.Alpine || {};

        // Global tool handler function
        window.genericToolHandler = (toolName) => {
            console.log(`Processing tool: ${toolName}`);
            this.processGenericTool(toolName);
        };

        // Get tool config function
        window.getToolConfig = (toolName) => {
            return {
                name: toolName,
                category: 'utility',
                description: `${toolName} tool`,
                maxFiles: 5,
                allowedTypes: ['*']
            };
        };

        // Setup Alpine.js global data
        if (typeof Alpine !== 'undefined') {
            Alpine.data('toolHandler', () => ({
                files: [],
                processing: false,
                progress: 0,
                results: [],
                dragover: false,

                addFiles(fileList) {
                    this.files = Array.from(fileList);
                },

                removeFile(index) {
                    this.files.splice(index, 1);
                },

                async processFiles() {
                    if (this.files.length === 0) return;

                    this.processing = true;
                    this.progress = 0;
                    this.results = [];

                    try {
                        // Simulate processing
                        for (let i = 0; i <= 100; i += 10) {
                            this.progress = i;
                            await new Promise(resolve => setTimeout(resolve, 100));
                        }

                        // Add demo results
                        this.results = this.files.map((file, index) => ({
                            id: index,
                            name: `processed_${file.name}`,
                            downloadUrl: '#',
                            size: '1.2 MB'
                        }));
                    } catch (error) {
                        console.error('Processing error:', error);
                    } finally {
                        this.processing = false;
                    }
                }
            }));
        }
    }
getCurrentTool() {
        const path = window.location.pathname;
        const toolMatch = path.match(/\/tools\/([^\/]+)/);
        return toolMatch ? toolMatch[1] : '';
    }

    async processGenericTool(toolName) {
        try {
            console.log(`Processing ${toolName} in demo mode`);

            // Show processing state
            const processingElements = document.querySelectorAll('[x-show="processing"]');
            processingElements.forEach(el => el.style.display = 'block');

            // Simulate processing
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Hide processing state
            processingElements.forEach(el => el.style.display = 'none');

            // Show success message
            this.showNotification(`${toolName} processed successfully!`, 'success');

        } catch (error) {
            console.error('Tool processing error:', error);
            this.showNotification('Processing failed. Please try again.', 'error');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 translate-x-full`;

        const bgColor = type === 'error' ? 'bg-red-500' : 
                       type === 'success' ? 'bg-green-500' : 
                       'bg-blue-500';

        notification.classList.add(bgColor, 'text-white');
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">×</button>
            </div>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
}