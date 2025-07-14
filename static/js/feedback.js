// Feedback Widget Functionality
document.addEventListener('DOMContentLoaded', function() {
    const feedbackForm = document.getElementById('feedback-form');
    
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(feedbackForm);
            const feedbackData = {
                type: formData.get('type'),
                message: formData.get('message'),
                url: window.location.href,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent
            };
            
            // Send feedback to backend
            fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(feedbackData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showNotification('Thank you for your feedback! 🙏', 'success');
                    feedbackForm.reset();
                    
                    // Close modal
                    const modal = document.querySelector('[x-data]');
                    if (modal && modal.__x) {
                        modal.__x.$data.open = false;
                    }
                } else {
                    showNotification('Error sending feedback. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error sending feedback. Please try again.', 'error');
            });
        });
    }
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animation
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Enhanced tool card animations
document.addEventListener('DOMContentLoaded', function() {
    const toolCards = document.querySelectorAll('.tool-card');
    
    // Add stagger animation to tool cards
    toolCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-fade-in-up');
    });
    
    // Enhanced hover effects
    toolCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Recently used tools functionality
class RecentlyUsedTools {
    constructor() {
        this.key = 'toolora_recent_tools';
        this.maxItems = 6;
    }
    
    add(toolName, toolCategory) {
        let recent = this.get();
        
        // Remove if already exists
        recent = recent.filter(item => item.tool !== toolName);
        
        // Add to beginning
        recent.unshift({
            tool: toolName,
            category: toolCategory,
            timestamp: Date.now()
        });
        
        // Keep only max items
        recent = recent.slice(0, this.maxItems);
        
        localStorage.setItem(this.key, JSON.stringify(recent));
        this.updateUI();
    }
    
    get() {
        try {
            return JSON.parse(localStorage.getItem(this.key)) || [];
        } catch {
            return [];
        }
    }
    
    updateUI() {
        const recentContainer = document.getElementById('recent-tools');
        if (!recentContainer) return;
        
        const recent = this.get();
        if (recent.length === 0) {
            recentContainer.style.display = 'none';
            return;
        }
        
        recentContainer.style.display = 'block';
        const list = recentContainer.querySelector('.recent-tools-list');
        
        if (list) {
            list.innerHTML = recent.map(item => `
                <a href="/tools/${item.tool}" class="recent-tool-item">
                    <div class="tool-icon">
                        <i data-lucide="${this.getToolIcon(item.category)}"></i>
                    </div>
                    <span>${item.tool.replace('-', ' ')}</span>
                </a>
            `).join('');
        }
    }
    
    getToolIcon(category) {
        const icons = {
            'pdf': 'file-text',
            'image': 'image',
            'video': 'video',
            'ai': 'brain',
            'govt': 'shield',
            'student': 'graduation-cap',
            'finance': 'calculator',
            'utility': 'settings'
        };
        return icons[category] || 'tool';
    }
}

// Initialize recently used tools
const recentlyUsedTools = new RecentlyUsedTools();

// Track tool usage
function trackToolUsage(toolName, toolCategory) {
    recentlyUsedTools.add(toolName, toolCategory);
    
    // Send analytics
    fetch('/api/analytics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'tool_click',
            tool: toolName,
            category: toolCategory,
            timestamp: Date.now()
        })
    }).catch(error => console.error('Analytics error:', error));
}

// "Surprise Me" functionality
function surpriseMe() {
    const allTools = [];
    
    // Collect all tools from config
    if (window.toolsConfig) {
        Object.entries(window.toolsConfig).forEach(([category, data]) => {
            data.tools.forEach(tool => {
                allTools.push({ tool, category });
            });
        });
    }
    
    if (allTools.length > 0) {
        const randomTool = allTools[Math.floor(Math.random() * allTools.length)];
        window.location.href = `/tools/${randomTool.tool}`;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // "/" for search
    if (e.key === '/' && !e.target.matches('input, textarea')) {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('[x-data]');
        modals.forEach(modal => {
            if (modal.__x && modal.__x.$data.open) {
                modal.__x.$data.open = false;
            }
        });
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    recentlyUsedTools.updateUI();
});