#!/usr/bin/env python3
"""
Script to detect current domain and provide Firebase setup instructions
"""
import os
import sys

def get_current_domain():
    """Get current domain from environment or system"""
    # Check common environment variables
    domain_sources = [
        os.environ.get('REPLIT_DOMAIN'),
        os.environ.get('REPL_SLUG'),
        os.environ.get('REPL_OWNER')
    ]
    
    # Try to construct domain
    if os.environ.get('REPL_SLUG') and os.environ.get('REPL_OWNER'):
        return f"{os.environ.get('REPL_SLUG')}--{os.environ.get('REPL_OWNER')}.replit.dev"
    
    # Fallback to hostname
    try:
        import socket
        hostname = socket.gethostname()
        if hostname and not hostname.startswith('localhost'):
            return f"{hostname}.replit.dev"
    except:
        pass
    
    return None

def print_firebase_instructions():
    """Print Firebase setup instructions"""
    domain = get_current_domain()
    
    print("="*60)
    print("🔥 FIREBASE DOMAIN AUTHORIZATION FIX")
    print("="*60)
    
    if domain:
        print(f"✅ Detected Domain: {domain}")
    else:
        print("❌ Could not auto-detect domain")
        print("👀 Check your browser address bar for the exact domain")
    
    print("\n📋 STEPS TO FIX:")
    print("1. Go to: https://console.firebase.google.com/")
    print("2. Select your project")
    print("3. Go to: Authentication → Settings → Authorized domains")
    print("4. Click 'Add domain'")
    
    if domain:
        print(f"5. Add this domain: {domain}")
    print("6. Also add: *.replit.dev (if available)")
    print("7. Wait 2-3 minutes and test authentication")
    
    print("\n🚀 AFTER DOMAIN FIX:")
    print("✅ Email/password login will work")
    print("✅ Google sign-in will work")
    print("✅ User registration will work")
    print("✅ Password reset will work")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print_firebase_instructions()