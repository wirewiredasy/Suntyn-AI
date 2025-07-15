# Firebase Authentication Setup Guide

## Current Issue: Domain Authorization

Your Firebase authentication is failing because the current Replit domain is not authorized in Firebase. Here's how to fix it:

## Step 1: Add Your Replit Domain to Firebase

1. **Get your current domain**: Your Replit app URL (something like `https://[random-chars].replit.dev` or `https://[your-repl-name]-[username].replit.dev`)

2. **Go to Firebase Console**:
   - Visit https://console.firebase.google.com/
   - Select your project
   - Go to **Authentication > Settings > Authorized domains**

3. **Add these domains**:
   - `localhost` (for development)
   - `[your-repl-name].replit.dev` (your current domain)
   - `replit.dev` (wildcard for all replit domains)
   - `*.replit.dev` (if available)

## Step 2: Service Account Setup (Optional but Recommended)

For better security, you can set up a service account:

1. **Generate Service Account Key**:
   - Go to Firebase Console > Project Settings > Service accounts
   - Click "Generate new private key"
   - Download the JSON file

2. **Add to Replit Secrets**:
   - Copy the entire JSON content
   - Add as secret key: `FIREBASE_SERVICE_ACCOUNT_JSON`
   - Paste the JSON as the value

## Step 3: Test Authentication

After adding the domains, authentication should work with:
- Email/password sign up and login
- Google sign-in (if domain is properly authorized)

## Current Implementation Status

✅ Firebase Admin SDK installed and configured
✅ Proper token verification with fallback
✅ Enhanced error handling for unauthorized domains
✅ Database user creation and linking
✅ Session management

## Troubleshooting

If you still have issues:
1. Double-check the domain in Firebase Console
2. Wait a few minutes for changes to propagate
3. Try clearing browser cache
4. Check browser console for specific error messages

## Alternative: Email-Only Authentication

If Google sign-in continues to fail, users can still register and login with email/password, which doesn't require domain authorization.