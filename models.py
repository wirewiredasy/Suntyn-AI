from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import JSON


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    # Removed Firebase authentication
    email = db.Column(db.String(120), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User preferences
    theme = db.Column(db.String(10), default='light')
    language = db.Column(db.String(10), default='en')
    
    # Premium features
    is_premium = db.Column(db.Boolean, default=False)
    premium_until = db.Column(db.DateTime, nullable=True)
    credits = db.Column(db.Integer, default=100)
    
    # Settings
    preferences = db.Column(JSON, default=lambda: {})
    
    # Relationships
    tool_history = db.relationship('ToolHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_files = db.relationship('SavedFile', backref='user', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('UserAnalytics', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def get_id(self):
        return str(self.id)

    @property
    def is_active_premium(self):
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return True
        return datetime.utcnow() < self.premium_until


class ToolHistory(db.Model):
    __tablename__ = 'tool_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    tool_name = db.Column(db.String(100), nullable=False)
    tool_category = db.Column(db.String(50), nullable=False)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_count = db.Column(db.Integer, default=1)
    processing_time = db.Column(db.Float, nullable=True)
    file_size_mb = db.Column(db.Float, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<ToolHistory {self.tool_name}>'


class SavedFile(db.Model):
    __tablename__ = 'saved_files'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    original_filename = db.Column(db.String(255), nullable=False)
    saved_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    tool_used = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<SavedFile {self.original_filename}>'

    @property
    def is_expired(self):
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at


class ToolCategory(db.Model):
    __tablename__ = 'tool_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(20), default='indigo')
    tool_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)


class Tool(db.Model):
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('tool_categories.id'), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_premium = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0)
    features = db.Column(JSON, default=lambda: [])
    file_types = db.Column(JSON, default=lambda: [])
    max_file_size_mb = db.Column(db.Integer, default=16)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    category = db.relationship('ToolCategory', backref='tools')


class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=False)
    page_url = db.Column(db.String(500), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    extra_data = db.Column(JSON, default=lambda: {})
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)


class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(100), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    usage_count = db.Column(db.Integer, default=0)
    rate_limit = db.Column(db.Integer, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='api_keys')


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    current_period_start = db.Column(db.DateTime, nullable=False)
    current_period_end = db.Column(db.DateTime, nullable=False)
    cancel_at_period_end = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='subscriptions')