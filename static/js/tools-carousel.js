// Compact Professional Tools Slider
class CompactToolsSlider {
    constructor() {
        this.currentSlide = 0;
        this.slideInterval = null;
        this.slideDuration = 4000; // 4 seconds
        this.tools = this.getToolsData();
        this.toolsPerView = this.getToolsPerView();
        this.init();
    }

    getToolsData() {
        return [
            { name: 'PDF Merge', icon: 'file-text', usage: '50K+', url: '/tools/pdf-merge' },
            { name: 'Image Compress', icon: 'image', usage: '45K+', url: '/tools/image-compress' },
            { name: 'Video Trimmer', icon: 'video', usage: '30K+', url: '/tools/video-trim' },
            { name: 'QR Generator', icon: 'qr-code', usage: '40K+', url: '/tools/qr-generator' },
            { name: 'Resume Builder', icon: 'brain', usage: '25K+', url: '/tools/resume-generator' },
            { name: 'Background Remover', icon: 'scissors', usage: '35K+', url: '/tools/background-remover' },
            { name: 'PDF Split', icon: 'scissors', usage: '28K+', url: '/tools/pdf-split' },
            { name: 'Password Generator', icon: 'shield', usage: '22K+', url: '/tools/password-generator' }
        ];
    }

    getToolsPerView() {
        if (window.innerWidth >= 1024) return 5;
        if (window.innerWidth >= 768) return 4;
        if (window.innerWidth >= 640) return 3;
        return 2;
    }

    init() {
        this.createSliderCards();
        this.createDots();
        this.startAutoSlide();
        this.addEventListeners();
    }

    createSliderCards() {
        const track = document.getElementById('compactSliderTrack');
        if (!track) return;

        track.innerHTML = '';

        this.tools.forEach((tool, index) => {
            const card = this.createCompactCard(tool, index);
            track.appendChild(card);
        });

        this.updateSliderWidth();
    }

    createCompactCard(tool, index) {
        const card = document.createElement('div');
        card.className = 'compact-tool-card flex-shrink-0 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 hover:shadow-lg hover:border-blue-200 dark:hover:border-blue-600 transition-all duration-300 cursor-pointer group';
        card.style.width = `${100 / this.toolsPerView - 1}%`;

        card.innerHTML = `
            <div class="p-4">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                        <i data-lucide="${tool.icon}" class="w-5 h-5 text-white"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <h4 class="text-sm font-semibold text-gray-900 dark:text-white truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                            ${tool.name}
                        </h4>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                            ${tool.usage} users
                        </p>
                    </div>
                    <div class="text-gray-400 group-hover:text-blue-500 transition-colors">
                        <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </div>
                </div>
            </div>
        `;

        card.addEventListener('click', () => {
            window.location.href = tool.url;
        });

        return card;
    }

    createDots() {
        const dotsContainer = document.getElementById('compactSliderDots');
        if (!dotsContainer) return;

        dotsContainer.innerHTML = '';

        const totalSlides = Math.ceil(this.tools.length / this.toolsPerView);
        
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('button');
            dot.className = `w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                i === 0 ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
            }`;
            dot.addEventListener('click', () => this.goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }

    goToSlide(slideIndex) {
        this.currentSlide = slideIndex;
        this.updateSlider();
        this.updateDots();
        this.restartAutoSlide();
    }

    updateSlider() {
        const track = document.getElementById('compactSliderTrack');
        if (!track) return;

        const translateX = -(this.currentSlide * 100);
        track.style.transform = `translateX(${translateX}%)`;
    }

    updateSliderWidth() {
        const track = document.getElementById('compactSliderTrack');
        if (!track) return;

        const totalSlides = Math.ceil(this.tools.length / this.toolsPerView);
        track.style.width = `${totalSlides * 100}%`;
    }

    updateDots() {
        const dots = document.querySelectorAll('#compactSliderDots button');
        dots.forEach((dot, index) => {
            if (index === this.currentSlide) {
                dot.className = 'w-1.5 h-1.5 rounded-full transition-all duration-300 bg-blue-500';
            } else {
                dot.className = 'w-1.5 h-1.5 rounded-full transition-all duration-300 bg-gray-300 dark:bg-gray-600';
            }
        });
    }

    nextSlide() {
        const totalSlides = Math.ceil(this.tools.length / this.toolsPerView);
        this.currentSlide = (this.currentSlide + 1) % totalSlides;
        this.updateSlider();
        this.updateDots();
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
        const slider = document.getElementById('compactToolsSlider');
        if (!slider) return;

        // Pause on hover
        slider.addEventListener('mouseenter', () => {
            clearInterval(this.slideInterval);
        });

        slider.addEventListener('mouseleave', () => {
            this.startAutoSlide();
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            this.toolsPerView = this.getToolsPerView();
            this.currentSlide = 0;
            this.createSliderCards();
            this.createDots();
            this.updateSlider();
        });
    }
}

// Initialize slider when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CompactToolsSlider();
});