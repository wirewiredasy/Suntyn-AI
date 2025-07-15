import os
import json
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    if not firebase_admin._apps:
        try:
            # Try to get service account from environment variable
            service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
            
            if service_account_json:
                # Parse the JSON string from environment variable
                service_account_dict = json.loads(service_account_json)
                cred = credentials.Certificate(service_account_dict)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized successfully")
            else:
                # Initialize with default credentials (for development)
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized with default credentials")
                
        except Exception as e:
            print(f"Failed to initialize Firebase Admin SDK: {e}")
            # Continue without Firebase Admin for development
            pass

def verify_firebase_token(id_token):
    """Verify Firebase ID token and return user info"""
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        return {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False),
            'name': decoded_token.get('name'),
            'picture': decoded_token.get('picture'),
            'provider': decoded_token.get('firebase', {}).get('sign_in_provider')
        }
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

# Initialize Firebase when module is imported
initialize_firebase()