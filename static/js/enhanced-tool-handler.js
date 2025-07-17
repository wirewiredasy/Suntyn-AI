// Enhanced Tool Handler for Toolora AI
class EnhancedToolHandler {
    constructor() {
        this.processingQueue = [];
        this.isProcessing = false;
        this.supportedTools = new Set([
            'pdf-merge', 'pdf-split', 'pdf-compress', 'image-compress', 
            'image-resize', 'video-to-mp3', 'video-trimmer', 'resume-generator',
            'qr-generator', 'password-generator', 'text-case-converter'
        ]);
    }

    async processFile(toolName, files, options = {}) {
        if (!this.supportedTools.has(toolName)) {
            throw new Error(`Tool ${toolName} is not supported yet`);
        }

        this.showProcessingStatus(true);

        try {
            const formData = new FormData();

            // Add files
            if (files && files.length > 0) {
                files.forEach(file => {
                    formData.append('files', file);
                });
            }

            // Add options
            Object.entries(options).forEach(([key, value]) => {
                formData.append(key, value);
            });

            const endpoint = this.getEndpoint(toolName);
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showSuccess(result);
                return result;
            } else {
                throw new Error(result.error || 'Processing failed');
            }

        } catch (error) {
            this.showError(error.message);
            throw error;
        } finally {
            this.showProcessingStatus(false);
        }
    }

    getEndpoint(toolName) {
        const endpoints = {
            'pdf-merge': '/api/pdf/merge',
            'pdf-split': '/api/pdf/split',
            'pdf-compress': '/api/pdf/compress',
            'image-compress': '/api/image/compress',
            'image-resize': '/api/image/resize',
            'video-to-mp3': '/api/video/extract-audio',
            'video-trimmer': '/api/video/trim',
            'resume-generator': '/api/ai/generate-resume',
            'qr-generator': '/api/utility/generate-qr',
            'password-generator': '/api/utility/generate-password',
            'text-case-converter': '/api/utility/convert-text-case'
        };

        return endpoints[toolName] || `/api/tools/generic/${toolName}`;
    }

    showProcessingStatus(isProcessing) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            if (statusElement && statusElement.style) {
                statusElement.style.display = isProcessing ? 'block' : 'none';
            }
        }

        const processBtn = document.getElementById('process-btn');
        if (processBtn) {
            processBtn.disabled = isProcessing;
            processBtn.textContent = isProcessing ? 'Processing...' : 'Process Files';
        }
    }

    showSuccess(result) {
        const notification = this.createNotification('Success! File processed.', 'success');
        document.body.appendChild(notification);

        if (result.download_url) {
            const downloadBtn = document.createElement('a');
            downloadBtn.href = result.download_url;
            downloadBtn.download = result.filename || 'processed_file';
            downloadBtn.className = 'bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 ml-2';
            downloadBtn.textContent = 'Download';
            notification.appendChild(downloadBtn);
        }

        setTimeout(() => notification.remove(), 5000);
    }

    showError(message) {
        const notification = this.createNotification(message, 'error');
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`;
        notification.textContent = message;
        return notification;
    }
}

// Initialize enhanced tool handler
const enhancedToolHandler = new EnhancedToolHandler();

// Export for global use
window.enhancedToolHandler = enhancedToolHandler;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.enhancedToolHandler = new EnhancedToolHandler();
});