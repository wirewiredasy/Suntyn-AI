// Tool-specific handlers and utilities
class ToolHandler {
    constructor() {
        this.activeTools = new Map();
        this.processingQueue = [];
        this.maxConcurrentProcessing = 3;
        this.currentProcessing = 0;
    }

    registerTool(name, handler) {
        this.activeTools.set(name, handler);
    }

    async processTool(toolName, files, options = {}) {
        const handler = this.activeTools.get(toolName);
        if (!handler) {
            throw new Error(`Tool ${toolName} is not registered`);
        }

        return new Promise((resolve, reject) => {
            const task = {
                toolName,
                files,
                options,
                resolve,
                reject
            };

            this.processingQueue.push(task);
            this.processQueue();
        });
    }

    async processQueue() {
        if (this.currentProcessing >= this.maxConcurrentProcessing || this.processingQueue.length === 0) {
            return;
        }

        this.currentProcessing++;
        const task = this.processingQueue.shift();

        try {
            const handler = this.activeTools.get(task.toolName);
            const result = await handler(task.files, task.options);
            task.resolve(result);
        } catch (error) {
            task.reject(error);
        } finally {
            this.currentProcessing--;
            this.processQueue();
        }
    }

    getProcessingStatus() {
        return {
            active: this.currentProcessing,
            queued: this.processingQueue.length,
            total: this.currentProcessing + this.processingQueue.length
        };
    }
}

// Initialize tool handler
const toolHandler = new ToolHandler();

// PDF Tools
class PDFToolHandler {
    static async merge(files, options = {}) {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        
        const response = await fetch('/api/pdf/merge', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to merge PDFs');
        }
        
        return result;
    }

    static async split(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('pages_per_file', options.pagesPerFile || 1);
        
        const response = await fetch('/api/pdf/split', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to split PDF');
        }
        
        return result;
    }

    static async compress(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('quality', options.quality || 0.7);
        
        const response = await fetch('/api/pdf/compress', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to compress PDF');
        }
        
        return result;
    }

    static async addWatermark(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('watermark_text', options.watermarkText || 'Watermark');
        formData.append('position', options.position || 'center');
        formData.append('opacity', options.opacity || 0.5);
        
        const response = await fetch('/api/pdf/watermark', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to add watermark');
        }
        
        return result;
    }

    static async rotate(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('rotation', options.rotation || 90);
        
        const response = await fetch('/api/pdf/rotate', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to rotate PDF');
        }
        
        return result;
    }

    static async extractPages(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('pages', JSON.stringify(options.pages || [1]));
        
        const response = await fetch('/api/pdf/extract-pages', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to extract pages');
        }
        
        return result;
    }
}

// Image Tools
class ImageToolHandler {
    static async compress(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('quality', options.quality || 85);
        formData.append('format', options.format || 'jpeg');
        
        const response = await fetch('/api/image/compress', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to compress image');
        }
        
        return result;
    }

    static async resize(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('width', options.width || 800);
        formData.append('height', options.height || 600);
        formData.append('maintain_aspect', options.maintainAspect !== false);
        
        const response = await fetch('/api/image/resize', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to resize image');
        }
        
        return result;
    }

    static async convert(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('format', options.format || 'png');
        
        const response = await fetch('/api/image/convert', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to convert image');
        }
        
        return result;
    }

    static async crop(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('x', options.x || 0);
        formData.append('y', options.y || 0);
        formData.append('width', options.width || 100);
        formData.append('height', options.height || 100);
        
        const response = await fetch('/api/image/crop', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to crop image');
        }
        
        return result;
    }

    static async rotate(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('angle', options.angle || 90);
        
        const response = await fetch('/api/image/rotate', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to rotate image');
        }
        
        return result;
    }

    static async addWatermark(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('watermark_text', options.watermarkText || 'Watermark');
        formData.append('position', options.position || 'bottom-right');
        formData.append('opacity', options.opacity || 0.7);
        
        const response = await fetch('/api/image/watermark', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to add watermark');
        }
        
        return result;
    }

