
#!/usr/bin/env python3
"""
Fresh database setup for Suntyn AI - Local SQLite
"""
import os
from app import app, db
from config import Config

def setup_fresh_database():
    """Create fresh local database with all 85 tools"""
    print('🚀 Setting up fresh local database for Suntyn AI...')
    
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        print('🗑️ Cleared existing database')
        
        # Create all tables fresh
        db.create_all()
        print('📋 Created fresh database tables')
        
        # Import models
        from models import ToolCategory, Tool
        
        # Clear any existing data
        db.session.query(Tool).delete()
        db.session.query(ToolCategory).delete()
        db.session.commit()
        
        total_tools = 0
        
        # Populate with all tool categories and tools
        for category_name, category_data in Config.TOOL_CATEGORIES.items():
            category = ToolCategory(
                name=category_data['name'],
                icon=category_data['icon'],
                color=category_data['color'],
                description=category_data['description']
            )
            db.session.add(category)
            db.session.flush()  # Get category ID
            
            # Add all tools for this category
            for tool_name in category_data['tools']:
                display_name = tool_name.replace('-', ' ').replace('_', ' ').title()
                tool = Tool(
                    name=display_name,
                    slug=tool_name,
                    description=f'Professional {display_name.lower()} tool with advanced features',
                    category_id=category.id
                )
                db.session.add(tool)
                total_tools += 1
        
        db.session.commit()
        print(f'✅ Successfully added {total_tools} tools across {len(Config.TOOL_CATEGORIES)} categories')
        print('🎉 Fresh Suntyn AI database setup complete!')
        
        # Verify database
        categories = ToolCategory.query.all()
        tools = Tool.query.all()
        print(f'📊 Database contains: {len(categories)} categories, {len(tools)} tools')

if __name__ == '__main__':
    setup_fresh_database()
