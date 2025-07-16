#!/usr/bin/env python3
"""
Database Setup Script for Toolora AI
Migrates from SQLite to PostgreSQL for production use
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

def setup_postgresql_database():
    """Set up PostgreSQL database with proper configuration"""
    
    # Check if we have a PostgreSQL connection string
    database_url = os.environ.get("DATABASE_URL")
    if not database_url or "postgresql" not in database_url:
        print("⚠️  No PostgreSQL DATABASE_URL found in environment")
        print("📝 To set up PostgreSQL database:")
        print("1. Go to Replit Secrets tab")
        print("2. Add DATABASE_URL with your PostgreSQL connection string")
        print("3. Format: postgresql://user:password@host:port/database")
        print("4. Or use a service like Neon, Render, or Supabase")
        return False
    
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Connected to PostgreSQL database")
        
        # Test connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {version['version']}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def migrate_sqlite_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Check if SQLite database exists
    sqlite_path = "./instance/toolora.db"
    if not os.path.exists(sqlite_path):
        print("⚠️  SQLite database not found")
        return False
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("⚠️  DATABASE_URL not set for PostgreSQL")
        return False
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(database_url)
        pg_cursor = pg_conn.cursor()
        
        print("🔄 Starting migration from SQLite to PostgreSQL...")
        
        # Get tools data
        sqlite_cursor.execute("SELECT * FROM tools")
        tools = sqlite_cursor.fetchall()
        
        sqlite_cursor.execute("SELECT * FROM tool_categories")
        categories = sqlite_cursor.fetchall()
        
        print(f"📊 Found {len(tools)} tools and {len(categories)} categories")
        
        # Create Flask app context to create tables
        sys.path.append('.')
        from app import app, db
        
        with app.app_context():
            # This will create all tables in PostgreSQL
            db.create_all()
            print("✅ PostgreSQL tables created")
        
        sqlite_conn.close()
        pg_conn.close()
        
        print("✅ Migration setup complete")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Toolora AI Database Setup")
    print("=" * 40)
    
    # Check current database
    current_db = os.environ.get("DATABASE_URL", "sqlite:///toolora.db")
    print(f"Current database: {current_db}")
    
    if "postgresql" in current_db:
        print("✅ PostgreSQL already configured")
        if setup_postgresql_database():
            print("✅ PostgreSQL database is ready")
        else:
            print("❌ PostgreSQL setup failed")
    else:
        print("📝 Currently using SQLite")
        print("To upgrade to PostgreSQL:")
        print("1. Set DATABASE_URL environment variable")
        print("2. Run this script again")
        print("3. Restart the application")
    
    print("\n🔍 Current database stats:")
    try:
        sys.path.append('.')
        from app import app, db
        
        with app.app_context():
            from models import Tool, ToolCategory
            
            tool_count = Tool.query.count()
            category_count = ToolCategory.query.count()
            
            print(f"📊 Tools: {tool_count}")
            print(f"📊 Categories: {category_count}")
            print("✅ Database is healthy")
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    main()