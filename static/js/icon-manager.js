class IconManager {
    constructor() {
        this.iconVariants = {
            'toolora-16': '/static/images/toolora-icon-only.svg',
            'toolora-24': '/static/images/toolora-icon-only.svg',
            'toolora-32': '/static/images/toolora-icon-only.svg',
            'toolora-48': '/static/images/toolora-professional-logo.svg',
            'toolora-64': '/static/images/toolora-professional-logo.svg',
            'toolora-mono-minimal': '/static/images/toolora-icon-only.svg',
            'toolora-square-badge': '/static/images/toolora-icon-only.svg',
            'toolora-circle-badge': '/static/images/toolora-icon-only.svg',
            'toolora-modern-square': '/static/images/toolora-professional-logo.svg',
            'toolora-social-square': '/static/images/toolora-professional-logo.svg',
            'toolora-social-rect': '/static/images/toolora-professional-logo.svg',
            'toolora-profile-circle': '/static/images/toolora-professional-logo.svg'
        };
        this.init();
    }

    init() {
        this.setupDynamicIcons();
        this.setupThemeAdaptation();
        this.setupContextualIcons();
    }

    // Get appropriate icon size based on context
    getContextualIcon(context) {
        const sizeMap = {
            'favicon': 'toolora-16',
            'navbar': 'toolora-32',
            'hero': 'toolora-64',
            'footer': 'toolora-24',
            'card': 'toolora-48',
            'social': 'toolora-social-square',
            'profile': 'toolora-profile-circle',
            'badge': 'toolora-square-badge',
            'minimal': 'toolora-mono-minimal'
        };
        return this.iconVariants[sizeMap[context]] || this.iconVariants['toolora-32'];
    }

    // Update all icons on page
    updateAllIcons() {
        // Update favicon
        this.updateFavicon();

        // Update navbar icons
        const navbarIcons = document.querySelectorAll('.navbar-brand img, .logo-navbar');
        navbarIcons.forEach(icon => {
            this.updateIcon(icon, 'navbar');
        });

        // Update hero section icons
        const heroIcons = document.querySelectorAll('.hero-logo, .main-logo');
        heroIcons.forEach(icon => {
            this.updateIcon(icon, 'hero');
        });

        // Update footer icons
        const footerIcons = document.querySelectorAll('.footer-logo');
        footerIcons.forEach(icon => {
            this.updateIcon(icon, 'footer');
        });
    }

    updateIcon(element, context) {
        if (!element) return;

        const iconUrl = this.getContextualIcon(context);

        if (element.tagName === 'IMG') {
            element.src = iconUrl;
        } else if (element.tagName === 'svg' || element.tagName === 'use') {
            element.setAttribute('href', iconUrl);
        }
    }

    updateFavicon() {
        let favicon = document.querySelector('link[rel="icon"]');
        if (!favicon) {
            favicon = document.createElement('link');
            favicon.rel = 'icon';
            document.head.appendChild(favicon);
        }
        favicon.href = this.getContextualIcon('favicon');
    }

    setupDynamicIcons() {
        // Auto-replace generic logos with Toolora branding
        const genericLogos = document.querySelectorAll('img[alt*="logo"], img[alt*="Logo"], .logo');
        genericLogos.forEach(logo => {
            if (logo.alt.toLowerCase().includes('toolora')) {
                const context = this.detectContext(logo);
                this.updateIcon(logo, context);
            }
        });
    }

    detectContext(element) {
        const classList = Array.from(element.classList);
        const parent = element.closest('.navbar, .hero, .footer, .card, .badge');

        if (parent) {
            if (parent.classList.contains('navbar')) return 'navbar';
            if (parent.classList.contains('hero')) return 'hero';
            if (parent.classList.contains('footer')) return 'footer';
            if (parent.classList.contains('card')) return 'card';
            if (parent.classList.contains('badge')) return 'badge';
        }

        // Default based on size
        const width = element.width || element.offsetWidth;
        if (width <= 24) return 'favicon';
        if (width <= 32) return 'navbar';
        if (width <= 48) return 'card';
        return 'hero';
    }

    setupThemeAdaptation() {
        // Adapt icons based on theme
        const observer = new MutationObserver(() => {
            const isDark = document.documentElement.classList.contains('dark') || 
                          document.body.classList.contains('dark-theme');
            this.adaptToTheme(isDark);
            this.updateSVGLogos(isDark);
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        });

        // Initial setup
        const isDark = document.documentElement.classList.contains('dark');
        this.updateSVGLogos(isDark);
    }

    adaptToTheme(isDark) {
        // Theme adaptation logic
        const icons = document.querySelectorAll('[data-lucide]');
        icons.forEach(icon => {
            if (isDark) {
                if (icon && icon.style) {
                    icon.style.color = '#ffffff';
                }
            } else {
                if (icon && icon.style) {
                    icon.style.color = '#000000';
                }
            }
        });
    }

    updateSVGLogos(isDark) {
        // Update SVG logos for dark mode
        const svgLogos = document.querySelectorAll('svg.professional-logo, svg[class*="toolora"]');
        svgLogos.forEach(svg => {
            const lightElements = svg.querySelectorAll('.light-mode');
            const darkElements = svg.querySelectorAll('.dark-mode');

            if (isDark) {
                lightElements.forEach(el => el.style.display = 'none');
                darkElements.forEach(el => el.style.display = 'block');
            } else {
                lightElements.forEach(el => el.style.display = 'block');
                darkElements.forEach(el => el.style.display = 'none');
            }
        });

        // Update text elements in SVG
        const svgTexts = document.querySelectorAll('svg text.logo-text');
        svgTexts.forEach(text => {
            if (isDark) {
                text.setAttribute('fill', '#ffffff');
                text.style.textShadow = '0 1px 2px rgba(0,0,0,0.5)';
            } else {
                text.setAttribute('fill', '#1f2937');
                text.style.textShadow = '0 1px 2px rgba(0,0,0,0.1)';
            }
        });
    }

    setupContextualIcons() {
        // Auto-setup icons when new content is loaded
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) { // Element node
                            const logos = node.querySelectorAll?.('img[alt*="toolora"], img[alt*="Toolora"], .toolora-logo');
                            logos?.forEach(logo => {
                                const context = this.detectContext(logo);
                                this.updateIcon(logo, context);
                            });
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Export icon for download
    exportIcon(variant, format = 'svg') {
        const iconUrl = this.iconVariants[variant];
        if (!iconUrl) return;

        const link = document.createElement('a');
        link.href = iconUrl;
        link.download = `toolora-${variant}.${format}`;
        link.click();
    }

    // Generate all icon sizes for app store
    generateAppIcons() {
        const appSizes = [16, 24, 32, 48, 64, 128, 256, 512, 1024];
        const icons = {};

        appSizes.forEach(size => {
            const closest = this.getClosestSize(size);
            icons[`${size}x${size}`] = this.iconVariants[closest];
        });

        return icons;
    }

    getClosestSize(targetSize) {
        const sizes = {
            16: 'toolora-16',
            24: 'toolora-24', 
            32: 'toolora-32',
            48: 'toolora-48',
            64: 'toolora-64'
        };

        const availableSizes = Object.keys(sizes).map(Number);
        const closest = availableSizes.reduce((prev, curr) => 
            Math.abs(curr - targetSize) < Math.abs(prev - targetSize) ? curr : prev
        );

        return sizes[closest];
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Icon Manager
    if (!window.iconManager) {
        window.iconManager = new IconManager();
        window.iconManager.updateAllIcons();
    }
});

// Export for global use
window.IconManager = IconManager;