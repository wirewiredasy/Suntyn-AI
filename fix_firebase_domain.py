#!/usr/bin/env python3
"""
Firebase Domain Fix Helper
Get current domain and show exact steps to fix Firebase authorization
"""

import os
import requests

def get_current_domain():
    """Get current Replit domain"""
    # Check environment variables for domain
    replit_domain = os.environ.get('REPLIT_DOMAINS')
    replit_url = os.environ.get('REPLIT_URL')
    
    current_domain = None
    
    if replit_domain:
        current_domain = replit_domain.split(',')[0].strip()
    elif replit_url:
        current_domain = replit_url.replace('https://', '').replace('http://', '')
    
    # Also try to detect from system
    try:
        response = requests.get('http://httpbin.org/ip', timeout=5)
        print(f"External IP check successful")
    except:
        print("Could not determine external access")
    
    return current_domain

def show_firebase_fix_instructions():
    """Show Firebase domain fix instructions"""
    current_domain = get_current_domain()
    
    print("🔥 FIREBASE DOMAIN AUTHORIZATION FIX")
    print("="*50)
    
    if current_domain:
        print(f"✅ Current Domain Detected: {current_domain}")
    else:
        print("⚠️  Could not auto-detect domain")
        current_domain = "your-replit-domain.replit.dev"
    
    print("\n📋 FOLLOW THESE EXACT STEPS:")
    print("-" * 30)
    
    print("1. Open Firebase Console:")
    print("   https://console.firebase.google.com/")
    
    print("\n2. Select your project: tooloraai-eccee")
    
    print("\n3. Go to: Authentication → Settings → Authorized domains")
    
    print(f"\n4. Add this domain: {current_domain}")
    
    print("\n5. Save the changes")
    
    print("\n6. Test authentication in your app")
    
    print("\n" + "="*50)
    print("🎯 After adding the domain, authentication will work!")
    
    return current_domain

if __name__ == "__main__":
    show_firebase_fix_instructions()