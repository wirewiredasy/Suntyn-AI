// Theme management system
class ThemeManager {
    constructor() {
        this.currentTheme = 'light';
        this.systemTheme = 'light';
        this.userPreference = 'system';
        this.listeners = [];
        
        this.init();
    }

    init() {
        // Load saved theme preference
        this.loadThemePreference();
        
        // Listen for system theme changes
        this.setupSystemThemeListener();
        
        // Apply initial theme
        this.applyTheme();
        
        // Setup theme toggle handlers
        this.setupThemeToggles();
    }

    loadThemePreference() {
        const saved = localStorage.getItem('theme-preference');
        if (saved) {
            this.userPreference = saved;
        }
        
        // Get system theme
        if (window.matchMedia) {
            this.systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        
        // Determine current theme
        if (this.userPreference === 'system') {
            this.currentTheme = this.systemTheme;
        } else {
            this.currentTheme = this.userPreference;
        }
    }

    setupSystemThemeListener() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                this.systemTheme = e.matches ? 'dark' : 'light';
                
                if (this.userPreference === 'system') {
                    this.currentTheme = this.systemTheme;
                    this.applyTheme();
                }
            });
        }
    }

    setupThemeToggles() {
        // Find all theme toggle buttons
        const toggles = document.querySelectorAll('[data-theme-toggle]');
        
        toggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        });
        
        // Find theme selector dropdowns
        const selectors = document.querySelectorAll('[data-theme-selector]');
        
        selectors.forEach(selector => {
            selector.addEventListener('change', (e) => {
                this.setTheme(e.target.value);
            });
            
            // Set initial value
            selector.value = this.userPreference;
        });
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        this.userPreference = theme;
        
        if (theme === 'system') {
            this.currentTheme = this.systemTheme;
        } else {
            this.currentTheme = theme;
        }
        
        this.saveThemePreference();
        this.applyTheme();
        this.notifyListeners();
    }

    applyTheme() {
        const html = document.documentElement;
        const body = document.body;
        
        // Remove existing theme classes
        html.classList.remove('light', 'dark');
        body.classList.remove('light', 'dark');
        
        // Add current theme class
        html.classList.add(this.currentTheme);
        body.classList.add(this.currentTheme);
        
        // Update meta theme-color
        this.updateMetaThemeColor();
        
        // Update theme toggle icons
        this.updateThemeToggleIcons();
        
        // Update theme selector values
        this.updateThemeSelectors();
        
        // Apply theme-specific styles
        this.applyThemeStyles();
    }

    updateMetaThemeColor() {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        const colors = {
            light: '#ffffff',
            dark: '#1f2937'
        };
        
        metaThemeColor.content = colors[this.currentTheme];
    }

    updateThemeToggleIcons() {
        const toggles = document.querySelectorAll('[data-theme-toggle]');
        
        toggles.forEach(toggle => {
            const lightIcon = toggle.querySelector('[data-theme-icon="light"]');
            const darkIcon = toggle.querySelector('[data-theme-icon="dark"]');
            
            if (lightIcon && darkIcon) {
                if (this.currentTheme === 'dark') {
                    lightIcon.style.display = 'block';
                    darkIcon.style.display = 'none';
                } else {
                    lightIcon.style.display = 'none';
                    darkIcon.style.display = 'block';
                }
            }
        });
    }

    updateThemeSelectors() {
        const selectors = document.querySelectorAll('[data-theme-selector]');
        
        selectors.forEach(selector => {
            selector.value = this.userPreference;
        });
    }

    applyThemeStyles() {
        // Apply custom CSS variables based on theme
        const root = document.documentElement;
        
        if (this.currentTheme === 'dark') {
            root.style.setProperty('--theme-bg', '#1f2937');
            root.style.setProperty('--theme-text', '#ffffff');
            root.style.setProperty('--theme-border', '#374151');
            root.style.setProperty('--theme-hover', '#374151');
        } else {
            root.style.setProperty('--theme-bg', '#ffffff');
            root.style.setProperty('--theme-text', '#1f2937');
            root.style.setProperty('--theme-border', '#e5e7eb');
            root.style.setProperty('--theme-hover', '#f9fafb');
        }
    }

    saveThemePreference() {
        localStorage.setItem('theme-preference', this.userPreference);
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    getUserPreference() {
        return this.userPreference;
    }

    getSystemTheme() {
        return this.systemTheme;
    }

    onThemeChange(callback) {
        this.listeners.push(callback);
    }

    offThemeChange(callback) {
        this.listeners = this.listeners.filter(listener => listener !== callback);
    }

    notifyListeners() {
        this.listeners.forEach(listener => {
            listener(this.currentTheme, this.userPreference);
        });
    }

    // Theme animation utilities
    enableThemeTransition() {
        const transitionStyle = document.createElement('style');
        transitionStyle.textContent = `
            * {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
            }
        `;
        document.head.appendChild(transitionStyle);
        
        setTimeout(() => {
            document.head.removeChild(transitionStyle);
        }, 300);
    }

    // Color scheme utilities
    getThemeColors() {
        const colors = {
            light: {
                primary: '#3b82f6',
                secondary: '#6b7280',
                background: '#ffffff',
                surface: '#f9fafb',
                text: '#1f2937',
                textSecondary: '#6b7280',
                border: '#e5e7eb',
                hover: '#f3f4f6',
                success: '#10b981',
                warning: '#f59e0b',
                error: '#ef4444',
                info: '#3b82f6'
            },
            dark: {
                primary: '#60a5fa',
                secondary: '#9ca3af',
                background: '#1f2937',
                surface: '#374151',
                text: '#ffffff',
                textSecondary: '#d1d5db',
                border: '#4b5563',
                hover: '#4b5563',
                success: '#34d399',
                warning: '#fbbf24',
                error: '#f87171',
                info: '#60a5fa'
            }
        };
        
        return colors[this.currentTheme];
    }

    // Accessibility utilities
    getContrastRatio(color1, color2) {
        const getLuminance = (color) => {
            const rgb = this.hexToRgb(color);
            const rsRGB = rgb.r / 255;
            const gsRGB = rgb.g / 255;
            const bsRGB = rgb.b / 255;
            
            const r = rsRGB <= 0.03928 ? rsRGB / 12.92 : Math.pow((rsRGB + 0.055) / 1.055, 2.4);
            const g = gsRGB <= 0.03928 ? gsRGB / 12.92 : Math.pow((gsRGB + 0.055) / 1.055, 2.4);
            const b = bsRGB <= 0.03928 ? bsRGB / 12.92 : Math.pow((bsRGB + 0.055) / 1.055, 2.4);
            
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        };
        
        const lum1 = getLuminance(color1);
        const lum2 = getLuminance(color2);
        
        const brightest = Math.max(lum1, lum2);
        const darkest = Math.min(lum1, lum2);
        
        return (brightest + 0.05) / (darkest + 0.05);
    }

    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    // Theme persistence across sessions
    syncThemeAcrossWindows() {
        window.addEventListener('storage', (e) => {
            if (e.key === 'theme-preference') {
                this.userPreference = e.newValue;
                this.loadThemePreference();
                this.applyTheme();
                this.notifyListeners();
            }
        });
    }

    // Theme analytics
    trackThemeUsage() {
        // Track theme preference changes
        this.onThemeChange((theme, preference) => {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'theme_change', {
                    theme: theme,
                    preference: preference
                });
            }
        });
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// Enable theme transitions
themeManager.enableThemeTransition();

