#!/usr/bin/env python3
"""
Neon Database Setup Script
Quick setup for Neon database connection
"""
import os
from app import app, db
from models import ToolCategory, Tool, User

def setup_neon_database():
    """Setup Neon PostgreSQL database with all tables"""
    
    # Get Neon database URL
    neon_url = os.environ.get("NEON_DATABASE_URL", "")
    database_url = os.environ.get("DATABASE_URL", "")
    
    # Use whichever is available
    if neon_url:
        print("🚀 Using NEON_DATABASE_URL")
        connection_url = neon_url
    elif "neon.tech" in database_url:
        print("🚀 Using DATABASE_URL (Neon detected)")
        connection_url = database_url
    else:
        print("❌ No Neon database URL found")
        print("\n📝 To set up Neon:")
        print("1. Go to https://neon.tech")
        print("2. Create a new project")
        print("3. Copy the connection string")
        print("4. Add to Replit Secrets: NEON_DATABASE_URL=postgresql://...")
        return False
    
    # Configure connection with pooling
    if connection_url.startswith("postgres://"):
        connection_url = connection_url.replace("postgres://", "postgresql://", 1)
    
    # Use connection pooler if available
    if '.us-east-2.' in connection_url and 'pooler' not in connection_url:
        pooled_url = connection_url.replace('.us-east-2.', '-pooler.us-east-2.')
        print("✅ Using Neon Connection Pooler")
        connection_url = pooled_url
    
    # Update app configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "connect_args": {
            "sslmode": "prefer",
            "connect_timeout": 30,
            "application_name": "Toolora_AI"
        }
    }
    
    try:
        with app.app_context():
            # Test connection
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                print("✅ Neon connection successful")
                
                # Create all tables
                db.create_all()
                print("✅ Database tables created")
                
                # Check data
                categories = ToolCategory.query.count()
                tools = Tool.query.count()
                users = User.query.count()
                
                print(f"📊 Database Stats:")
                print(f"   Categories: {categories}")
                print(f"   Tools: {tools}")
                print(f"   Users: {users}")
                
                # Populate tools if empty
                if tools == 0:
                    print("📦 Populating database with 85 tools...")
                    from populate_all_85_tools import populate_all_tools
                    populate_all_tools()
                    print("✅ Database populated successfully!")
                
                return True
                
    except Exception as e:
        print(f"❌ Neon setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Neon Database Setup")
    print("=" * 30)
    
    if setup_neon_database():
        print("\n🎉 Neon setup successful!")
    else:
        print("\n❌ Neon setup failed!")