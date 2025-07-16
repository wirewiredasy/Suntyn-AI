# Firebase Authentication Domain Fix

## Problem
Authentication fails because the current Replit domain is not authorized in Firebase Console.

## Current Domain
Your Replit app domain: `workspace--tooloraai.replit.dev`

## Firebase Project Details
- Project ID: `tooloraai-eccee`
- API Key: Configured ✓
- App ID: Configured ✓

## Quick Fix Steps

### Step 1: Go to Firebase Console
1. Open: https://console.firebase.google.com
2. Select project: **tooloraai-eccee**

### Step 2: Add Authorized Domain
1. Go to **Authentication** (left sidebar)
2. Click **Settings** tab
3. Scroll down to **Authorized domains**
4. Click **Add domain** button
5. Add this domain: `workspace--tooloraai.replit.dev`
6. Click **Done**

### Step 3: Test Authentication
1. Come back to your app
2. Refresh the page
3. Try logging in with Google or email/password

## Alternative Domains to Add (if needed)
If your Replit domain changes, also add these common patterns:
- `workspace--tooloraai.replit.dev`
- `*.replit.dev` (wildcard - may not be supported)
- Your custom domain if you have one

## Current Status
- ❌ Authentication failing due to unauthorized domain
- ✅ Firebase configuration is correct
- ✅ All other code is working properly

Once you add the domain to Firebase Console, authentication will work immediately without any code changes needed.