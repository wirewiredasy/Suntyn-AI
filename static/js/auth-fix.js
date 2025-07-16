// Enhanced authentication with proper error handling
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Firebase configuration check
    function checkFirebaseConfig() {
        const apiKey = document.querySelector('meta[name="firebase-api-key"]')?.content;
        const projectId = document.querySelector('meta[name="firebase-project-id"]')?.content;
        const appId = document.querySelector('meta[name="firebase-app-id"]')?.content;
        
        if (!apiKey || !projectId || !appId) {
            console.warn('Firebase configuration missing');
            return false;
        }
        
        return { apiKey, projectId, appId };
    }
    
    // Initialize Firebase if config is available
    const firebaseConfig = checkFirebaseConfig();
    
    if (firebaseConfig && typeof firebase !== 'undefined') {
        try {
            firebase.initializeApp({
                apiKey: firebaseConfig.apiKey,
                authDomain: `${firebaseConfig.projectId}.firebaseapp.com`,
                projectId: firebaseConfig.projectId,
                appId: firebaseConfig.appId
            });
            
            const auth = firebase.auth();
            
            // Google Sign In
            window.signInWithGoogle = function() {
                const provider = new firebase.auth.GoogleAuthProvider();
                auth.signInWithPopup(provider)
                    .then(handleAuthSuccess)
                    .catch(handleAuthError);
            };
            
            // Email/Password Sign In
            window.signInWithEmail = function(email, password) {
                auth.signInWithEmailAndPassword(email, password)
                    .then(handleAuthSuccess)
                    .catch(handleAuthError);
            };
            
            // Email/Password Sign Up
            window.signUpWithEmail = function(email, password) {
                auth.createUserWithEmailAndPassword(email, password)
                    .then(handleAuthSuccess)
                    .catch(handleAuthError);
            };
            
            // Handle successful authentication
            function handleAuthSuccess(result) {
                const user = result.user;
                user.getIdToken().then(idToken => {
                    fetch('/auth/verify-token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            idToken: idToken,
                            userInfo: {
                                uid: user.uid,
                                email: user.email,
                                displayName: user.displayName,
                                photoURL: user.photoURL
                            }
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            window.location.href = '/dashboard';
                        } else {
                            showAuthError(data.error || 'Authentication failed');
                        }
                    })
                    .catch(error => {
                        showAuthError('Network error: ' + error.message);
                    });
                });
            }
            
            // Handle authentication errors
            function handleAuthError(error) {
                let message = 'Authentication failed';
                switch (error.code) {
                    case 'auth/user-not-found':
                        message = 'No account found with this email';
                        break;
                    case 'auth/wrong-password':
                        message = 'Incorrect password';
                        break;
                    case 'auth/email-already-in-use':
                        message = 'Email already registered';
                        break;
                    case 'auth/weak-password':
                        message = 'Password is too weak';
                        break;
                    case 'auth/invalid-email':
                        message = 'Invalid email address';
                        break;
                    default:
                        message = error.message || 'Authentication failed';
                }
                showAuthError(message);
            }
            
            // Show authentication error
            function showAuthError(message) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-error mb-4 animate__animated animate__shakeX';
                errorDiv.innerHTML = `
                    <div class="flex items-center">
                        <i data-lucide="alert-circle" class="w-5 h-5 mr-3"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                const form = document.querySelector('.auth-form');
                if (form) {
                    form.insertBefore(errorDiv, form.firstChild);
                    setTimeout(() => errorDiv.remove(), 5000);
                    
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
            }
            
            console.log('Firebase authentication initialized');
            
        } catch (error) {
            console.error('Firebase initialization error:', error);
        }
    } else {
        console.warn('Firebase not available or configuration missing');
        
        // Fallback authentication message
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(form => {
            const notice = document.createElement('div');
            notice.className = 'alert alert-info mb-4';
            notice.innerHTML = `
                <div class="flex items-center">
                    <i data-lucide="info" class="w-5 h-5 mr-3"></i>
                    <span>Authentication is being configured. Please try again shortly.</span>
                </div>
            `;
            form.insertBefore(notice, form.firstChild);
        });
    }
    
    // Handle logout
    window.signOut = function() {
        if (firebase && firebase.auth) {
            firebase.auth().signOut().then(() => {
                fetch('/auth/logout', { method: 'POST' })
                    .then(() => {
                        window.location.href = '/';
                    });
            });
        } else {
            fetch('/auth/logout', { method: 'POST' })
                .then(() => {
                    window.location.href = '/';
                });
        }
    };
});