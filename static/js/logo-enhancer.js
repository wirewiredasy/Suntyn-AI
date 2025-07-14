
/**
 * Logo Enhancement Script
 * Adds dynamic effects and ensures proper logo loading
 */

class LogoEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.enhanceLogos();
        this.addFloatingParticles();
        this.setupLogoInteractions();
        this.addLoadingAnimation();
    }

    enhanceLogos() {
        // Find all logo elements
        const logos = document.querySelectorAll('img[alt="Toolora AI"]');
        
        logos.forEach(logo => {
            // Add loading class
            logo.classList.add('logo-loading');
            
            // Ensure proper loading
            logo.addEventListener('load', () => {
                logo.classList.remove('logo-loading');
                logo.classList.add('logo-loaded');
            });

            // Add error handling
            logo.addEventListener('error', () => {
                logo.src = '/static/favicon.svg';
                logo.classList.add('logo-fallback');
            });
        });
    }

    addFloatingParticles() {
        const logoContainers = document.querySelectorAll('.logo-container');
        
        logoContainers.forEach(container => {
            container.addEventListener('mouseenter', () => {
                this.createParticles(container);
            });
        });
    }

    createParticles(container) {
        const colors = ['#10B981', '#06B6D4', '#8B5CF6'];
        
        for (let i = 0; i < 6; i++) {
            const particle = document.createElement('div');
            particle.className = 'logo-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: ${colors[i % colors.length]};
                border-radius: 50%;
                pointer-events: none;
                z-index: 10;
                animation: particleFloat 2s ease-out forwards;
            `;
            
            const rect = container.getBoundingClientRect();
            particle.style.left = Math.random() * rect.width + 'px';
            particle.style.top = Math.random() * rect.height + 'px';
            
            container.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 2000);
        }
    }

    setupLogoInteractions() {
        const headerLogos = document.querySelectorAll('.header-logo');
        
        headerLogos.forEach(logo => {
            logo.addEventListener('mouseenter', () => {
                logo.style.animation = 'logoHover 0.6s ease-in-out';
            });
            
            logo.addEventListener('mouseleave', () => {
                logo.style.animation = 'gradientFlow 4s ease infinite';
            });
        });
    }

    addLoadingAnimation() {
        // Add CSS for particles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes particleFloat {
                0% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-30px) scale(0.5);
                }
            }
            
            .logo-particle {
                box-shadow: 0 0 10px currentColor;
            }
            
            .logo-loaded {
                animation: fadeInLogo 1s ease-in-out;
            }
            
            .logo-fallback {
                filter: grayscale(1);
                opacity: 0.8;
            }
            
            /* Sparkle effect */
            .logo-sparkle {
                position: relative;
                overflow: visible;
            }
            
            .logo-sparkle::before {
                content: '✨';
                position: absolute;
                top: -5px;
                right: -5px;
                font-size: 12px;
                opacity: 0;
                animation: sparkleGlow 2s ease-in-out infinite;
            }
            
            .logo-sparkle:hover::before {
                opacity: 1;
            }
            
            @keyframes sparkleGlow {
                0%, 100% { opacity: 0; transform: scale(0.8) rotate(0deg); }
                50% { opacity: 1; transform: scale(1.2) rotate(180deg); }
            }
            
            /* Logo pulse for important states */
            .logo-pulse-success {
                animation: pulseSuccess 1s ease-in-out;
            }
            
            @keyframes pulseSuccess {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); box-shadow: 0 0 20px rgba(16, 185, 129, 0.5); }
                100% { transform: scale(1); }
            }
            
            /* Mobile touch feedback */
            @media (max-width: 768px) {
                .logo-container:active {
                    transform: scale(0.95);
                    transition: transform 0.1s ease;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Public method to trigger logo success animation
    triggerSuccess() {
        const logos = document.querySelectorAll('.logo-container');
        logos.forEach(logo => {
            logo.classList.add('logo-pulse-success');
            setTimeout(() => {
                logo.classList.remove('logo-pulse-success');
            }, 1000);
        });
    }

    // Public method to add sparkle effect
    addSparkles() {
        const logos = document.querySelectorAll('img[alt="Toolora AI"]');
        logos.forEach(logo => {
            logo.classList.add('logo-sparkle');
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.logoEnhancer = new LogoEnhancer();
});

// Export for global use
window.LogoEnhancer = LogoEnhancer;
