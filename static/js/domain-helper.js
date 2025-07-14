
// Domain Helper for Firebase Configuration
class DomainHelper {
    static getCurrentDomain() {
        return window.location.hostname;
    }
    
    static isLocalDevelopment() {
        const hostname = this.getCurrentDomain();
        return hostname === 'localhost' || hostname === '127.0.0.1' || hostname.endsWith('.replit.dev');
    }
    
    static getReplitDomain() {
        const hostname = this.getCurrentDomain();
        if (hostname.includes('.replit.app') || hostname.includes('.replit.dev')) {
            return hostname;
        }
        return null;
    }
    
    static showDomainInstructions() {
        const domain = this.getCurrentDomain();
        console.log(`
Firebase Domain Setup Instructions:
1. Go to Firebase Console: https://console.firebase.google.com/
2. Select your project
3. Navigate to Authentication → Settings
4. Click on "Authorized domains" tab
5. Add this domain: ${domain}
6. Save the changes

Current domain: ${domain}
        `);
        
        // Show user-friendly message
        if (window.firebaseAuthHandler) {
            alert(`Please add ${domain} to your Firebase authorized domains list. Check console for detailed instructions.`);
        }
    }
}

// Auto-check domain on page load
document.addEventListener('DOMContentLoaded', function() {
    const domain = DomainHelper.getCurrentDomain();
    console.log('Current domain:', domain);
    
    // Log Replit-specific domain info
    if (DomainHelper.getReplitDomain()) {
        console.log('Replit domain detected:', DomainHelper.getReplitDomain());
    }
});

window.DomainHelper = DomainHelper;
