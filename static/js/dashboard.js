/**
 * Professional Dashboard Integration with Real User Data
 */

function dashboard() {
    return {
        // Real-time stats
        stats: {
            toolsUsed: 0,
            filesProcessed: 0,
            dataSaved: '0 MB',
            timeSaved: '0 hours'
        },
        
        // Activity history
        history: [],
        
        // Quick tools
        quickTools: [],
        
        // Loading states
        loading: true,
        error: null,
        
        // User data
        currentUser: null,
        
        // Initialize dashboard
        async init() {
            console.log('🚀 Initializing Professional Dashboard');
            
            // Wait for Firebase auth
            await this.waitForAuth();
            
            // Load dashboard data
            await this.loadDashboardData();
            
            // Set up real-time updates
            this.setupRealTimeUpdates();
            
            this.loading = false;
        },
        
        // Wait for Firebase authentication
        async waitForAuth() {
            return new Promise((resolve) => {
                if (typeof firebase !== 'undefined' && firebase.auth) {
                    firebase.auth().onAuthStateChanged((user) => {
                        this.currentUser = user;
                        resolve();
                    });
                } else {
                    // Demo mode - no authentication
                    this.currentUser = null;
                    resolve();
                }
            });
        },
        
        // Load real dashboard data
        async loadDashboardData() {
            try {
                const userId = this.currentUser ? this.currentUser.uid : null;
                const response = await fetch(`/api/dashboard/stats?user_id=${userId || ''}`);
                const data = await response.json();
                
                // Update stats with real data
                this.stats = {
                    toolsUsed: data.tools_used,
                    filesProcessed: data.files_processed,
                    dataSaved: data.data_saved,
                    timeSaved: data.time_saved
                };
                
                // Update history with real activity
                this.history = data.recent_activity || [];
                
                // Update quick tools
                this.quickTools = data.quick_tools || [];
                
                console.log('✅ Dashboard data loaded:', data);
                
            } catch (error) {
                console.error('❌ Error loading dashboard data:', error);
                this.error = 'Failed to load dashboard data';
                
                // Fallback to demo data
                this.loadDemoData();
            }
        },
        
        // Load demo data when no user or error
        loadDemoData() {
            this.stats = {
                toolsUsed: 0,
                filesProcessed: 0,
                dataSaved: '0 MB',
                timeSaved: '0 hours'
            };
            
            this.history = [];
            
            this.quickTools = [
                { name: 'pdf-merge', category: 'pdf', display_name: 'PDF Merge' },
                { name: 'image-compress', category: 'image', display_name: 'Image Compress' },
                { name: 'video-to-mp3', category: 'video', display_name: 'Video To MP3' },
                { name: 'resume-generator', category: 'ai', display_name: 'Resume Generator' },
                { name: 'qr-generator', category: 'utility', display_name: 'QR Generator' },
                { name: 'text-case-converter', category: 'utility', display_name: 'Text Case Converter' }
            ];
        },
        
        // Set up real-time updates
        setupRealTimeUpdates() {
            // Refresh data every 30 seconds if user is logged in
            if (this.currentUser) {
                setInterval(() => {
                    this.loadDashboardData();
                }, 30000);
            }
        },
        
        // Format time ago
        formatTimeAgo(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const diffInMinutes = Math.floor((now - date) / (1000 * 60));
            
            if (diffInMinutes < 1) return 'Just now';
            if (diffInMinutes < 60) return `${diffInMinutes} min ago`;
            
            const diffInHours = Math.floor(diffInMinutes / 60);
            if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
            
            const diffInDays = Math.floor(diffInHours / 24);
            if (diffInDays < 7) return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
            
            return date.toLocaleDateString();
        },
        
        // Navigate to tool
        openTool(toolName) {
            window.location.href = `/tools/${toolName}`;
        },
        
        // Track tool usage (called when user uses a tool)
        async trackToolUsage(toolName, category, fileCount = 1, fileSize = 0) {
            if (!this.currentUser) return;
            
            try {
                await fetch('/api/dashboard/track', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: this.currentUser.uid,
                        tool_name: toolName,
                        tool_category: category,
                        file_count: fileCount,
                        file_size_mb: fileSize
                    })
                });
                
                // Refresh dashboard data
                await this.loadDashboardData();
                
            } catch (error) {
                console.error('Error tracking tool usage:', error);
            }
        },
        
        // Get category icon
        getCategoryIcon(category) {
            const icons = {
                'pdf': 'file-text',
                'image': 'image',
                'video': 'video',
                'ai': 'brain',
                'utility': 'settings',
                'govt': 'shield',
                'student': 'graduation-cap',
                'finance': 'calculator'
            };
            return icons[category] || 'tool';
        },
        
        // Get category color
        getCategoryColor(category) {
            const colors = {
                'pdf': 'red',
                'image': 'green',
                'video': 'purple',
                'ai': 'violet',
                'utility': 'slate',
                'govt': 'orange',
                'student': 'blue',
                'finance': 'emerald'
            };
            return colors[category] || 'gray';
        }
    };
}

// Global function to track tool usage from any page
window.trackToolUsage = async function(toolName, category, fileCount = 1, fileSize = 0) {
    // If dashboard is loaded, use its method
    if (window.dashboardApp && window.dashboardApp.trackToolUsage) {
        return window.dashboardApp.trackToolUsage(toolName, category, fileCount, fileSize);
    }
    
    // Otherwise, make direct API call
    try {
        if (typeof firebase !== 'undefined' && firebase.auth && firebase.auth().currentUser) {
            const user = firebase.auth().currentUser;
            await fetch('/api/dashboard/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: user.uid,
                    tool_name: toolName,
                    tool_category: category,
                    file_count: fileCount,
                    file_size_mb: fileSize
                })
            });
        }
    } catch (error) {
        console.error('Error tracking tool usage:', error);
    }
};

// Make dashboard function globally available
window.dashboard = dashboard;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/dashboard') {
        console.log('📊 Professional Dashboard Loading...');
        
        // Initialize dashboard if Alpine.js is available
        if (typeof Alpine !== 'undefined') {
            console.log('✅ Alpine.js found, dashboard ready');
        }
    }
});