// Temporary authentication fallback while Firebase domain is being configured
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Check if we're in demo mode (Firebase not configured)
    let isDemoMode = false;
    
    // Override auth functions temporarily
    setTimeout(() => {
        // Check if Firebase auth is failing
        const checkAuthStatus = () => {
            if (!window.firebaseAuth || window.location.hostname.includes('replit.dev')) {
                isDemoMode = true;
                setupDemoAuth();
            }
        };
        
        checkAuthStatus();
        
        // Listen for auth errors
        window.addEventListener('error', function(e) {
            if (e.message && (e.message.includes('auth/unauthorized-domain') || e.message.includes('Firebase'))) {
                isDemoMode = true;
                setupDemoAuth();
            }
        });
    }, 2000);
    
    function setupDemoAuth() {
        console.log('Setting up demo authentication mode');
        
        // Show demo mode notice
        const demoNotice = document.createElement('div');
        demoNotice.className = 'bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4';
        demoNotice.innerHTML = `
            <div class="flex items-center">
                <i data-lucide="settings" class="w-5 h-5 text-orange-600 mr-3"></i>
                <div>
                    <h3 class="text-orange-800 font-medium">Demo Authentication Mode</h3>
                    <p class="text-orange-700 text-sm mt-1">
                        Firebase domain authorization pending. Use demo login below.
                    </p>
                </div>
            </div>
        `;
        
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(form => {
            form.parentNode.insertBefore(demoNotice, form);
        });
        
        // Add demo login button
        const demoLoginBtn = document.createElement('button');
        demoLoginBtn.type = 'button';
        demoLoginBtn.className = 'w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 mb-4';
        demoLoginBtn.innerHTML = `
            <i data-lucide="play-circle" class="w-5 h-5 mr-2 inline"></i>
            Demo Login (Skip Authentication)
        `;
        
        demoLoginBtn.addEventListener('click', function() {
            // Create demo session
            fetch('/auth/verify-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userInfo: {
                        uid: 'demo-user-' + Date.now(),
                        email: 'demo@toolora.ai',
                        displayName: 'Demo User',
                        photoURL: null
                    }
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    // Simple redirect for demo
                    window.location.href = '/dashboard';
                }
            })
            .catch(error => {
                // Even if API fails, redirect to dashboard for demo
                window.location.href = '/dashboard';
            });
        });
        
        // Insert demo button before regular forms
        authForms.forEach(form => {
            form.parentNode.insertBefore(demoLoginBtn.cloneNode(true), form);
            // Add event listener to the new button
            const newBtn = form.parentNode.querySelector('button');
            if (newBtn && newBtn.innerHTML.includes('Demo Login')) {
                newBtn.addEventListener('click', demoLoginBtn.onclick);
            }
        });
        
        // Refresh icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
});