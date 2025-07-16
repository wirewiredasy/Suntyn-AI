#!/usr/bin/env python3
"""
Render PostgreSQL Database Setup Script
Quick setup for Render database connection
"""
import os
from app import app, db
from models import ToolCategory, Tool, User

def setup_render_connection():
    """Configure Render database connection"""
    
    # Render connection string format
    render_url = os.environ.get("RENDER_DATABASE_URL", "")
    
    if not render_url:
        print("❌ RENDER_DATABASE_URL not found in environment variables")
        print("\n📝 To set up Render PostgreSQL:")
        print("1. Go to https://render.com")
        print("2. Create a new PostgreSQL database")
        print("3. Copy the Internal Database URL")
        print("4. Add to Replit Secrets: RENDER_DATABASE_URL=postgresql://...")
        return False
    
    # Update app configuration for Render
    app.config["SQLALCHEMY_DATABASE_URI"] = render_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "connect_args": {
            "sslmode": "require",
            "connect_timeout": 30,
            "application_name": "Toolora_AI"
        }
    }
    
    print("🚀 Render database configured")
    return True

def test_render_connection():
    """Test Render connection"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                print("✅ Render connection successful")
                
                # Create tables
                db.create_all()
                print("✅ Database tables created")
                
                # Test queries
                categories = ToolCategory.query.count()
                tools = Tool.query.count()
                users = User.query.count()
                
                print(f"📊 Database Stats:")
                print(f"   Categories: {categories}")
                print(f"   Tools: {tools}")
                print(f"   Users: {users}")
                
                return True
    except Exception as e:
        print(f"❌ Render connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Render Database Setup")
    print("=" * 30)
    
    if setup_render_connection():
        if test_render_connection():
            print("\n🎉 Render setup successful!")
        else:
            print("\n❌ Render setup failed!")
    else:
        print("\n❌ Render configuration failed!")