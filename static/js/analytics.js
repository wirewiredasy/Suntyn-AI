
class TooloraAnalytics {
    constructor() {
        this.userId = this.generateUserId();
        this.sessionId = this.generateSessionId();
        this.initializeTracking();
    }

    generateUserId() {
        let userId = localStorage.getItem('toolora_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('toolora_user_id', userId);
        }
        return userId;
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    initializeTracking() {
        // Track page views
        this.trackPageView();
        
        // Track tool usage
        this.trackToolUsage();
        
        // Track user engagement
        this.trackEngagement();
        
        // Track performance metrics
        this.trackPerformance();
    }

    trackPageView() {
        const pageData = {
            page: window.location.pathname,
            title: document.title,
            referrer: document.referrer,
            timestamp: new Date().toISOString(),
            userId: this.userId,
            sessionId: this.sessionId
        };
        
        this.sendEvent('page_view', pageData);
    }

    trackToolUsage() {
        document.addEventListener('click', (e) => {
            const toolButton = e.target.closest('.use-tool-btn, .tool-card a');
            if (toolButton) {
                const toolName = this.extractToolName(toolButton);
                this.sendEvent('tool_click', {
                    tool: toolName,
                    userId: this.userId,
                    sessionId: this.sessionId,
                    timestamp: new Date().toISOString()
                });
            }
        });
    }

    trackEngagement() {
        let startTime = Date.now();
        let isActive = true;

        // Track time on page
        window.addEventListener('beforeunload', () => {
            const timeSpent = Date.now() - startTime;
            this.sendEvent('engagement', {
                timeSpent: timeSpent,
                page: window.location.pathname,
                userId: this.userId,
                sessionId: this.sessionId
            });
        });

        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
            maxScroll = Math.max(maxScroll, scrollPercent);
        });

        window.addEventListener('beforeunload', () => {
            this.sendEvent('scroll_depth', {
                maxScroll: maxScroll,
                page: window.location.pathname,
                userId: this.userId
            });
        });
    }

    trackPerformance() {
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            this.sendEvent('performance', {
                loadTime: perfData.loadEventEnd - perfData.fetchStart,
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
                page: window.location.pathname,
                userId: this.userId
            });
        });
    }

    extractToolName(element) {
        const href = element.getAttribute('href');
        if (href) {
            const match = href.match(/\/tools\/([^\/]+)/);
            return match ? match[1] : 'unknown';
        }
        return 'unknown';
    }

    sendEvent(eventType, data) {
        // In production, send to your analytics endpoint
        console.log('Analytics Event:', eventType, data);
        
        // Store locally for now
        const events = JSON.parse(localStorage.getItem('toolora_events') || '[]');
        events.push({
            type: eventType,
            data: data,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 100 events
        if (events.length > 100) {
            events.splice(0, events.length - 100);
        }
        
        localStorage.setItem('toolora_events', JSON.stringify(events));
    }
}

// Initialize analytics
const tooloraAnalytics = new TooloraAnalytics();
window.tooloraAnalytics = tooloraAnalytics;
