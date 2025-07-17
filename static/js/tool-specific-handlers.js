/**
 * Tool-Specific Handlers for Suntyn AI
 * Enhanced functionality for individual tools
 */

// Global configurations
window.ToolSpecificHandlers = {
    currentTool: null,
    apiBase: '/enhanced_api',
    uploadProgress: 0,
    processing: false,
    results: null
};

// Initialize tool-specific functionality
function initializeToolSpecificHandlers() {
    const toolName = document.body.getAttribute('data-tool-name');
    if (!toolName) return;
    
    window.ToolSpecificHandlers.currentTool = toolName;
    
    // Setup drag and drop
    setupDragAndDrop();
    
    // Setup form handlers
    setupFormHandlers();
    
    // Setup progress tracking
    setupProgressTracking();
    
    // Tool-specific initialization
    initializeToolSpecific(toolName);
}

function setupDragAndDrop() {
    const dropZone = document.getElementById('dropZone');
    if (!dropZone) return;
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('border-blue-500', 'bg-blue-50');
    });
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('border-blue-500', 'bg-blue-50');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('border-blue-500', 'bg-blue-50');
        
        const files = e.dataTransfer.files;
        handleFileUpload(files);
    });
}

function setupFormHandlers() {
    const form = document.getElementById('toolForm');
    if (!form) return;
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        processToolData();
    });
    
    // File input change handler
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            handleFileUpload(e.target.files);
        });
    }
}

function setupProgressTracking() {
    const progressBar = document.getElementById('progressBar');
    if (!progressBar) return;
    
    // Progress update function
    window.updateProgress = (progress) => {
        window.ToolSpecificHandlers.uploadProgress = progress;
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
    };
}

