/**
 * Tool-Specific JavaScript Handlers
 * Unique behaviors for each of the 85 tools
 */

// Advanced PDF Merge Handler with drag-and-drop reordering
function pdfMerger() {
    return {
        files: [],
        dragover: false,
        processing: false,
        progress: 0,
        
        handleDrop(event) {
            this.dragover = false;
            const files = Array.from(event.dataTransfer.files).filter(f => f.type === 'application/pdf');
            this.addFiles(files);
        },
        
        handleFiles(files) {
            const pdfFiles = Array.from(files).filter(f => f.type === 'application/pdf');
            this.addFiles(pdfFiles);
        },
        
        addFiles(files) {
            files.forEach(file => {
                this.files.push({
                    file,
                    name: file.name,
                    size: file.size,
                    id: Date.now() + Math.random()
                });
            });
        },
        
        removeFile(index) {
            this.files.splice(index, 1);
        },
        
        moveFile(from, to) {
            const item = this.files.splice(from, 1)[0];
            this.files.splice(to, 0, item);
        },
        
        formatFileSize(bytes) {
            return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
        },
        
        async processMerge() {
            if (this.files.length < 2) {
                alert('Please select at least 2 PDF files to merge');
                return;
            }
            
            this.processing = true;
            this.progress = 0;
            
            // Simulate progress
            const progressInterval = setInterval(() => {
                this.progress += 10;
                if (this.progress >= 90) clearInterval(progressInterval);
            }, 200);
            
            try {
                const formData = new FormData();
                this.files.forEach((fileObj, index) => {
                    formData.append(`file_${index}`, fileObj.file);
                });
                
                const response = await fetch('/api/tools/pdf-merge', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                clearInterval(progressInterval);
                this.progress = 100;
                
                if (result.success) {
                    this.downloadFile(result.filename);
                    this.showSuccess('PDFs merged successfully!');
                } else {
                    this.showError(result.message || 'Error processing PDFs');
                }
            } catch (error) {
                clearInterval(progressInterval);
                this.showError('Network error occurred');
            }
            
            this.processing = false;
        },
        
        downloadFile(filename) {
            const a = document.createElement('a');
            a.href = `/api/download/${filename}`;
            a.download = filename;
            a.click();
        },
        
        showSuccess(message) {
            // Create success notification
            const notification = document.createElement('div');
            notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        },
        
        showError(message) {
            // Create error notification
            const notification = document.createElement('div');
            notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Advanced Image Compress Handler with quality preview
function imageCompressor() {
    return {
        files: [],
        quality: 80,
        processing: false,
        previewUrl: null,
        originalSize: 0,
        compressedSize: 0,
        
        handleFiles(files) {
            this.files = Array.from(files).filter(f => f.type.startsWith('image/'));
            if (this.files.length > 0) {
                this.previewImage(this.files[0]);
            }
        },
        
        previewImage(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.previewUrl = e.target.result;
                this.originalSize = file.size;
            };
            reader.readAsDataURL(file);
        },
        
        async compressImage() {
            if (!this.files.length) return;
            
            this.processing = true;
            
            const formData = new FormData();
            formData.append('image', this.files[0]);
            formData.append('quality', this.quality);
            
            try {
                const response = await fetch('/api/tools/image-compress', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    this.compressedSize = result.size;
                    this.downloadFile(result.filename);
                    this.showSuccess(`Image compressed! Size reduced by ${this.getSizeReduction()}%`);
                } else {
                    this.showError(result.message || 'Compression failed');
                }
            } catch (error) {
                this.showError('Network error occurred');
            }
            
            this.processing = false;
        },
        
        getSizeReduction() {
            if (!this.originalSize || !this.compressedSize) return 0;
            return Math.round((1 - this.compressedSize / this.originalSize) * 100);
        },
        
        downloadFile(filename) {
            const a = document.createElement('a');
            a.href = `/api/download/${filename}`;
            a.download = filename;
            a.click();
        },
        
        showSuccess(message) {
            this.showNotification(message, 'success');
        },
        
        showError(message) {
            this.showNotification(message, 'error');
        },
        
        showNotification(message, type) {
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Advanced QR Code Generator with customization
function qrGenerator() {
    return {
        text: '',
        size: 256,
        color: '#000000',
        bgColor: '#ffffff',
        format: 'PNG',
        qrCodeUrl: null,
        
        async generateQR() {
            if (!this.text.trim()) {
                this.showError('Please enter text or URL');
                return;
            }
            
            try {
                const response = await fetch('/api/tools/qr-generator', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: this.text,
                        size: this.size,
                        color: this.color,
                        bgColor: this.bgColor,
                        format: this.format
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    this.qrCodeUrl = result.url;
                    this.showSuccess('QR Code generated successfully!');
                } else {
                    this.showError(result.message || 'Generation failed');
                }
            } catch (error) {
                this.showError('Network error occurred');
            }
        },
        
        downloadQR() {
            if (!this.qrCodeUrl) return;
            
            const a = document.createElement('a');
            a.href = this.qrCodeUrl;
            a.download = `qr-code.${this.format.toLowerCase()}`;
            a.click();
        },
        
        showSuccess(message) {
            this.showNotification(message, 'success');
        },
        
        showError(message) {
            this.showNotification(message, 'error');
        },
        
        showNotification(message, type) {
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Advanced Video Trimmer with timeline preview
function videoTrimmer() {
    return {
        file: null,
        videoUrl: null,
        duration: 0,
        startTime: 0,
        endTime: 0,
        processing: false,
        progress: 0,
        
        handleFile(files) {
            if (files.length === 0) return;
            
            this.file = files[0];
            this.videoUrl = URL.createObjectURL(this.file);
            
            // Wait for video to load to get duration
            const video = document.createElement('video');
            video.src = this.videoUrl;
            video.onloadedmetadata = () => {
                this.duration = video.duration;
                this.endTime = this.duration;
            };
        },
        
        formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        },
        
        async trimVideo() {
            if (!this.file) {
                this.showError('Please select a video file');
                return;
            }
            
            if (this.startTime >= this.endTime) {
                this.showError('End time must be greater than start time');
                return;
            }
            
            this.processing = true;
            this.progress = 0;
            
            const formData = new FormData();
            formData.append('video', this.file);
            formData.append('startTime', this.startTime);
            formData.append('endTime', this.endTime);
            
            // Simulate progress
            const progressInterval = setInterval(() => {
                this.progress += 5;
                if (this.progress >= 90) clearInterval(progressInterval);
            }, 500);
            
            try {
                const response = await fetch('/api/tools/video-trimmer', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                clearInterval(progressInterval);
                this.progress = 100;
                
                if (result.success) {
                    this.downloadFile(result.filename);
                    this.showSuccess('Video trimmed successfully!');
                } else {
                    this.showError(result.message || 'Trimming failed');
                }
            } catch (error) {
                clearInterval(progressInterval);
                this.showError('Network error occurred');
            }
            
            this.processing = false;
        },
        
        downloadFile(filename) {
            const a = document.createElement('a');
            a.href = `/api/download/${filename}`;
            a.download = filename;
            a.click();
        },
        
        showSuccess(message) {
            this.showNotification(message, 'success');
        },
        
        showError(message) {
            this.showNotification(message, 'error');
        },
        
        showNotification(message, type) {
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Resume Generator with form validation
function resumeGenerator() {
    return {
        formData: {
            name: '',
            email: '',
            phone: '',
            address: '',
            objective: '',
            experience: [],
            education: [],
            skills: [],
            projects: []
        },
        currentStep: 1,
        totalSteps: 4,
        processing: false,
        
        addExperience() {
            this.formData.experience.push({
                company: '',
                position: '',
                duration: '',
                description: ''
            });
        },
        
        removeExperience(index) {
            this.formData.experience.splice(index, 1);
        },
        
        addEducation() {
            this.formData.education.push({
                institution: '',
                degree: '',
                year: '',
                grade: ''
            });
        },
        
        removeEducation(index) {
            this.formData.education.splice(index, 1);
        },
        
        addSkill() {
            this.formData.skills.push('');
        },
        
        removeSkill(index) {
            this.formData.skills.splice(index, 1);
        },
        
        nextStep() {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
            }
        },
        
        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
            }
        },
        
        async generateResume() {
            if (!this.validateForm()) return;
            
            this.processing = true;
            
            try {
                const response = await fetch('/api/tools/resume-generator', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    this.downloadFile(result.filename);
                    this.showSuccess('Resume generated successfully!');
                } else {
                    this.showError(result.message || 'Generation failed');
                }
            } catch (error) {
                this.showError('Network error occurred');
            }
            
            this.processing = false;
        },
        
        validateForm() {
            if (!this.formData.name.trim()) {
                this.showError('Name is required');
                return false;
            }
            if (!this.formData.email.trim()) {
                this.showError('Email is required');
                return false;
            }
            return true;
        },
        
        downloadFile(filename) {
            const a = document.createElement('a');
            a.href = `/api/download/${filename}`;
            a.download = filename;
            a.click();
        },
        
        showSuccess(message) {
            this.showNotification(message, 'success');
        },
        
        showError(message) {
            this.showNotification(message, 'error');
        },
        
        showNotification(message, type) {
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Generic Tool Handler (fallback for tools without specific handlers)
function genericToolHandler(toolName) {
    return {
        files: [],
        processing: false,
        progress: 0,
        dragover: false,
        
        handleDrop(event) {
            this.dragover = false;
            this.handleFiles(event.dataTransfer.files);
        },
        
        handleFiles(files) {
            this.files = Array.from(files);
        },
        
        removeFile(index) {
            this.files.splice(index, 1);
        },
        
        async processFiles() {
            if (this.files.length === 0) {
                this.showError('Please select files to process');
                return;
            }
            
            this.processing = true;
            this.progress = 0;
            
            const formData = new FormData();
            this.files.forEach((file, index) => {
                formData.append(`file_${index}`, file);
            });
            
            // Simulate progress
            const progressInterval = setInterval(() => {
                this.progress += 10;
                if (this.progress >= 90) clearInterval(progressInterval);
            }, 300);
            
            try {
                const response = await fetch(`/api/tools/generic/${toolName}`, {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                clearInterval(progressInterval);
                this.progress = 100;
                
                if (result.success) {
                    if (result.filename) {
                        this.downloadFile(result.filename);
                    }
                    this.showSuccess(result.message || 'Processing completed successfully!');
                } else {
                    this.showError(result.message || 'Processing failed');
                }
            } catch (error) {
                clearInterval(progressInterval);
                this.showError('Network error occurred');
            }
            
            this.processing = false;
        },
        
        downloadFile(filename) {
            const a = document.createElement('a');
            a.href = `/api/download/${filename}`;
            a.download = filename;
            a.click();
        },
        
        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        showSuccess(message) {
            this.showNotification(message, 'success');
        },
        
        showError(message) {
            this.showNotification(message, 'error');
        },
        
        showNotification(message, type) {
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 5000);
        }
    };
}

// Export functions for use in templates
window.pdfMerger = pdfMerger;
window.imageCompressor = imageCompressor;
window.qrGenerator = qrGenerator;
window.videoTrimmer = videoTrimmer;
window.resumeGenerator = resumeGenerator;
window.genericToolHandler = genericToolHandler;