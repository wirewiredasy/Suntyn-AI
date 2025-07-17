
// Alpine.js Fallback - Initialize missing data
(function() {
    'use strict';

    // Wait for Alpine to be available or create fallback
    function initializeAlpineData() {
        if (typeof Alpine !== 'undefined') {
            // Alpine is available, set up data
            Alpine.data('toolHandler', () => ({
                files: [],
                processing: false,
                progress: 0,
                results: [],
                dragover: false,
                
                init() {
                    // Initialize component
                },

                addFiles(fileList) {
                    this.files = Array.from(fileList);
                    console.log('Files added:', this.files.length);
                },

                removeFile(index) {
                    this.files.splice(index, 1);
                    console.log('File removed, remaining:', this.files.length);
                },

                async processFiles() {
                    if (this.files.length === 0) {
                        console.log('No files to process');
                        return;
                    }

                    this.processing = true;
                    this.progress = 0;
                    this.results = [];

                    try {
                        // Simulate processing with progress
                        for (let i = 0; i <= 100; i += 20) {
                            this.progress = i;
                            await new Promise(resolve => setTimeout(resolve, 200));
                        }

                        // Create demo results
                        this.results = this.files.map((file, index) => ({
                            id: index,
                            name: `processed_${file.name}`,
                            downloadUrl: '#',
                            size: this.formatFileSize(file.size || 1024000)
                        }));

                        console.log('Processing completed:', this.results);
                    } catch (error) {
                        console.error('Processing error:', error);
                    } finally {
                        this.processing = false;
                    }
                },

                formatFileSize(bytes) {
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                }
            }));

            // Set up global Alpine data
            Alpine.store('toolData', {
                files: [],
                closeMobileMenu() {
                    const sidebar = document.getElementById('mobile-sidebar');
                    if (sidebar) {
                        sidebar.style.transform = 'translateX(-100%)';
                    }
                },
                processing: false,
                progress: 0,
                results: [],
                dragover: false
            });

        } else {
            // Alpine not available, create fallback
            console.log('Alpine.js not found, creating fallback');
            
            // Create global Alpine fallback
            window.Alpine = {
                data: function(name, callback) {
                    window[`alpineData_${name}`] = callback();
                    return window[`alpineData_${name}`];
                },
                store: function(name, data) {
                    window[`alpineStore_${name}`] = data;
                    return data;
                }
            };
            
            // Initialize toolHandler globally
            window.alpineData_toolHandler = {
                files: [],
                processing: false,
                progress: 0,
                results: [],
                dragover: false,
                
                addFiles: function(fileList) {
                    this.files = Array.from(fileList);
                },
                
                removeFile: function(index) {
                    this.files.splice(index, 1);
                },
                
                processFiles: function() {
                    console.log('Processing files in fallback mode');
                    if (window.genericToolHandler) {
                        window.genericToolHandler('default-tool');
                    }
                }
            };
            
            // Make variables globally accessible for templates
            window.processing = false;
            window.progress = 0;
            window.results = [];
            window.files = [];
        }
    }

    // Try to initialize immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAlpineData);
    } else {
        initializeAlpineData();
    }

    // Also try after a short delay to catch late-loading Alpine
    setTimeout(initializeAlpineData, 500);
})();