function handleFileUpload(files) {
    if (!files || files.length === 0) return;
    
    const fileList = document.getElementById('fileList');
    const processBtn = document.getElementById('processBtn');
    
    if (fileList) {
        fileList.innerHTML = '';
        
        Array.from(files).forEach((file, index) => {
            const fileDiv = document.createElement('div');
            fileDiv.className = 'flex items-center justify-between bg-gray-50 p-3 rounded-lg';
            fileDiv.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i data-lucide="file" class="w-5 h-5 text-gray-500"></i>
                    <span class="text-sm font-medium text-gray-700">${file.name}</span>
                    <span class="text-xs text-gray-500">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
                </div>
                <button type="button" onclick="removeFile(${index})" class="text-red-500 hover:text-red-700">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            `;
            fileList.appendChild(fileDiv);
        });
        
        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    if (processBtn) {
        processBtn.disabled = false;
        processBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
    
    // Store files for processing
    window.ToolSpecificHandlers.uploadedFiles = files;
}

function processToolData() {
    if (window.ToolSpecificHandlers.processing) return;
    
    window.ToolSpecificHandlers.processing = true;
    const toolName = window.ToolSpecificHandlers.currentTool;
    
    // Show processing state
    showProcessingState();
    
    // Get tool-specific processor
    const processor = getToolProcessor(toolName);
    if (processor) {
        processor();
    } else {
        // Generic processing
        processGenericTool();
    }
}

function showProcessingState() {
    const processBtn = document.getElementById('processBtn');
    const progressContainer = document.getElementById('progressContainer');
    
    if (processBtn) {
        processBtn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin mr-2"></i> Processing...';
        processBtn.disabled = true;
    }
    
    if (progressContainer) {
        progressContainer.classList.remove('hidden');
    }
}

function hideProcessingState() {
    const processBtn = document.getElementById('processBtn');
    const progressContainer = document.getElementById('progressContainer');
    
    if (processBtn) {
        processBtn.innerHTML = '<i data-lucide="play" class="w-4 h-4 mr-2"></i> Process';
        processBtn.disabled = false;
    }
    
    if (progressContainer) {
        progressContainer.classList.add('hidden');
    }
    
    window.ToolSpecificHandlers.processing = false;
}

function getToolProcessor(toolName) {
    const processors = {
        'pdf-merge': processPdfMerge,
        'pdf-split': processPdfSplit,
        'pdf-compress': processPdfCompress,
        'image-compress': processImageCompress,
        'image-resize': processImageResize,
        'video-trimmer': processVideoTrimmer,
        'video-to-mp3': processVideoToMp3,
        'qr-generator': processQrGenerator,
        'password-generator': processPasswordGenerator,
        'resume-generator': processResumeGenerator,
        'business-name-generator': processBusinessNameGenerator
    };
    
    return processors[toolName];
}

// Tool-specific processors
function processPdfMerge() {
    const files = window.ToolSpecificHandlers.uploadedFiles;
    if (!files || files.length < 2) {
        showError('Please upload at least 2 PDF files');
        return;
    }
    
    const formData = new FormData();
    Array.from(files).forEach((file, index) => {
        formData.append(`file_${index}`, file);
    });
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/pdf-merge`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showDownloadLink(data.filename);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processPdfSplit() {
    const files = window.ToolSpecificHandlers.uploadedFiles;
    const pageRange = document.getElementById('pageRange')?.value || '1-3';
    
    if (!files || files.length === 0) {
        showError('Please upload a PDF file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file_0', files[0]);
    formData.append('page_range', pageRange);
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/pdf-split`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showDownloadLink(data.filename);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processPdfCompress() {
    const files = window.ToolSpecificHandlers.uploadedFiles;
    const compressionLevel = document.getElementById('compressionLevel')?.value || 'medium';
    
    if (!files || files.length === 0) {
        showError('Please upload a PDF file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file_0', files[0]);
    formData.append('compression_level', compressionLevel);
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/pdf-compress`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showDownloadLink(data.filename);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processImageCompress() {
    const files = window.ToolSpecificHandlers.uploadedFiles;
    const quality = document.getElementById('quality')?.value || 80;
    
    if (!files || files.length === 0) {
        showError('Please upload an image file');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', files[0]);
    formData.append('quality', quality);
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/image-compress`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showDownloadLink(data.filename);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processQrGenerator() {
    const text = document.getElementById('qrText')?.value;
    const size = document.getElementById('qrSize')?.value || 256;
    const color = document.getElementById('qrColor')?.value || '#000000';
    const bgColor = document.getElementById('qrBgColor')?.value || '#ffffff';
    
    if (!text) {
        showError('Please enter text or URL');
        return;
    }
    
    const data = {
        text: text,
        size: parseInt(size),
        color: color,
        bgColor: bgColor,
        format: 'PNG'
    };
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/qr-generator`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showDownloadLink(data.filename);
            showQrPreview(data.url);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processPasswordGenerator() {
    const length = document.getElementById('passwordLength')?.value || 12;
    const uppercase = document.getElementById('uppercase')?.checked || true;
    const lowercase = document.getElementById('lowercase')?.checked || true;
    const numbers = document.getElementById('numbers')?.checked || true;
    const symbols = document.getElementById('symbols')?.checked || true;
    
    const data = {
        length: parseInt(length),
        uppercase: uppercase,
        lowercase: lowercase,
        numbers: numbers,
        symbols: symbols
    };
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/password-generator`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            showGeneratedPassword(data.password);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

function processGenericTool() {
    const files = window.ToolSpecificHandlers.uploadedFiles;
    const toolName = window.ToolSpecificHandlers.currentTool;
    
    const formData = new FormData();
    if (files) {
        Array.from(files).forEach((file, index) => {
            formData.append(`file_${index}`, file);
        });
    }
    
    fetch(`${window.ToolSpecificHandlers.apiBase}/tools/generic/${toolName}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
        } else {
            showError(data.message);
        }
    })
    .catch(error => showError(`Error: ${error.message}`))
    .finally(() => hideProcessingState());
}

// UI Helper Functions
function showSuccess(message) {
    const alertContainer = document.getElementById('alertContainer');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="bg-green-50 border border-green-200 rounded-md p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i data-lucide="check-circle" class="w-5 h-5 text-green-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-green-800">${message}</p>
                    </div>
                </div>
            </div>
        `;
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

function showError(message) {
    const alertContainer = document.getElementById('alertContainer');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-md p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i data-lucide="alert-circle" class="w-5 h-5 text-red-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-red-800">${message}</p>
                    </div>
                </div>
            </div>
        `;
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

function showDownloadLink(filename) {
    const downloadContainer = document.getElementById('downloadContainer');
    if (downloadContainer) {
        downloadContainer.innerHTML = `
            <div class="bg-blue-50 border border-blue-200 rounded-md p-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <i data-lucide="download" class="w-5 h-5 text-blue-400 mr-2"></i>
                        <span class="text-sm font-medium text-blue-800">File ready for download</span>
                    </div>
                    <a href="${window.ToolSpecificHandlers.apiBase}/download/${filename}" 
                       class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                       download>
                        <i data-lucide="download" class="w-4 h-4 mr-1"></i>
                        Download
                    </a>
                </div>
            </div>
        `;
        downloadContainer.classList.remove('hidden');
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

function showQrPreview(url) {
    const previewContainer = document.getElementById('previewContainer');
    if (previewContainer) {
        previewContainer.innerHTML = `
            <div class="text-center">
                <img src="${url}" alt="QR Code" class="mx-auto mb-4 border border-gray-300 rounded-lg">
                <p class="text-sm text-gray-600">QR Code Preview</p>
            </div>
        `;
        previewContainer.classList.remove('hidden');
    }
}

function showGeneratedPassword(password) {
    const resultContainer = document.getElementById('resultContainer');
    if (resultContainer) {
        resultContainer.innerHTML = `
            <div class="bg-gray-50 border border-gray-200 rounded-md p-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <i data-lucide="key" class="w-5 h-5 text-gray-400 mr-2"></i>
                        <span class="text-lg font-mono font-medium text-gray-800" id="generatedPassword">${password}</span>
                    </div>
                    <button onclick="copyPassword()" class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                        <i data-lucide="copy" class="w-4 h-4 mr-1"></i>
                        Copy
                    </button>
                </div>
            </div>
        `;
        resultContainer.classList.remove('hidden');
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

function copyPassword() {
    const passwordElement = document.getElementById('generatedPassword');
    if (passwordElement) {
        navigator.clipboard.writeText(passwordElement.textContent);
        showSuccess('Password copied to clipboard!');
    }
}

function initializeToolSpecific(toolName) {
    // Tool-specific initialization based on tool name
    switch(toolName) {
        case 'qr-generator':
            initializeQrGenerator();
            break;
        case 'password-generator':
            initializePasswordGenerator();
            break;
        case 'pdf-compress':
            initializePdfCompress();
            break;
        case 'image-compress':
            initializeImageCompress();
            break;
        // Add more tool-specific initializations as needed
    }
}

function initializeQrGenerator() {
    const textInput = document.getElementById('qrText');
    if (textInput) {
        textInput.addEventListener('input', () => {
            const processBtn = document.getElementById('processBtn');
            if (processBtn) {
                processBtn.disabled = !textInput.value.trim();
            }
        });
    }
}

function initializePasswordGenerator() {
    const lengthSlider = document.getElementById('passwordLength');
    const lengthDisplay = document.getElementById('lengthDisplay');
    
    if (lengthSlider && lengthDisplay) {
        lengthSlider.addEventListener('input', () => {
            lengthDisplay.textContent = lengthSlider.value;
        });
    }
}

function initializePdfCompress() {
    const compressionSlider = document.getElementById('compressionLevel');
    const compressionDisplay = document.getElementById('compressionDisplay');
    
    if (compressionSlider && compressionDisplay) {
        compressionSlider.addEventListener('input', () => {
            const levels = ['Low', 'Medium', 'High'];
            compressionDisplay.textContent = levels[compressionSlider.value] || 'Medium';
        });
    }
}

function initializeImageCompress() {
    const qualitySlider = document.getElementById('quality');
    const qualityDisplay = document.getElementById('qualityDisplay');
    
    if (qualitySlider && qualityDisplay) {
        qualitySlider.addEventListener('input', () => {
            qualityDisplay.textContent = `${qualitySlider.value}%`;
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeToolSpecificHandlers);

// Export for global access
window.ToolSpecificHandlers.init = initializeToolSpecificHandlers;