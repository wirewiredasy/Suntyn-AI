# Google OAuth Domain Fix Guide

## Problem
Google sign-up failing on Render domain `tooloraai.onrender.com`

## Solution

### Step 1: Add Domain to Firebase Console
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `tooloraai-eccee`
3. Go to **Authentication** → **Settings** → **Authorized domains**
4. Click **Add domain**
5. Add: `tooloraai.onrender.com`
6. Save

### Step 2: Update Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Select your project
3. Click on your OAuth 2.0 Client ID
4. Add to **Authorized redirect URIs**:
   - `https://tooloraai.onrender.com/auth/google/callback`
   - `https://tooloraai.onrender.com/google_login/callback`
5. Save

### Step 3: Set Environment Variables
Make sure these are set in Render:
```
GOOGLE_OAUTH_CLIENT_ID=your_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
```

### Current Domain
Your current domain is: `tooloraai.onrender.com`

## Verify Fix
After adding the domain, test:
1. Go to registration page
2. Click "Sign up with Google"
3. Should redirect properly without errors

## Error Message
"Google sign-up failed. Please try again." means domain authorization is missing.