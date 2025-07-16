#!/usr/bin/env python3
"""
Database Setup Script for Multiple Providers
Supports: Neon, Render PostgreSQL, Supabase
"""
import os
import sys
from urllib.parse import urlparse
from app import app, db
from models import ToolCategory, Tool, User
from config import Config

def detect_database_provider(database_url):
    """Detect database provider from URL"""
    if not database_url:
        return "unknown"
    
    parsed = urlparse(database_url)
    host = parsed.hostname or ""
    
    if "neon.tech" in host:
        return "neon"
    elif "render.com" in host:
        return "render"
    elif "supabase.co" in host:
        return "supabase"
    elif "replit.dev" in host or "replit.com" in host:
        return "replit"
    else:
        return "custom"

def get_database_config(provider, database_url):
    """Get optimized database configuration for provider"""
    base_config = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    if provider in ["neon", "render", "supabase"]:
        # Production cloud database configuration
        base_config.update({
            "pool_size": 10,
            "max_overflow": 20,
            "pool_timeout": 30,
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 30,
            }
        })
    elif provider == "replit":
        # Replit database configuration
        base_config.update({
            "pool_size": 5,
            "max_overflow": 10,
            "pool_timeout": 20,
        })
    
    return base_config

def setup_database_connection():
    """Setup database connection with optimal configuration"""
    database_url = os.environ.get("DATABASE_URL", "sqlite:///toolora.db")
    
    # Fix PostgreSQL URL format if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    provider = detect_database_provider(database_url)
    print(f"🔍 Detected database provider: {provider.upper()}")
    
    # Get optimized configuration
    config = get_database_config(provider, database_url)
    
    # Update app configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = config
    
    print(f"✅ Database configured for {provider.upper()}")
    print(f"📍 Connection URL: {database_url[:50]}...")
    
    return provider, database_url

def test_database_connection():
    """Test database connection and basic operations"""
    try:
        with app.app_context():
            # Test connection
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                print("✅ Database connection successful")
            
            # Test table creation
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Test basic query
            category_count = ToolCategory.query.count()
            tool_count = Tool.query.count()
            user_count = User.query.count()
            
            print(f"📊 Database Statistics:")
            print(f"   Categories: {category_count}")
            print(f"   Tools: {tool_count}")
            print(f"   Users: {user_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def create_setup_instructions():
    """Create setup instructions for all providers"""
    instructions = """
# Database Setup Instructions for Toolora AI

## Option 1: Neon Database (Recommended)
1. Go to https://neon.tech
2. Create a new project
3. Copy the connection string from the dashboard
4. Set as environment variable: DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/dbname

## Option 2: Render PostgreSQL
1. Go to https://render.com
2. Create a new PostgreSQL database
3. Copy the Internal Database URL
4. Set as environment variable: DATABASE_URL=postgresql://username:password@xxx.render.com/dbname

## Option 3: Supabase
1. Go to https://supabase.com
2. Create a new project
3. Go to Settings → Database → Connection string
4. Copy the connection string (use Transaction pooler)
5. Replace [YOUR-PASSWORD] with your actual password
6. Set as environment variable: DATABASE_URL=postgresql://username:password@xxx.supabase.co/postgres

## Current Configuration
Your app is configured to automatically detect and optimize for any of these providers.
"""
    
    with open("DATABASE_SETUP_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("📝 Setup instructions created: DATABASE_SETUP_INSTRUCTIONS.md")

def main():
    print("🚀 Database Setup for Toolora AI")
    print("=" * 50)
    
    # Setup database connection
    provider, url = setup_database_connection()
    
    # Test connection
    if test_database_connection():
        print(f"\n🎉 Database setup complete for {provider.upper()}!")
        
        # Populate tools if database is empty
        with app.app_context():
            if Tool.query.count() == 0:
                print("📦 Populating database with tools...")
                from populate_all_85_tools import populate_all_tools
                populate_all_tools()
    else:
        print(f"\n❌ Database setup failed for {provider.upper()}")
        print("Check your DATABASE_URL environment variable")
    
    # Create setup instructions
    create_setup_instructions()

if __name__ == "__main__":
    main()