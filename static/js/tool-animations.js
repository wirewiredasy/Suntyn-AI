// Enhanced animations and interactions for tools
class ToolAnimationManager {
    constructor() {
        this.initializeAnimations();
        this.setupIntersectionObserver();
        this.setupHoverEffects();
        this.setupLoadingAnimations();
    }

    initializeAnimations() {
        // Add stagger animation to tool cards
        this.staggerToolCards();

        // Add smooth transitions
        this.addSmoothTransitions();

        // Initialize progress animations
        this.initializeProgressAnimations();
    }

    staggerToolCards() {
        const toolCards = document.querySelectorAll('.tool-card');
        toolCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('animate-fade-in-up');
        });
    }

    addSmoothTransitions() {
        const style = document.createElement('style');
        style.textContent = `
            .animate-fade-in-up {
                animation: fadeInUp 0.2s ease-out forwards;
                opacity: 0;
                transform: translateY(10px);
            }

            @keyframes fadeInUp {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .tool-card {
                transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
                transform: translateZ(0);
            }

            .tool-card:hover {
                transform: translateY(-4px) scale(1.01) translateZ(0);
                box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1), 0 5px 8px -3px rgba(0, 0, 0, 0.04);
            }

            .processing-animation {
                animation: simpleRotate 1s linear infinite;
            }

            @keyframes simpleRotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .instant-feedback {
                animation: quickBounce 0.3s ease-out;
            }

            @keyframes quickBounce {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }

            .progress-bar {
                transition: width 0.5s ease-out;
            }

            .bounce-in {
                animation: bounceIn 0.6s ease-out;
            }

            @keyframes bounceIn {
                0% { transform: scale(0.3); opacity: 0; }
                50% { transform: scale(1.05); }
                70% { transform: scale(0.9); }
                100% { transform: scale(1); opacity: 1; }
            }

            .slide-in-right {
                animation: slideInRight 0.5s ease-out;
            }

            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            .rotate-in {
                animation: rotateIn 0.5s ease-out;
            }

            @keyframes rotateIn {
                from { transform: rotate(-180deg) scale(0); opacity: 0; }
                to { transform: rotate(0deg) scale(1); opacity: 1; }
            }

            .shake {
                animation: shake 0.5s ease-in-out;
            }

            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            .glow {
                animation: glow 2s ease-in-out infinite alternate;
            }

            @keyframes glow {
                from { box-shadow: 0 0 10px rgba(59, 130, 246, 0.3); }
                to { box-shadow: 0 0 10px rgba(59, 130, 246, 0.3); }
            }
        `;
        document.head.appendChild(style);
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        // Observe all tool cards
        document.querySelectorAll('.tool-card').forEach(card => {
            observer.observe(card);
        });
    }

    setupHoverEffects() {
        document.addEventListener('DOMContentLoaded', () => {
            // Add hover effects to buttons
            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(button => {
                button.addEventListener('mouseenter', () => {
                    button.style.transform = 'translateY(-2px)';
                });

                button.addEventListener('mouseleave', () => {
                    button.style.transform = 'translateY(0)';
                });
            });

            // Add ripple effect to buttons
            this.addRippleEffect();
        });
    }

    addRippleEffect() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const ripple = document.createElement('span');
                const rect = button.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                `;

                button.style.position = 'relative';
                button.style.overflow = 'hidden';
                button.appendChild(ripple);

                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });

        // Add ripple animation
        const rippleStyle = document.createElement('style');
        rippleStyle.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(rippleStyle);
    }

    setupLoadingAnimations() {
        // Create loading spinner component
        window.createLoadingSpinner = (color = 'blue') => {
            const spinner = document.createElement('div');
            spinner.className = `inline-block w-6 h-6 border-2 border-${color}-200 border-t-${color}-600 rounded-full animate-spin`;
            return spinner;
        };

        // Create progress bar component
        window.createProgressBar = (progress = 0, color = 'blue') => {
            const container = document.createElement('div');
            container.className = `w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2`;

            const bar = document.createElement('div');
            bar.className = `bg-${color}-600 h-2 rounded-full progress-bar`;
            bar.style.width = `${progress}%`;

            container.appendChild(bar);
            return container;
        };

        // Animate progress updates
        window.animateProgress = (element, targetProgress) => {
            const bar = element.querySelector('.progress-bar');
            if (bar) {
                bar.style.width = `${targetProgress}%`;
            }
        };
    }

    initializeProgressAnimations() {
        // Set up progress tracking for file uploads
        window.trackUploadProgress = (file, progressCallback) => {
            const reader = new FileReader();
            let progress = 0;

            const interval = setInterval(() => {
                progress += Math.random() * 20;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                }
                progressCallback(progress);
            }, 100);

            return interval;
        };
    }

    // Utility methods for animations
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';

        const fadeEffect = setInterval(() => {
            if (!element.style.opacity) {
                element.style.opacity = '0';
            }
            if (parseFloat(element.style.opacity) < 1) {
                element.style.opacity = (parseFloat(element.style.opacity) + 0.1).toString();
            } else {
                clearInterval(fadeEffect);
            }
        }, duration / 10);
    }

    fadeOut(element, duration = 300) {
        const fadeEffect = setInterval(() => {
            if (!element.style.opacity) {
                element.style.opacity = '1';
            }
            if (parseFloat(element.style.opacity) > 0) {
                element.style.opacity = (parseFloat(element.style.opacity) - 0.1).toString();
            } else {
                clearInterval(fadeEffect);
                element.style.display = 'none';
            }
        }, duration / 10);
    }

    slideDown(element, duration = 300) {
        element.style.maxHeight = '0';
        element.style.overflow = 'hidden';
        element.style.transition = `max-height ${duration}ms ease-out`;

        setTimeout(() => {
            element.style.maxHeight = element.scrollHeight + 'px';
        }, 10);
    }

    slideUp(element, duration = 300) {
        element.style.maxHeight = element.scrollHeight + 'px';
        element.style.overflow = 'hidden';
        element.style.transition = `max-height ${duration}ms ease-out`;

        setTimeout(() => {
            element.style.maxHeight = '0';
        }, 10);
    }

    // Success/error animations
    showSuccess(message, duration = 3000) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 bounce-in';
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('slide-in-right');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, duration);
    }

    showError(message, duration = 3000) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 shake';
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('slide-in-right');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, duration);
    }

    // File upload animations
    animateFileUpload(dropZone) {
        dropZone.classList.add('professional-highlight');

        setTimeout(() => {
            dropZone.classList.remove('professional-highlight');
        }, 1000);
    }

    animateFileProcessing(element) {
        element.classList.add('processing-animation');

        return () => {
            element.classList.remove('processing-animation');
        };
    }
}

// Initialize animation manager
const toolAnimationManager = new ToolAnimationManager();

// Simple clean animations only

// Advanced button interaction effects
    setupAdvancedButtonEffects() {
        document.addEventListener('DOMContentLoaded', () => {
            // Enhanced CTA button effects
            const exploreBtn = document.querySelector('.explore-tools-btn');
            const featuredBtn = document.querySelector('.featured-tools-btn');

            if (exploreBtn) {
                this.addMagneticEffect(exploreBtn);
                this.addParticleTrail(exploreBtn);
            }

            if (featuredBtn) {
                this.addMagneticEffect(featuredBtn);
                this.addSparkleEffect(featuredBtn);
            }
        });
    }

    addMagneticEffect(element) {
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            element.style.transform = `translateY(-8px) scale(1.05) rotateX(${y * 0.1}deg) rotateY(${x * 0.1}deg)`;
        });

        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0) scale(1) rotateX(0) rotateY(0)';
        });
    }

    addParticleTrail(element) {
        element.addEventListener('mouseenter', () => {
            for (let i = 0; i < 8; i++) {
                setTimeout(() => {
                    this.createFloatingParticle(element);
                }, i * 100);
            }
        });
    }

    createFloatingParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, #fbbf24, #f59e0b);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            animation: floatUp 2s ease-out forwards;
        `;

        const rect = container.getBoundingClientRect();
        particle.style.left = Math.random() * rect.width + 'px';
        particle.style.top = rect.height + 'px';

        container.appendChild(particle);

        setTimeout(() => {
            particle.remove();
        }, 2000);
    }

    addSparkleEffect(element) {
        element.addEventListener('mouseenter', () => {
            for (let i = 0; i < 12; i++) {
                setTimeout(() => {
                    this.createSparkle(element);
                }, i * 80);
            }
        });
    }

    createSparkle(container) {
        const sparkle = document.createElement('div');
        sparkle.innerHTML = '✨';
        sparkle.style.cssText = `
            position: absolute;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
            animation: sparkleFloat 1.5s ease-out forwards;
        `;

        const rect = container.getBoundingClientRect();
        sparkle.style.left = Math.random() * rect.width + 'px';
        sparkle.style.top = Math.random() * rect.height + 'px';

        container.appendChild(sparkle);

        setTimeout(() => {
            sparkle.remove();
        }, 1500);
    }

    // Add CSS animations
    addAdvancedAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes floatUp {
                0% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-50px) scale(0.5);
                }
            }

            @keyframes sparkleFloat {
                0% {
                    opacity: 0;
                    transform: translateY(0) scale(0) rotate(0deg);
                }
                50% {
                    opacity: 1;
                    transform: translateY(-20px) scale(1) rotate(180deg);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-40px) scale(0) rotate(360deg);
                }
            }

            .explore-tools-btn:hover,
            .featured-tools-btn:hover {
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }

            .floating-particle {
                animation: floatUp 2s ease-out forwards;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize enhanced effects
const advancedAnimationManager = new ToolAnimationManager();
advancedAnimationManager.setupAdvancedButtonEffects();
advancedAnimationManager.addAdvancedAnimations();

// Export for global use
window.toolAnimationManager = toolAnimationManager;
        window.addInstantPageTransitions = this.addInstantPageTransitions.bind(this);