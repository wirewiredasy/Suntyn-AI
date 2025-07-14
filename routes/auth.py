from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import User
from app import db
import os
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify Firebase ID token and create/update user session"""
    try:
        data = request.get_json()
        if not data or 'idToken' not in data:
            return jsonify({'error': 'ID token required'}), 400
        
        # In a real app, you would verify the ID token with Firebase Admin SDK
        # For this demo, we'll extract user info from the token payload
        user_info = data.get('userInfo', {})
        
        # Create or update user in database
        user = User.query.filter_by(firebase_uid=user_info.get('uid')).first()
        
        if not user:
            user = User(
                firebase_uid=user_info.get('uid'),
                email=user_info.get('email'),
                display_name=user_info.get('displayName'),
                photo_url=user_info.get('photoURL')
            )
            db.session.add(user)
        else:
            # Update existing user info
            user.display_name = user_info.get('displayName')
            user.photo_url = user_info.get('photoURL')
        
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
        return jsonify({'error': str(e)}), 500

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
