// Simplified tool manager for immediate functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tool Manager Initialized');
    
    // Get current tool name from page
    const currentTool = window.location.pathname.split('/').pop();
    console.log('Current tool:', currentTool);
    
    // Enhanced file upload and processing
    setupToolProcessing(currentTool);
});

function setupToolProcessing(toolName) {
    const fileInput = document.getElementById('file-input');
    const fileSelectBtn = document.getElementById('file-select-btn');
    const processBtn = document.getElementById('process-btn');
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileList = document.getElementById('file-list');
    const toolForm = document.getElementById('tool-form');
    
    let selectedFiles = [];
    
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
}