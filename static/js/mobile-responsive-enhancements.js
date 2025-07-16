/**
 * Mobile Responsive Enhancements for Toolora AI
 * Optimizes user experience across all device sizes
 */

// Mobile-first responsive utilities
const MobileUtils = {
    // Detect device type
    isMobile() {
        return window.innerWidth <= 768;
    },
    
    isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    },
    
    isDesktop() {
        return window.innerWidth > 1024;
    },
    
    // Touch device detection
    isTouchDevice() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    },
    
    // Optimize file upload for mobile
    optimizeFileUpload() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            if (this.isMobile()) {
                // Add mobile-specific attributes
                input.setAttribute('accept', input.getAttribute('accept') || '*');
                input.setAttribute('capture', 'environment');
                
                // Improve click target size
                const wrapper = input.closest('.file-upload-wrapper');
                if (wrapper) {
                    wrapper.style.minHeight = '44px';
                    wrapper.style.padding = '12px';
                }
            }
        });
    },
    
    // Optimize drag and drop for mobile
    optimizeDragDrop() {
        const dropZones = document.querySelectorAll('[data-drop-zone]');
        dropZones.forEach(zone => {
            if (this.isTouchDevice()) {
                // Add touch-friendly drag and drop
                zone.addEventListener('touchstart', this.handleTouchStart.bind(this));
                zone.addEventListener('touchmove', this.handleTouchMove.bind(this));
                zone.addEventListener('touchend', this.handleTouchEnd.bind(this));
            }
        });
    },
    
    // Handle touch events for drag and drop
    handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        this.touchStartX = touch.clientX;
        this.touchStartY = touch.clientY;
    },
    
    handleTouchMove(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const deltaX = touch.clientX - this.touchStartX;
        const deltaY = touch.clientY - this.touchStartY;
        
        // Visual feedback for drag
        e.target.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    },
    
    handleTouchEnd(e) {
        e.preventDefault();
        e.target.style.transform = '';
        
        // Trigger file selection on touch end
        const fileInput = e.target.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.click();
        }
    },
    
    // Optimize buttons for mobile
    optimizeButtons() {
        const buttons = document.querySelectorAll('button, .btn');
        buttons.forEach(button => {
            if (this.isMobile()) {
                // Ensure minimum touch target size
                const styles = window.getComputedStyle(button);
                const height = parseInt(styles.height);
                const padding = parseInt(styles.padding);
                
                if (height + padding * 2 < 44) {
                    button.style.minHeight = '44px';
                    button.style.padding = '12px 16px';
                }
                
                // Add touch feedback
                button.addEventListener('touchstart', () => {
                    button.style.opacity = '0.7';
                });
                
                button.addEventListener('touchend', () => {
                    button.style.opacity = '1';
                });
            }
        });
    },
    
    // Optimize form inputs
    optimizeFormInputs() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (this.isMobile()) {
                // Improve input accessibility
                input.style.fontSize = '16px'; // Prevent zoom on iOS
                input.style.minHeight = '44px';
                
                // Add appropriate input types
                if (input.type === 'text') {
                    if (input.name.includes('email')) {
                        input.type = 'email';
                    } else if (input.name.includes('phone')) {
                        input.type = 'tel';
                    } else if (input.name.includes('url')) {
                        input.type = 'url';
                    }
                }
            }
        });
    },
    
    // Optimize modals for mobile
    optimizeModals() {
        const modals = document.querySelectorAll('.modal, [data-modal]');
        modals.forEach(modal => {
            if (this.isMobile()) {
                modal.style.margin = '0';
                modal.style.borderRadius = '16px 16px 0 0';
                modal.style.maxHeight = '90vh';
                modal.style.overflow = 'auto';
                
                // Add swipe to close
                let startY = 0;
                modal.addEventListener('touchstart', (e) => {
                    startY = e.touches[0].clientY;
                });
                
                modal.addEventListener('touchmove', (e) => {
                    const currentY = e.touches[0].clientY;
                    const deltaY = currentY - startY;
                    
                    if (deltaY > 50) {
                        modal.style.transform = `translateY(${deltaY - 50}px)`;
                    }
                });
                
                modal.addEventListener('touchend', (e) => {
                    const currentY = e.changedTouches[0].clientY;
                    const deltaY = currentY - startY;
                    
                    if (deltaY > 100) {
                        modal.style.display = 'none';
                    }
                    modal.style.transform = '';
                });
            }
        });
    },
    
    // Optimize navigation for mobile
    optimizeNavigation() {
        const nav = document.querySelector('nav');
        if (nav && this.isMobile()) {
            // Add mobile menu toggle
            const menuToggle = document.createElement('button');
            menuToggle.innerHTML = '☰';
            menuToggle.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                background: white;
                border: none;
                border-radius: 50%;
                width: 44px;
                height: 44px;
                font-size: 18px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            `;
            
            menuToggle.addEventListener('click', () => {
                nav.classList.toggle('mobile-menu-open');
            });
            
            document.body.appendChild(menuToggle);
        }
    },
    
    // Optimize progress bars for mobile
    optimizeProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            if (this.isMobile()) {
                bar.style.height = '8px';
                bar.style.borderRadius = '4px';
                
                // Add haptic feedback for progress updates
                if (navigator.vibrate) {
                    const observer = new MutationObserver(() => {
                        navigator.vibrate(50);
                    });
                    observer.observe(bar, { attributes: true });
                }
            }
        });
    },
    
    // Optimize file previews for mobile
    optimizeFilePreviews() {
        const previews = document.querySelectorAll('.file-preview');
        previews.forEach(preview => {
            if (this.isMobile()) {
                preview.style.padding = '8px';
                preview.style.fontSize = '14px';
                
                // Add swipe to remove
                let startX = 0;
                preview.addEventListener('touchstart', (e) => {
                    startX = e.touches[0].clientX;
                });
                
                preview.addEventListener('touchmove', (e) => {
                    const currentX = e.touches[0].clientX;
                    const deltaX = currentX - startX;
                    
                    if (Math.abs(deltaX) > 20) {
                        preview.style.transform = `translateX(${deltaX}px)`;
                        preview.style.opacity = 1 - Math.abs(deltaX) / 200;
                    }
                });
                
                preview.addEventListener('touchend', (e) => {
                    const currentX = e.changedTouches[0].clientX;
                    const deltaX = currentX - startX;
                    
                    if (Math.abs(deltaX) > 100) {
                        preview.remove();
                    } else {
                        preview.style.transform = '';
                        preview.style.opacity = '';
                    }
                });
            }
        });
    },
    
    // Add keyboard shortcuts for accessibility
    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + U for upload
            if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
                e.preventDefault();
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) fileInput.click();
            }
            
            // Ctrl/Cmd + Enter for process
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                const processButton = document.querySelector('[data-process-button]');
                if (processButton) processButton.click();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                const modal = document.querySelector('.modal:not([style*="display: none"])');
                if (modal) modal.style.display = 'none';
            }
        });
    },
    
    // Initialize all mobile optimizations
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.optimizeFileUpload();
            this.optimizeDragDrop();
            this.optimizeButtons();
            this.optimizeFormInputs();
            this.optimizeModals();
            this.optimizeNavigation();
            this.optimizeProgressBars();
            this.optimizeFilePreviews();
            this.addKeyboardShortcuts();
            
            // Re-optimize on resize
            window.addEventListener('resize', () => {
                this.optimizeButtons();
                this.optimizeFormInputs();
            });
        });
    }
};

// Performance monitoring for mobile
const PerformanceMonitor = {
    trackPageLoad() {
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            if (loadTime > 3000) {
                console.warn('Page load time:', loadTime, 'ms');
            }
        });
    },
    
    trackFileProcessing(toolName) {
        const startTime = performance.now();
        return () => {
            const endTime = performance.now();
            const processingTime = endTime - startTime;
            
            // Send analytics (if needed)
            if (processingTime > 5000) {
                console.warn(`${toolName} processing time:`, processingTime, 'ms');
            }
        };
    },
    
    optimizeImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (MobileUtils.isMobile()) {
                // Add loading optimization
                img.loading = 'lazy';
                img.decoding = 'async';
                
                // Compress images on mobile
                if (img.naturalWidth > 800) {
                    img.style.maxWidth = '100%';
                    img.style.height = 'auto';
                }
            }
        });
    },
    
    init() {
        this.trackPageLoad();
        this.optimizeImages();
    }
};

// Accessibility enhancements
const AccessibilityUtils = {
    addAriaLabels() {
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            const text = button.textContent.trim();
            if (text) {
                button.setAttribute('aria-label', text);
            }
        });
    },
    
    addFocusIndicators() {
        const focusableElements = document.querySelectorAll('button, input, select, textarea, a[href]');
        focusableElements.forEach(element => {
            element.addEventListener('focus', () => {
                element.style.outline = '2px solid #3b82f6';
                element.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', () => {
                element.style.outline = '';
                element.style.outlineOffset = '';
            });
        });
    },
    
    addScreenReaderSupport() {
        // Add live region for status updates
        const statusRegion = document.createElement('div');
        statusRegion.setAttribute('aria-live', 'polite');
        statusRegion.setAttribute('aria-atomic', 'true');
        statusRegion.className = 'sr-only';
        statusRegion.id = 'status-region';
        document.body.appendChild(statusRegion);
        
        // Function to announce status
        window.announceStatus = (message) => {
            statusRegion.textContent = message;
        };
    },
    
    init() {
        this.addAriaLabels();
        this.addFocusIndicators();
        this.addScreenReaderSupport();
    }
};

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', () => {
    MobileUtils.init();
    PerformanceMonitor.init();
    AccessibilityUtils.init();
});

// Export for use in other modules
window.MobileUtils = MobileUtils;
window.PerformanceMonitor = PerformanceMonitor;
window.AccessibilityUtils = AccessibilityUtils;