#!/usr/bin/env python3
"""
Supabase Database Setup Script
Quick setup for Supabase database connection
"""
import os
from app import app, db
from models import ToolCategory, Tool, User

def setup_supabase_connection():
    """Configure Supabase database connection"""
    
    # Supabase connection string format
    supabase_url = os.environ.get("SUPABASE_DATABASE_URL", "")
    
    if not supabase_url:
        print("❌ SUPABASE_DATABASE_URL not found in environment variables")
        print("\n📝 To set up Supabase:")
        print("1. Go to https://supabase.com")
        print("2. Create a new project")
        print("3. Go to Settings → Database → Connection string")
        print("4. Copy the connection string (Transaction pooler)")
        print("5. Replace [YOUR-PASSWORD] with your actual password")
        print("6. Add to Replit Secrets: SUPABASE_DATABASE_URL=postgresql://...")
        return False
    
    # Update app configuration for Supabase
    app.config["SQLALCHEMY_DATABASE_URI"] = supabase_url
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
    
    print("🚀 Supabase database configured")
    return True

def test_supabase_connection():
    """Test Supabase connection"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                print("✅ Supabase connection successful")
                
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
        print(f"❌ Supabase connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Supabase Database Setup")
    print("=" * 30)
    
    if setup_supabase_connection():
        if test_supabase_connection():
            print("\n🎉 Supabase setup successful!")
        else:
            print("\n❌ Supabase setup failed!")
    else:
        print("\n❌ Supabase configuration failed!")