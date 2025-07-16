// Authentication event handlers for login and register forms
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showMessage('Please fill in all fields', 'error');
                return;
            }
            
            // Use Firebase authentication if available
            if (window.signInWithEmail) {
                window.signInWithEmail(email, password);
            } else {
                showMessage('Authentication system is loading...', 'info');
            }
        });
    }
    
    // Handle register form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            if (!email || !password || !confirmPassword) {
                showMessage('Please fill in all fields', 'error');
                return;
            }
            
            if (password !== confirmPassword) {
                showMessage('Passwords do not match', 'error');
                return;
            }
            
            if (password.length < 6) {
                showMessage('Password must be at least 6 characters long', 'error');
                return;
            }
            
            // Use Firebase authentication if available
            if (window.signUpWithEmail) {
                window.signUpWithEmail(email, password);
            } else {
                showMessage('Authentication system is loading...', 'info');
            }
        });
    }
    
    // Handle Google sign-in
    const googleSignInBtn = document.getElementById('google-signin');
    if (googleSignInBtn) {
        googleSignInBtn.addEventListener('click', function() {
            if (window.signInWithGoogle) {
                window.signInWithGoogle();
            } else {
                showMessage('Google sign-in is loading...', 'info');
            }
        });
    }
    
    // Utility function to show messages
    function showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type} mb-4 animate__animated animate__fadeInDown`;
        messageDiv.innerHTML = `
            <div class="flex items-center">
                <i data-lucide="${type === 'error' ? 'alert-circle' : type === 'success' ? 'check-circle' : 'info'}" class="w-5 h-5 mr-3"></i>
                <span>${message}</span>
            </div>
        `;
        
        const form = document.querySelector('.auth-form');
        if (form) {
            // Remove existing messages
            const existingMessages = form.querySelectorAll('.alert');
            existingMessages.forEach(msg => msg.remove());
            
            form.insertBefore(messageDiv, form.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                messageDiv.remove();
            }, 5000);
            
            // Refresh icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }
});