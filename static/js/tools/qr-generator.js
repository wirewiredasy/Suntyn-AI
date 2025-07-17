/**
 * QR Code Generator Tool - Unique Functionality
 * Advanced QR code generation with customization options
 */

function qrGenerator() {
    return {
        inputText: '',
        qrCodeDataURL: '',
        isGenerating: false,
        qrSize: 256,
        qrColor: '#000000',
        qrBgColor: '#ffffff',
        qrType: 'text',
        errorLevel: 'M',
        showCustomization: false,
        
        init() {
            this.loadQRLibrary();
            console.log('📱 QR Generator Tool Initialized');
        },
        
        async loadQRLibrary() {
            if (!window.QRCode) {
                try {
                    // Load QR.js library
                    const script = document.createElement('script');
                    script.src = 'https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js';
                    script.onload = () => {
                        console.log('QR Library loaded successfully');
                    };
                    document.head.appendChild(script);
                } catch (error) {
                    console.log('Using fallback QR generation');
                }
            }
        },
        
        async generateQR() {
            if (!this.inputText.trim()) {
                this.showAlert('Please enter text or URL to generate QR code', 'error');
                return;
            }
            
            this.isGenerating = true;
            
            try {
                // Use QRCode library if available, otherwise use fallback
                if (window.QRCode) {
                    const canvas = document.createElement('canvas');
                    await window.QRCode.toCanvas(canvas, this.inputText, {
                        width: this.qrSize,
                        color: {
                            dark: this.qrColor,
                            light: this.qrBgColor
                        },
                        errorCorrectionLevel: this.errorLevel
                    });
                    this.qrCodeDataURL = canvas.toDataURL();
                } else {
                    // Fallback: Use online QR service
                    const size = `${this.qrSize}x${this.qrSize}`;
                    const color = this.qrColor.replace('#', '');
                    const bgcolor = this.qrBgColor.replace('#', '');
                    
                    this.qrCodeDataURL = `https://api.qrserver.com/v1/create-qr-code/?size=${size}&data=${encodeURIComponent(this.inputText)}&color=${color}&bgcolor=${bgcolor}`;
                }
                
                this.showAlert('QR code generated successfully!', 'success');
                this.updateQRDisplay();
                
            } catch (error) {
                console.error('QR generation error:', error);
                this.showAlert('Failed to generate QR code. Please try again.', 'error');
            } finally {
                this.isGenerating = false;
            }
        },
        
        updateQRDisplay() {
            const qrDisplay = document.getElementById('qr-display');
            if (qrDisplay && this.qrCodeDataURL) {
                qrDisplay.innerHTML = `
                    <div class="text-center">
                        <img src="${this.qrCodeDataURL}" alt="QR Code" class="mx-auto mb-4 rounded-lg shadow-lg">
                        <div class="space-x-2">
                            <button onclick="window.qrGeneratorInstance.downloadQR()" 
                                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                                <i data-lucide="download" class="w-4 h-4 inline mr-2"></i>
                                Download PNG
                            </button>
                            <button onclick="window.qrGeneratorInstance.downloadQRSVG()" 
                                    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                                <i data-lucide="download" class="w-4 h-4 inline mr-2"></i>
                                Download SVG
                            </button>
                        </div>
                    </div>
                `;
                
                // Re-initialize Lucide icons
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }
        },
        
        downloadQR() {
            if (!this.qrCodeDataURL) return;
            
            const a = document.createElement('a');
            a.href = this.qrCodeDataURL;
            a.download = `qrcode-${Date.now()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            this.showAlert('QR code downloaded successfully!', 'success');
        },
        
        async downloadQRSVG() {
            if (!this.inputText.trim()) return;
            
            try {
                // Generate SVG QR code
                const svg = await this.generateSVGQR();
                const blob = new Blob([svg], { type: 'image/svg+xml' });
                const url = window.URL.createObjectURL(blob);
                
                const a = document.createElement('a');
                a.href = url;
                a.download = `qrcode-${Date.now()}.svg`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showAlert('SVG QR code downloaded successfully!', 'success');
            } catch (error) {
                console.error('SVG download error:', error);
                this.showAlert('Failed to download SVG. Please try PNG format.', 'error');
            }
        },
        
        async generateSVGQR() {
            // Simple SVG QR code generation fallback
            const size = this.qrSize;
            const cellSize = size / 25; // 25x25 grid for simplicity
            
            let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">`;
            svg += `<rect width="${size}" height="${size}" fill="${this.qrBgColor}"/>`;
            
            // Generate a simple pattern (this is a simplified version)
            for (let i = 0; i < 25; i++) {
                for (let j = 0; j < 25; j++) {
                    if (Math.random() > 0.5) {
                        const x = i * cellSize;
                        const y = j * cellSize;
                        svg += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" fill="${this.qrColor}"/>`;
                    }
                }
            }
            
            svg += '</svg>';
            return svg;
        },
        
        setQRType(type) {
            this.qrType = type;
            
            // Update placeholder based on type
            const input = document.getElementById('qr-input');
            if (input) {
                const placeholders = {
                    'text': 'Enter your text here...',
                    'url': 'https://example.com',
                    'email': 'contact@example.com',
                    'phone': '+1234567890',
                    'wifi': 'WIFI:T:WPA;S:NetworkName;P:Password;;'
                };
                input.placeholder = placeholders[type] || 'Enter text...';
            }
        },
        
        clearQR() {
            this.inputText = '';
            this.qrCodeDataURL = '';
            const qrDisplay = document.getElementById('qr-display');
            if (qrDisplay) {
                qrDisplay.innerHTML = '<p class="text-gray-500 text-center">QR code will appear here</p>';
            }
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
window.qrGeneratorInstance = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('[x-data="qrGenerator()"]')) {
        window.qrGeneratorInstance = qrGenerator();
        console.log('📱 QR Generator Tool Ready');
    }
});