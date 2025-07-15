from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import User
from app import db
from firebase_config import verify_firebase_token
import os
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@auth_bp.route('/register')
def register():
    return render_template('auth/register.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify Firebase ID token and create/update user session"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        id_token = data.get('idToken')
        user_info = data.get('userInfo', {})
        
        # Try to verify token with Firebase Admin SDK first
        if id_token:
            verified_user = verify_firebase_token(id_token)
            if verified_user:
                # Use verified user info from Firebase
                user_info = {
                    'uid': verified_user['uid'],
                    'email': verified_user['email'],
                    'displayName': verified_user.get('name'),
                    'photoURL': verified_user.get('picture'),
                    'emailVerified': verified_user.get('email_verified', False)
                }
            else:
                # If verification fails, still check if we have basic user info
                if not user_info.get('uid') or not user_info.get('email'):
                    return jsonify({'error': 'Token verification failed and no user info provided'}), 400
        elif not user_info.get('uid') or not user_info.get('email'):
            return jsonify({'error': 'Missing required user information'}), 400
        
        # Create or update user in database
        user = User.query.filter_by(firebase_uid=user_info.get('uid')).first()
        
        if not user:
            # Check if email already exists
            existing_user = User.query.filter_by(email=user_info.get('email')).first()
            if existing_user:
                # Link Firebase UID to existing user
                existing_user.firebase_uid = user_info.get('uid')
                existing_user.display_name = user_info.get('displayName') or existing_user.display_name
                existing_user.photo_url = user_info.get('photoURL') or existing_user.photo_url
                user = existing_user
            else:
                # Create new user
                user = User(
                    firebase_uid=user_info.get('uid'),
                    email=user_info.get('email'),
                    display_name=user_info.get('displayName') or user_info.get('email').split('@')[0],
                    photo_url=user_info.get('photoURL')
                )
                db.session.add(user)
        else:
            # Update existing user info
            user.display_name = user_info.get('displayName') or user.display_name
            user.photo_url = user_info.get('photoURL') or user.photo_url
        
        db.session.commit()
        
        # Set session
        session['user_id'] = user.id
        session['firebase_uid'] = user.firebase_uid
        
        return jsonify({'success': True, 'user': {
            'id': user.id,
            'email': user.email,
            'displayName': user.display_name,
            'photoURL': user.photo_url
        }})
    
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear user session"""
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/user')
def get_user():
    """Get current user info"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'displayName': user.display_name,
        'photoURL': user.photo_url,
        'theme': user.theme,
        'language': user.language
    })
