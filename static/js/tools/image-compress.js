/**
 * Image Compression Tool - Unique Functionality
 * Advanced image compression with quality preview
 */

function imageCompressor() {
    return {
        selectedFile: null,
        compressedFile: null,
        originalSize: 0,
        compressedSize: 0,
        quality: 0.8,
        isProcessing: false,
        showPreview: false,
        originalPreview: '',
        compressedPreview: '',
        
        init() {
            this.setupFileInput();
            this.setupDragAndDrop();
            console.log('🖼️ Image Compressor Tool Initialized');
        },
        
        setupFileInput() {
            const fileInput = document.getElementById('image-file-input');
            if (!fileInput) return;
            
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) this.loadImage(file);
            });
        },
        
        setupDragAndDrop() {
            const dropZone = document.getElementById('image-drop-zone');
            if (!dropZone) return;
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.add('border-green-500', 'bg-green-50');
                });
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.remove('border-green-500', 'bg-green-50');
                });
            });
            
            dropZone.addEventListener('drop', (e) => {
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    this.loadImage(file);
                } else {
                    this.showAlert('Please select a valid image file', 'error');
                }
            });
        },
        
        loadImage(file) {
            if (!file.type.startsWith('image/')) {
                this.showAlert('Please select a valid image file', 'error');
                return;
            }
            
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                this.showAlert('Image size too large (max 10MB)', 'error');
                return;
            }
            
            this.selectedFile = file;
            this.originalSize = file.size;
            this.showPreview = true;
            
            // Create preview
            const reader = new FileReader();
            reader.onload = (e) => {
                this.originalPreview = e.target.result;
                this.compressImage();
            };
            reader.readAsDataURL(file);
        },
        
        async compressImage() {
            if (!this.selectedFile) return;
            
            this.isProcessing = true;
            
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                
                img.onload = () => {
                    // Calculate new dimensions to maintain aspect ratio
                    let { width, height } = img;
                    const maxDimension = 1920; // Max width or height
                    
                    if (width > maxDimension || height > maxDimension) {
                        if (width > height) {
                            height = (height * maxDimension) / width;
                            width = maxDimension;
                        } else {
                            width = (width * maxDimension) / height;
                            height = maxDimension;
                        }
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // Draw and compress
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    // Convert to blob with quality setting
                    canvas.toBlob((blob) => {
                        this.compressedFile = blob;
                        this.compressedSize = blob.size;
                        this.compressedPreview = canvas.toDataURL('image/jpeg', this.quality);
                        this.isProcessing = false;
                        this.updateCompressionStats();
                    }, 'image/jpeg', this.quality);
                };
                
                img.onerror = () => {
                    this.showAlert('Failed to process image', 'error');
                    this.isProcessing = false;
                };
                
                img.src = this.originalPreview;
                
            } catch (error) {
                console.error('Compression error:', error);
                this.showAlert('Failed to compress image', 'error');
                this.isProcessing = false;
            }
        },
        
        updateQuality(value) {
            this.quality = parseFloat(value);
            if (this.selectedFile) {
                this.compressImage();
            }
        },
        
        updateCompressionStats() {
            const statsElement = document.getElementById('compression-stats');
            if (!statsElement) return;
            
            const originalSizeMB = (this.originalSize / (1024 * 1024)).toFixed(2);
            const compressedSizeMB = (this.compressedSize / (1024 * 1024)).toFixed(2);
            const compressionRatio = ((1 - this.compressedSize / this.originalSize) * 100).toFixed(1);
            
            statsElement.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <p class="text-sm text-blue-600 font-medium">Original Size</p>
                        <p class="text-lg font-bold text-blue-800">${originalSizeMB} MB</p>
                    </div>
                    <div class="bg-green-50 p-4 rounded-lg">
                        <p class="text-sm text-green-600 font-medium">Compressed Size</p>
                        <p class="text-lg font-bold text-green-800">${compressedSizeMB} MB</p>
                    </div>
                    <div class="bg-purple-50 p-4 rounded-lg">
                        <p class="text-sm text-purple-600 font-medium">Size Reduction</p>
                        <p class="text-lg font-bold text-purple-800">${compressionRatio}%</p>
                    </div>
                </div>
            `;
        },
        
        downloadCompressed() {
            if (!this.compressedFile) {
                this.showAlert('No compressed image available', 'error');
                return;
            }
            
            const url = window.URL.createObjectURL(this.compressedFile);
            const a = document.createElement('a');
            a.href = url;
            a.download = `compressed-${this.selectedFile.name.replace(/\.[^/.]+$/, '')}.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.showAlert('Compressed image downloaded successfully!', 'success');
        },
        
        resetTool() {
            this.selectedFile = null;
            this.compressedFile = null;
            this.originalSize = 0;
            this.compressedSize = 0;
            this.quality = 0.8;
            this.showPreview = false;
            this.originalPreview = '';
            this.compressedPreview = '';
            
            const fileInput = document.getElementById('image-file-input');
            if (fileInput) fileInput.value = '';
            
            const statsElement = document.getElementById('compression-stats');
            if (statsElement) statsElement.innerHTML = '';
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
window.imageCompressorInstance = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('[x-data="imageCompressor()"]')) {
        window.imageCompressorInstance = imageCompressor();
        console.log('🖼️ Image Compressor Tool Ready');
    }
});