// Sync theme across windows
themeManager.syncThemeAcrossWindows();

// Track theme usage
themeManager.trackThemeUsage();

// Export for global use
window.themeManager = themeManager;

// Auto-detect theme preference on first visit
document.addEventListener('DOMContentLoaded', () => {
    const firstVisit = !localStorage.getItem('theme-preference');
    
    if (firstVisit) {
        // Set theme based on system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            themeManager.setTheme('dark');
        } else {
            themeManager.setTheme('light');
        }
    }
});

// Handle theme-specific code splitting
if (themeManager.getCurrentTheme() === 'dark') {
    // Load dark theme specific resources
    const darkStyles = document.createElement('link');
    darkStyles.rel = 'stylesheet';
    darkStyles.href = '/static/css/dark-theme.css';
    document.head.appendChild(darkStyles);
}

// Theme-aware image loading
function loadThemeAwareImage(lightSrc, darkSrc, element) {
    const currentTheme = themeManager.getCurrentTheme();
    element.src = currentTheme === 'dark' ? darkSrc : lightSrc;
    
    themeManager.onThemeChange((theme) => {
        element.src = theme === 'dark' ? darkSrc : lightSrc;
    });
}

// Theme-aware animation preferences
function respectsReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// High contrast mode detection
function detectHighContrastMode() {
    return window.matchMedia('(prefers-contrast: high)').matches;
}

// Export utilities
window.themeUtils = {
    loadThemeAwareImage,
    respectsReducedMotion,
    detectHighContrastMode
};
