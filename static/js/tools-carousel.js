// Auto-Scrolling Tools Carousel
class ToolsCarousel {
    constructor() {
        this.currentSlide = 0;
        this.slideInterval = null;
        this.slideDuration = 3000; // 3 seconds
        this.tools = this.getToolsData();
        this.init();
    }

    getToolsData() {
        return [
            {
                name: 'PDF Merge',
                category: 'PDF Tools',
                description: 'Combine multiple PDF files into a single document with ease. Perfect for merging reports, contracts, and presentations.',
                icon: 'file-text',
                color: 'red',
                usage: '50K+',
                url: '/tools/pdf-merge'
            },
            {
                name: 'Image Compress',
                category: 'Image Tools', 
                description: 'Reduce image file sizes while maintaining quality. Optimize images for web and mobile applications.',
                icon: 'image',
                color: 'green',
                usage: '45K+',
                url: '/tools/image-compress'
            },
            {
                name: 'Video Trimmer',
                category: 'Video & Audio',
                description: 'Cut and trim video files to exact specifications. Remove unwanted sections with precision.',
                icon: 'video',
                color: 'purple',
                usage: '30K+',
                url: '/tools/video-trim'
            },
            {
                name: 'AI Resume Generator',
                category: 'AI Tools',
                description: 'Create professional resumes using AI technology. Generate compelling content tailored to your industry.',
                icon: 'brain',
                color: 'violet',
                usage: '25K+',
                url: '/tools/resume-generator'
            },
            {
                name: 'QR Code Generator',
                category: 'Utility Tools',
                description: 'Generate custom QR codes for URLs, text, contacts, and more. Perfect for marketing and sharing.',
                icon: 'qr-code',
                color: 'slate',
                usage: '40K+',
                url: '/tools/qr-generator'
            },
            {
                name: 'Background Remover',
                category: 'Image Tools',
                description: 'Remove backgrounds from images automatically using AI. Create transparent PNGs instantly.',
                icon: 'scissors',
                color: 'green',
                usage: '35K+',
                url: '/tools/background-remover'
            }
        ];
    }

    init() {
        this.createCarouselSlides();
        this.createIndicators();
        this.startAutoSlide();
        this.addEventListeners();
    }

    createCarouselSlides() {
        const track = document.getElementById('carouselTrack');
        if (!track) return;

        track.innerHTML = '';

        this.tools.forEach((tool, index) => {
            const slide = this.createSlide(tool, index);
            track.appendChild(slide);
        });

        // Set initial width
        track.style.width = `${this.tools.length * 100}%`;
    }

    createSlide(tool, index) {
        const slide = document.createElement('div');
        slide.className = 'carousel-slide flex-shrink-0 px-4';
        slide.style.width = `${100 / this.tools.length}%`;

        slide.innerHTML = `
            <div class="tool-card bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 h-full">
                <!-- Tool Icon Header -->
                <div class="bg-gradient-to-br from-${tool.color}-500 to-${tool.color}-600 h-32 flex items-center justify-center relative overflow-hidden">
                    <div class="absolute inset-0 bg-gradient-to-br from-transparent via-white/10 to-transparent"></div>
                    <div class="relative z-10 w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                        <i data-lucide="${tool.icon}" class="w-8 h-8 text-white"></i>
                    </div>
                    <div class="absolute top-4 right-4">
                        <div class="bg-white/20 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-full font-semibold">
                            ${tool.usage}
                        </div>
                    </div>
                </div>

                <!-- Tool Content -->
                <div class="p-6">
                    <div class="mb-3">
                        <span class="inline-block bg-${tool.color}-50 dark:bg-${tool.color}-900/20 text-${tool.color}-600 dark:text-${tool.color}-400 text-xs px-2 py-1 rounded-full font-medium">
                            ${tool.category}
                        </span>
                    </div>
                    
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3 line-clamp-2">
                        ${tool.name}
                    </h3>
                    
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed mb-6 line-clamp-3">
                        ${tool.description}
                    </p>
                    
                    <a href="${tool.url}" 
                       class="inline-flex items-center justify-center w-full bg-gradient-to-r from-${tool.color}-600 to-${tool.color}-700 hover:from-${tool.color}-700 hover:to-${tool.color}-800 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 group">
                        <span>Try Tool</span>
                        <i data-lucide="arrow-right" class="w-4 h-4 ml-2 transition-transform duration-200 group-hover:translate-x-0.5"></i>
                    </a>
                </div>
            </div>
        `;

        return slide;
    }

    createIndicators() {
        const indicatorsContainer = document.getElementById('carouselIndicators');
        if (!indicatorsContainer) return;

        indicatorsContainer.innerHTML = '';

        for (let i = 0; i < this.tools.length; i++) {
            const indicator = document.createElement('button');
            indicator.className = `w-2 h-2 rounded-full transition-all duration-300 ${
                i === 0 ? 'bg-cyan-400' : 'bg-gray-600'
            }`;
            indicator.addEventListener('click', () => this.goToSlide(i));
            indicatorsContainer.appendChild(indicator);
        }
    }

    goToSlide(slideIndex) {
        this.currentSlide = slideIndex;
        this.updateCarousel();
        this.updateIndicators();
        this.restartAutoSlide();
    }

    updateCarousel() {
        const track = document.getElementById('carouselTrack');
        if (!track) return;

        const translateX = -(this.currentSlide * (100 / this.tools.length));
        track.style.transform = `translateX(${translateX}%)`;
    }

    updateIndicators() {
        const indicators = document.querySelectorAll('#carouselIndicators button');
        indicators.forEach((indicator, index) => {
            if (index === this.currentSlide) {
                indicator.className = 'w-2 h-2 rounded-full transition-all duration-300 bg-cyan-400';
            } else {
                indicator.className = 'w-2 h-2 rounded-full transition-all duration-300 bg-gray-600';
            }
        });
    }

    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.tools.length;
        this.updateCarousel();
        this.updateIndicators();
    }

    startAutoSlide() {
        this.slideInterval = setInterval(() => {
            this.nextSlide();
        }, this.slideDuration);
    }

    restartAutoSlide() {
        clearInterval(this.slideInterval);
        this.startAutoSlide();
    }

    addEventListeners() {
        const carousel = document.getElementById('toolsCarousel');
        if (!carousel) return;

        // Pause on hover
        carousel.addEventListener('mouseenter', () => {
            clearInterval(this.slideInterval);
        });

        carousel.addEventListener('mouseleave', () => {
            this.startAutoSlide();
        });
    }
}

// Initialize carousel when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ToolsCarousel();
});