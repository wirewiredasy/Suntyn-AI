/**
 * PDF Merge Tool - Unique Functionality
 * Advanced PDF merging with drag-and-drop reordering
 */

function pdfMerger() {
    return {
        files: [],
        isProcessing: false,
        showPreview: false,
        mergeProgress: 0,
        
        init() {
            this.setupDragAndDrop();
            this.setupFileInput();
            console.log('🔄 PDF Merge Tool Initialized');
        },
        
        setupDragAndDrop() {
            const dropZone = document.getElementById('pdf-drop-zone');
            if (!dropZone) return;
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.add('border-red-500', 'bg-red-50');
                });
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.remove('border-red-500', 'bg-red-50');
                });
            });
            
            dropZone.addEventListener('drop', (e) => {
                const files = Array.from(e.dataTransfer.files);
                this.addFiles(files);
            });
        },
        
        setupFileInput() {
            const fileInput = document.getElementById('pdf-file-input');
            if (!fileInput) return;
            
            fileInput.addEventListener('change', (e) => {
                const files = Array.from(e.target.files);
                this.addFiles(files);
            });
        },
        
        addFiles(files) {
            const pdfFiles = files.filter(file => file.type === 'application/pdf');
            
            if (pdfFiles.length === 0) {
                this.showAlert('Please select only PDF files', 'error');
                return;
            }
            
            pdfFiles.forEach(file => {
                if (file.size > 50 * 1024 * 1024) { // 50MB limit
                    this.showAlert(`File ${file.name} is too large (max 50MB)`, 'error');
                    return;
                }
                
                const fileObj = {
                    id: Date.now() + Math.random(),
                    file: file,
                    name: file.name,
                    size: this.formatFileSize(file.size),
                    preview: null
                };
                
                this.files.push(fileObj);
                this.generatePreview(fileObj);
            });
            
            this.$nextTick(() => {
                this.updateFileList();
            });
        },
        
        async generatePreview(fileObj) {
            try {
                // Create a simple preview for PDF files
                const reader = new FileReader();
                reader.onload = (e) => {
                    fileObj.preview = 'data:image/svg+xml;base64,' + btoa(`
                        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="120" viewBox="0 0 100 120">
                            <rect width="100" height="120" fill="#dc2626" rx="8"/>
                            <text x="50" y="60" text-anchor="middle" fill="white" font-size="12">PDF</text>
                            <text x="50" y="75" text-anchor="middle" fill="white" font-size="8">${fileObj.name.substr(0, 10)}...</text>
                        </svg>
                    `);
                };
                reader.readAsArrayBuffer(fileObj.file);
            } catch (error) {
                console.log('Preview generation failed, using default');
            }
        },
        
        removeFile(fileId) {
            this.files = this.files.filter(f => f.id !== fileId);
            this.updateFileList();
        },
        
        moveFile(fileId, direction) {
            const index = this.files.findIndex(f => f.id === fileId);
            if (index === -1) return;
            
            const newIndex = direction === 'up' ? index - 1 : index + 1;
            if (newIndex < 0 || newIndex >= this.files.length) return;
            
            // Swap files
            [this.files[index], this.files[newIndex]] = [this.files[newIndex], this.files[index]];
            this.updateFileList();
        },
        
        updateFileList() {
            const fileList = document.getElementById('file-list');
            if (!fileList) return;
            
            fileList.innerHTML = '';
            
            this.files.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg border';
                fileItem.innerHTML = `
                    <div class="flex items-center space-x-3">
                        <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                            <i data-lucide="file-text" class="w-6 h-6 text-red-600"></i>
                        </div>
                        <div>
                            <p class="font-medium text-gray-900">${file.name}</p>
                            <p class="text-sm text-gray-500">${file.size}</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="window.pdfMergerInstance.moveFile(${file.id}, 'up')" 
                                class="p-2 text-gray-400 hover:text-gray-600" ${index === 0 ? 'disabled' : ''}>
                            <i data-lucide="chevron-up" class="w-4 h-4"></i>
                        </button>
                        <button onclick="window.pdfMergerInstance.moveFile(${file.id}, 'down')" 
                                class="p-2 text-gray-400 hover:text-gray-600" ${index === this.files.length - 1 ? 'disabled' : ''}>
                            <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                        <button onclick="window.pdfMergerInstance.removeFile(${file.id})" 
                                class="p-2 text-red-400 hover:text-red-600">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                `;
                fileList.appendChild(fileItem);
            });
            
            // Re-initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        },
        
        async mergePDFs() {
            if (this.files.length < 2) {
                this.showAlert('Please select at least 2 PDF files to merge', 'error');
                return;
            }
            
            this.isProcessing = true;
            this.mergeProgress = 0;
            
            try {
                const formData = new FormData();
                this.files.forEach((fileObj, index) => {
                    formData.append('files', fileObj.file);
                    formData.append('order', index);
                });
                
                // Simulate progress
                const progressInterval = setInterval(() => {
                    if (this.mergeProgress < 90) {
                        this.mergeProgress += Math.random() * 10;
                    }
                }, 200);
                
                const response = await fetch('/api/tools/pdf-merge', {
                    method: 'POST',
                    body: formData
                });
                
                clearInterval(progressInterval);
                this.mergeProgress = 100;
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'merged-document.pdf';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                    
                    this.showAlert('PDF files merged successfully!', 'success');
                } else {
                    throw new Error('Merge failed');
                }
            } catch (error) {
                console.error('PDF merge error:', error);
                this.showAlert('Failed to merge PDF files. Please try again.', 'error');
            } finally {
                this.isProcessing = false;
                setTimeout(() => {
                    this.mergeProgress = 0;
                }, 2000);
            }
        },
        
        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        showAlert(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
                type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
            }`;
            alertDiv.textContent = message;
            document.body.appendChild(alertDiv);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
    };
}

// Global instance for button callbacks
window.pdfMergerInstance = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('[x-data="pdfMerger()"]')) {
        window.pdfMergerInstance = pdfMerger();
        console.log('🔄 PDF Merge Tool Ready');
    }
});