from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User preferences
    theme = db.Column(db.String(10), default='light')
    language = db.Column(db.String(10), default='en')
    
    # Relationships
    tool_history = db.relationship('ToolHistory', backref='user', lazy=True)
    saved_files = db.relationship('SavedFile', backref='user', lazy=True)

class ToolHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tool_name = db.Column(db.String(100), nullable=False)
    tool_category = db.Column(db.String(50), nullable=False)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_count = db.Column(db.Integer, default=1)

class SavedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    saved_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    tool_used = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ToolCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(20), default='indigo')
    tool_count = db.Column(db.Integer, default=0)
