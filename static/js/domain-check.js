// Domain detection and Firebase authorization helper
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Get current domain
    const currentDomain = window.location.hostname;
    const isReplit = currentDomain.includes('replit.dev') || currentDomain.includes('replit.app');
    
    console.log('Current domain:', currentDomain);
    
    // Check if Firebase authentication fails due to domain authorization
    window.addEventListener('unhandledrejection', function(event) {
        if (event.reason && event.reason.code === 'auth/unauthorized-domain') {
            showDomainError(currentDomain);
        }
    });
    
    function showDomainError(domain) {
        const errorHTML = `
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                <div class="flex items-start">
                    <i data-lucide="alert-triangle" class="w-5 h-5 text-yellow-600 mt-0.5 mr-3"></i>
                    <div>
                        <h3 class="text-yellow-800 font-medium mb-2">Firebase Domain Authorization Required</h3>
                        <p class="text-yellow-700 text-sm mb-3">
                            Current domain <code class="bg-yellow-100 px-1 rounded">${domain}</code> needs to be authorized in Firebase.
                        </p>
                        <div class="text-yellow-700 text-sm">
                            <p class="font-medium mb-1">Quick Fix Steps:</p>
                            <ol class="list-decimal list-inside space-y-1 text-xs">
                                <li>Go to <a href="https://console.firebase.google.com" target="_blank" class="underline">Firebase Console</a></li>
                                <li>Select your project: <strong>tooloraai-eccee</strong></li>
                                <li>Go to Authentication → Settings → Authorized domains</li>
                                <li>Click "Add domain" and add: <code class="bg-yellow-100 px-1 rounded">${domain}</code></li>
                                <li>Save and refresh this page</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(form => {
            form.insertAdjacentHTML('beforebegin', errorHTML);
        });
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    // Test Firebase connection
    setTimeout(() => {
        const apiKey = document.querySelector('meta[name="firebase-api-key"]')?.content;
        if (apiKey && apiKey !== '') {
            console.log('Firebase API key found, testing connection...');
            
            // Show current domain info to user
            if (isReplit) {
                const infoDiv = document.createElement('div');
                infoDiv.className = 'bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4 text-sm';
                infoDiv.innerHTML = `
                    <div class="flex items-center">
                        <i data-lucide="info" class="w-4 h-4 text-blue-600 mr-2"></i>
                        <span class="text-blue-700">
                            Authentication domain: <code class="bg-blue-100 px-1 rounded">${currentDomain}</code>
                        </span>
                    </div>
                `;
                
                const firstForm = document.querySelector('.auth-form');
                if (firstForm) {
                    firstForm.parentNode.insertBefore(infoDiv, firstForm);
                    
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
            }
        }
    }, 1000);
});