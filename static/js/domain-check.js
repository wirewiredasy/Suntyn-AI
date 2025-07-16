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
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4">
                <div class="flex items-start">
                    <i data-lucide="alert-triangle" class="w-5 h-5 text-orange-600 mt-0.5 mr-3"></i>
                    <div>
                        <h3 class="text-orange-800 font-medium mb-2">🔥 Firebase Domain Authorization Needed</h3>
                        <p class="text-orange-700 text-sm mb-3">
                            <strong>Current Domain:</strong> <code class="bg-orange-100 px-1 rounded font-mono text-xs">${domain}</code>
                        </p>
                        <div class="text-orange-700 text-sm">
                            <p class="font-medium mb-2">तुरंत Fix करें (5 मिनट में):</p></div>
                            <ol class="list-decimal list-inside space-y-1 text-xs">
                                <li><a href="https://console.firebase.google.com" target="_blank" class="underline text-blue-600">Firebase Console खोलें</a></li>
                                <li>Project select करें: <strong>tooloraai-eccee</strong></li>
                                <li><strong>Authentication</strong> → <strong>Settings</strong> → <strong>Authorized domains</strong></li>
                                <li><strong>"Add domain"</strong> पर click करें</li>
                                <li>Add करें: <code class="bg-orange-100 px-1 rounded font-mono">${domain}</code></li>
                                <li><strong>Save</strong> करें और 2-3 मिनट wait करें</li>
                                <li>Page refresh करें</li>
                            </ol>
                            <div class="mt-3 p-2 bg-green-50 rounded text-green-700">
                                <strong>✅ Fix होने के बाद:</strong> Normal login/signup काम करेगा
                            </div>
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