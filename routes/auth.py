from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models import User
from app import db
import os
import json

auth_bp = Blueprint('auth', __name__)

# Authentication disabled - all tools freely accessible

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """No authentication required - return success for compatibility"""
    return jsonify({'success': True, 'message': 'All tools are freely accessible'})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear user session"""
    logout_user()
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/user')
def get_user():
    """Return guest user info - no authentication required"""
    return jsonify({
        'id': 'guest',
        'email': 'guest@toolora.ai',
        'displayName': 'Guest User',
        'photoURL': None,
        'theme': 'light',
        'language': 'en'
    })