// Firebase Authentication Handler
class FirebaseAuthHandler {
    constructor() {
        this.auth = null;
        this.currentUser = null;
        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) return;
        
        try {
            // Wait for Firebase to be loaded
            await this.waitForFirebase();
            
            this.auth = window.firebaseAuth;
            
            // Set up auth state observer
            this.auth.onAuthStateChanged((user) => {
                this.currentUser = user;
                this.onAuthStateChanged(user);
            });
            
            this.initialized = true;
            console.log('Firebase Auth initialized');
        } catch (error) {
            console.error('Firebase Auth initialization failed:', error);
        }
    }

    waitForFirebase() {
        return new Promise((resolve, reject) => {
            const checkFirebase = () => {
                if (window.firebaseAuth) {
                    resolve();
                } else {
                    setTimeout(checkFirebase, 100);
                }
            };
            
            checkFirebase();
            
            // Timeout after 10 seconds
            setTimeout(() => {
                reject(new Error('Firebase took too long to load'));
            }, 10000);
        });
    }

    onAuthStateChanged(user) {
        // Update UI based on auth state
        this.updateUserInterface(user);
        
        // Update navigation
        this.updateNavigation(user);
        
        // Handle protected routes
        this.handleProtectedRoutes(user);
    }

    updateUserInterface(user) {
        const userElements = document.querySelectorAll('[data-user-info]');
        const loginElements = document.querySelectorAll('[data-login-required]');
        const logoutElements = document.querySelectorAll('[data-logout-required]');
        
        userElements.forEach(element => {
            if (user) {
                element.textContent = user.displayName || user.email || 'User';
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        });
        
        loginElements.forEach(element => {
            element.style.display = user ? 'none' : 'block';
        });
        
        logoutElements.forEach(element => {
            element.style.display = user ? 'block' : 'none';
        });
    }

    updateNavigation(user) {
        const userAvatar = document.querySelector('[data-user-avatar]');
        const userEmail = document.querySelector('[data-user-email]');
        
        if (userAvatar && user) {
            if (user.photoURL) {
                userAvatar.src = user.photoURL;
            } else {
                userAvatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.displayName || user.email)}&background=3b82f6&color=fff`;
            }
        }
        
        if (userEmail && user) {
            userEmail.textContent = user.email;
        }
    }

    handleProtectedRoutes(user) {
        const protectedPages = ['/dashboard', '/profile', '/settings'];
        const currentPath = window.location.pathname;
        
        if (protectedPages.includes(currentPath) && !user) {
            window.location.href = '/auth/login';
        }
    }

    async signInWithGoogle() {
        try {
            const { GoogleAuthProvider, signInWithPopup } = await import('https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js');
            
            const provider = new GoogleAuthProvider();
            provider.addScope('profile');
            provider.addScope('email');
            
            const result = await signInWithPopup(this.auth, provider);
            
            // Send ID token to server
            await this.verifyTokenWithServer(result.user);
            
            return result.user;
        } catch (error) {
            console.error('Google sign-in error:', error);
            throw this.handleAuthError(error);
        }
    }

    async signInWithEmail(email, password) {
        try {
            const { signInWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js');
            
            const result = await signInWithEmailAndPassword(this.auth, email, password);
            
            // Send ID token to server
            await this.verifyTokenWithServer(result.user);
            
            return result.user;
        } catch (error) {
            console.error('Email sign-in error:', error);
            throw this.handleAuthError(error);
        }
    }

    async signUpWithEmail(email, password, displayName = '') {
        try {
            const { createUserWithEmailAndPassword, updateProfile } = await import('https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js');
            
            const result = await createUserWithEmailAndPassword(this.auth, email, password);
            
            // Update profile with display name
            if (displayName) {
                await updateProfile(result.user, { displayName });
            }
            
            // Send ID token to server
            await this.verifyTokenWithServer(result.user);
            
            return result.user;
        } catch (error) {
            console.error('Email sign-up error:', error);
            throw this.handleAuthError(error);
        }
    }

    async signOut() {
        try {
            await this.auth.signOut();
            
            // Clear server session
            await fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            // Redirect to home page
            window.location.href = '/';
        } catch (error) {
            console.error('Sign-out error:', error);
            throw error;
        }
    }

    async resetPassword(email) {
        try {
            const { sendPasswordResetEmail } = await import('https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js');
            
            await sendPasswordResetEmail(this.auth, email);
            
            return true;
        } catch (error) {
            console.error('Password reset error:', error);
            throw this.handleAuthError(error);
        }
    }

    async verifyTokenWithServer(user) {
        try {
            const idToken = await user.getIdToken();
            
            const response = await fetch('/auth/verify-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
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
            });
            
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'Token verification failed');
            }
            
            return result;
        } catch (error) {
            console.error('Token verification error:', error);
            throw error;
        }
    }

    handleAuthError(error) {
        const errorMessages = {
            'auth/user-not-found': 'No account found with this email address.',
            'auth/wrong-password': 'Incorrect password. Please try again.',
            'auth/email-already-in-use': 'An account with this email already exists.',
            'auth/weak-password': 'Password should be at least 6 characters long.',
            'auth/invalid-email': 'Please enter a valid email address.',
            'auth/user-disabled': 'This account has been disabled.',
            'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
            'auth/network-request-failed': 'Network error. Please check your connection.',
            'auth/popup-closed-by-user': 'Sign-in was cancelled.',
            'auth/popup-blocked': 'Please allow popups for this site.',
            'auth/operation-not-allowed': 'This sign-in method is not enabled.',
            'auth/cancelled-popup-request': 'Only one popup request is allowed at a time.',
            'auth/credential-already-in-use': 'This credential is already associated with a different user account.',
            'auth/invalid-credential': 'The credential is malformed or has expired.',
            'auth/quota-exceeded': 'Quota exceeded. Please try again later.',
            'auth/missing-android-pkg-name': 'An Android package name must be provided.',
            'auth/missing-continue-uri': 'A continue URL must be provided.',
            'auth/missing-ios-bundle-id': 'An iOS bundle ID must be provided.',
            'auth/invalid-continue-uri': 'The continue URL provided is invalid.',
            'auth/unauthorized-continue-uri': 'The domain of the continue URL is not whitelisted.',
            'auth/invalid-dynamic-link-domain': 'The provided dynamic link domain is not configured or authorized.',
            'auth/argument-error': 'Please check your request parameters.',
            'auth/invalid-persistence-type': 'The specified persistence type is invalid.',
            'auth/unsupported-persistence-type': 'The current environment does not support the specified persistence type.',
            'auth/invalid-provider-id': 'The specified provider ID is invalid.',
            'auth/invalid-oauth-responsetype': 'Only exactly one OAuth response type should be set to true.',
            'auth/invalid-oauth-clientid': 'The OAuth client ID provided is either invalid or does not match the specified API key.',
            'auth/invalid-oauth-client-secret': 'The OAuth client secret provided is invalid.',
            'auth/invalid-oauth-scope': 'The requested OAuth scope is invalid, unknown, or malformed.',
            'auth/invalid-api-key': 'The provided API key is invalid.',
            'auth/invalid-user-token': 'The user\'s credential is no longer valid. The user must sign in again.',
            'auth/invalid-tenant-id': 'The tenant ID provided is invalid.',
            'auth/tenant-id-mismatch': 'The provided tenant ID does not match the Auth instance\'s tenant ID.',
            'auth/token-expired': 'The user\'s credential is no longer valid. The user must sign in again.',
            'auth/user-token-expired': 'The user\'s credential is no longer valid. The user must sign in again.',
            'auth/requires-recent-login': 'This operation is sensitive and requires recent authentication.',
            'auth/admin-restricted-operation': 'This operation is restricted to administrators only.',
            'auth/internal-error': 'An internal error has occurred.',
            'auth/invalid-phone-number': 'The provided phone number is invalid.',
            'auth/missing-phone-number': 'A phone number is required.',
            'auth/invalid-verification-code': 'The verification code is invalid.',
            'auth/invalid-verification-id': 'The verification ID is invalid.',
            'auth/missing-verification-code': 'The verification code is required.',
            'auth/missing-verification-id': 'The verification ID is required.',
            'auth/captcha-check-failed': 'The reCAPTCHA response token provided is either invalid, expired, already used or the domain associated with it does not match the list of whitelisted domains.',
            'auth/invalid-app-credential': 'The phone verification request contains an invalid application verifier.',
            'auth/invalid-app-id': 'The mobile app identifier is not registered for the current project.',
            'auth/missing-app-credential': 'The phone verification request is missing an application verifier assertion.',
            'auth/session-cookie-expired': 'The Firebase session cookie has expired.',
            'auth/session-cookie-revoked': 'The Firebase session cookie has been revoked.',
            'auth/invalid-session-cookie-duration': 'The session cookie duration must be a valid number in milliseconds between 5 minutes and 2 weeks.',
            'auth/email-change-needs-verification': 'Multi-factor users must always have a verified email.',
            'auth/email-already-exists': 'The provided email is already in use by an existing user.',
            'auth/reserved-claims': 'One or more custom user claims provided are reserved.',
            'auth/invalid-claims': 'The provided custom claim attributes are invalid.',
            'auth/phone-number-already-exists': 'The provided phone number is already in use by an existing user.',
            'auth/invalid-display-name': 'The provided display name is invalid.',
            'auth/invalid-photo-url': 'The provided photo URL is invalid.',
            'auth/uid-already-exists': 'The provided uid is already in use by an existing user.',
            'auth/invalid-uid': 'The provided uid must be a non-empty string with at most 128 characters.',
            'auth/uid-generator-not-available': 'The uid generator is not available.',
            'auth/project-not-found': 'No Firebase project was found.',
            'auth/insufficient-permission': 'The credential used to initialize the Admin SDK has insufficient permission.',
            'auth/invalid-argument': 'An invalid argument was provided.',
            'auth/invalid-creation-time': 'The creation time must be a valid UTC date string.',
            'auth/invalid-last-sign-in-time': 'The last sign-in time must be a valid UTC date string.',
            'auth/invalid-page-token': 'The provided next page token is invalid.',
            'auth/maximum-user-count-exceeded': 'The maximum allowed number of users to import has been exceeded.',
            'auth/missing-hash-algorithm': 'Importing users with password hashes requires that the hash algorithm and its parameters be provided.',
            'auth/missing-hash-memory-cost': 'The memory cost is required when using the SCRYPT hash algorithm.',
            'auth/missing-hash-parallelization': 'The parallelization is required when using the SCRYPT hash algorithm.',
            'auth/missing-hash-derived-key-length': 'The derived key length is required when using the SCRYPT hash algorithm.',
            'auth/missing-hash-block-size': 'The block size is required when using the SCRYPT hash algorithm.',
            'auth/missing-hash-rounds': 'The rounds is required when using the PBKDF2 hash algorithm.',
            'auth/missing-hash-salt-separator': 'The salt separator is required when using the SCRYPT hash algorithm.',
            'auth/forbidden-claim': 'The provided custom claim is forbidden.',
            'auth/invalid-hash-algorithm': 'The provided hash algorithm is invalid.',
            'auth/invalid-hash-memory-cost': 'The memory cost must be a valid number.',
            'auth/invalid-hash-parallelization': 'The parallelization must be a valid number.',
            'auth/invalid-hash-derived-key-length': 'The derived key length must be a valid number.',
            'auth/invalid-hash-block-size': 'The block size must be a valid number.',
            'auth/invalid-hash-rounds': 'The rounds must be a valid number.',
            'auth/invalid-hash-salt-separator': 'The salt separator must be a valid string.',
            'auth/invalid-id-token': 'The provided ID token is not a valid Firebase ID token.',
            'auth/id-token-expired': 'The provided Firebase ID token is expired.',
            'auth/id-token-revoked': 'The Firebase ID token has been revoked.',
            'auth/invalid-refresh-token': 'The provided refresh token is invalid.',
            'auth/invalid-custom-token': 'The provided custom token is invalid.',
            'auth/custom-token-mismatch': 'The custom token corresponds to a different audience.'
        };
        
        const userMessage = errorMessages[error.code] || 'An error occurred during authentication. Please try again.';
        
        return {
            code: error.code,
            message: userMessage,
            originalMessage: error.message
        };
    }

    getCurrentUser() {
        return this.currentUser;
    }

    isAuthenticated() {
        return !!this.currentUser;
    }

    async getCurrentUserToken() {
        if (!this.currentUser) {
            throw new Error('No user is currently signed in');
        }
        
        return await this.currentUser.getIdToken();
    }

    async refreshToken() {
        if (!this.currentUser) {
            throw new Error('No user is currently signed in');
        }
        
        return await this.currentUser.getIdToken(true);
    }
}

// Initialize Firebase Auth Handler
const firebaseAuthHandler = new FirebaseAuthHandler();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    firebaseAuthHandler.initialize();
});

// Export for global use
window.firebaseAuthHandler = firebaseAuthHandler;