    static async removeBackground(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/image/remove-background', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to remove background');
        }
        
        return result;
    }
}

// Video Tools
class VideoToolHandler {
    static async trim(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('start_time', options.startTime || 0);
        formData.append('end_time', options.endTime || 10);
        
        const response = await fetch('/api/video/trim', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to trim video');
        }
        
        return result;
    }

    static async extractAudio(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('format', options.format || 'mp3');
        
        const response = await fetch('/api/video/extract-audio', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to extract audio');
        }
        
        return result;
    }

    static async compress(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('quality', options.quality || 'medium');
        
        const response = await fetch('/api/video/compress', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to compress video');
        }
        
        return result;
    }

    static async convert(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('format', options.format || 'mp4');
        
        const response = await fetch('/api/video/convert', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to convert video');
        }
        
        return result;
    }

    static async cropVertical(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('aspect_ratio', options.aspectRatio || '9:16');
        
        const response = await fetch('/api/video/crop-vertical', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to crop video');
        }
        
        return result;
    }
}

// AI Tools
class AIToolHandler {
    static async generateResume(data, options = {}) {
        const response = await fetch('/api/ai/resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate resume');
        }
        
        return result;
    }

    static async generateBusinessNames(data, options = {}) {
        const response = await fetch('/api/ai/business-names', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate business names');
        }
        
        return result;
    }

    static async generateBlogTitles(data, options = {}) {
        const response = await fetch('/api/ai/blog-titles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate blog titles');
        }
        
        return result;
    }

    static async generateProductDescription(data, options = {}) {
        const response = await fetch('/api/ai/product-description', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate product description');
        }
        
        return result;
    }

    static async generateAdCopy(data, options = {}) {
        const response = await fetch('/api/ai/ad-copy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate ad copy');
        }
        
        return result;
    }
}

// Register all tools
toolHandler.registerTool('pdf-merge', PDFToolHandler.merge);
toolHandler.registerTool('pdf-split', PDFToolHandler.split);
toolHandler.registerTool('pdf-compress', PDFToolHandler.compress);
toolHandler.registerTool('pdf-watermark', PDFToolHandler.addWatermark);
toolHandler.registerTool('pdf-rotate', PDFToolHandler.rotate);
toolHandler.registerTool('pdf-extract-pages', PDFToolHandler.extractPages);

toolHandler.registerTool('image-compress', ImageToolHandler.compress);
toolHandler.registerTool('image-resize', ImageToolHandler.resize);
toolHandler.registerTool('image-convert', ImageToolHandler.convert);
toolHandler.registerTool('image-crop', ImageToolHandler.crop);
toolHandler.registerTool('image-rotate', ImageToolHandler.rotate);
toolHandler.registerTool('image-watermark', ImageToolHandler.addWatermark);
toolHandler.registerTool('background-remover', ImageToolHandler.removeBackground);

toolHandler.registerTool('video-trim', VideoToolHandler.trim);
toolHandler.registerTool('video-extract-audio', VideoToolHandler.extractAudio);
toolHandler.registerTool('video-compress', VideoToolHandler.compress);
toolHandler.registerTool('video-convert', VideoToolHandler.convert);
toolHandler.registerTool('video-crop-vertical', VideoToolHandler.cropVertical);

toolHandler.registerTool('resume-generator', AIToolHandler.generateResume);
toolHandler.registerTool('business-name-generator', AIToolHandler.generateBusinessNames);
toolHandler.registerTool('blog-title-generator', AIToolHandler.generateBlogTitles);
toolHandler.registerTool('product-description', AIToolHandler.generateProductDescription);
toolHandler.registerTool('ad-copy-generator', AIToolHandler.generateAdCopy);

// Export for global use
window.toolHandler = toolHandler;
window.PDFToolHandler = PDFToolHandler;
window.ImageToolHandler = ImageToolHandler;
window.VideoToolHandler = VideoToolHandler;
window.AIToolHandler = AIToolHandler;
