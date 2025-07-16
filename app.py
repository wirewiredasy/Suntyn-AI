import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///toolora.db")
neon_database_url = os.environ.get("NEON_DATABASE_URL", "")

# Use Neon database if available, otherwise use primary database
if neon_database_url:
    database_url = neon_database_url
    print("🚀 Using Neon Database")
else:
    print("🚀 Using Primary Database")

# Fix PostgreSQL connection for proper format
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# PostgreSQL database configuration (Render/Neon)
if "postgresql" in database_url or "render" in database_url or "neon" in database_url:
    # Check if it's Neon database for connection pooling
    if "neon" in database_url or neon_database_url:
        # Use Neon's connection pooler for better performance
        pooled_url = database_url.replace('.us-east-2', '-pooler.us-east-2')
        if pooled_url != database_url:
            app.config["SQLALCHEMY_DATABASE_URI"] = pooled_url
            print("✅ Using Neon Connection Pooler")
    
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 20,
        "pool_size": 10,
        "max_overflow": 20,
        "connect_args": {
            "sslmode": "require" if "render" in database_url else "prefer",
            "connect_timeout": 30,
            "application_name": "Toolora_AI"
        }
    }
else:
    # Local SQLite configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import routes after app creation to avoid circular imports
from routes.main import main_bp
from routes.tools import tools_bp
from routes.auth import auth_bp
from routes.api import api_bp
from routes.enhanced_api import api_bp as enhanced_api_bp

app.register_blueprint(main_bp)
app.register_blueprint(tools_bp, url_prefix='/tools')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(enhanced_api_bp, url_prefix='/enhanced_api')

with app.app_context():
    # Import models here so their tables are created
    import models
    db.create_all()

# Add Firebase config to all templates
@app.context_processor
def inject_firebase_config():
    return {
        'firebase_api_key': os.environ.get("FIREBASE_API_KEY", ""),
        'firebase_project_id': os.environ.get("FIREBASE_PROJECT_ID", ""),
        'firebase_app_id': os.environ.get("FIREBASE_APP_ID", "")
    }

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
