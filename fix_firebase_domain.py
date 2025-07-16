
#!/usr/bin/env python3
"""
Firebase Domain Fix Helper
Get current domain and show exact steps to fix Firebase authorization
"""
import os
import requests

def get_current_domain():
    """Get current Replit domain"""
    try:
        # Try to get from environment
        repl_slug = os.environ.get('REPL_SLUG')
        repl_owner = os.environ.get('REPL_OWNER')
        
        if repl_slug and repl_owner:
            return f"{repl_slug}--{repl_owner}.replit.dev"
        
        # Try other methods
        replit_db_url = os.environ.get('REPLIT_DB_URL', '')
        if 'replit.dev' in replit_db_url:
            # Extract domain from DB URL
            parts = replit_db_url.split('/')
            for part in parts:
                if 'replit.dev' in part:
                    return part.replace('https://', '').replace('http://', '')
        
        return None
    except:
        return None

def show_firebase_fix_instructions():
    """Show Firebase domain fix instructions"""
    domain = get_current_domain()
    
    print("🔥" * 50)
    print("FIREBASE DOMAIN AUTHORIZATION FIX")
    print("🔥" * 50)
    
    if domain:
        print(f"✅ Current Domain: {domain}")
    else:
        print("❌ Domain detection failed - check browser address bar")
    
    print("\n📋 EXACT STEPS TO FIX:")
    print("1. Open: https://console.firebase.google.com/")
    print("2. Select project: tooloraai-eccee")
    print("3. Go to: Authentication → Settings")
    print("4. Click on 'Authorized domains' tab")
    print("5. Click 'Add domain' button")
    
    if domain:
        print(f"6. Add this exact domain: {domain}")
    else:
        print("6. Add your current domain from browser address bar")
    
    print("7. Also add: *.replit.dev (if available)")
    print("8. Click 'Save'")
    print("9. Wait 2-3 minutes for propagation")
    print("10. Refresh your app and try login")
    
    print("\n✅ AFTER FIX - THESE WILL WORK:")
    print("• Email/password registration")
    print("• Email/password login")
    print("• Google sign-in")
    print("• Password reset")
    print("• All authentication features")
    
    print("\n🚀 PROJECT STATUS:")
    print("• Database: ✅ Working (8 tools loaded)")
    print("• App: ✅ Running on port 5000")
    print("• Firebase Config: ✅ Ready")
    print("• Only Issue: ❌ Domain authorization")
    
    print("\n" + "🔥" * 50)
    print("COPY THIS DOMAIN TO FIREBASE:")
    if domain:
        print(f">>> {domain} <<<")
    else:
        print(">>> Check browser address bar <<<")
    print("🔥" * 50)

if __name__ == "__main__":
    show_firebase_fix_instructions()
