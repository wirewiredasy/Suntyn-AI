
#!/usr/bin/env python3
"""
Fresh database setup for Suntyn AI - Complete with all 85 tools
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
        
        total_tools = 0
        
        # Populate with all tool categories and tools
        for category_name, category_data in Config.TOOL_CATEGORIES.items():
            category = ToolCategory(
                name=category_name,
                display_name=category_data['name'],
                icon=category_data['icon'],
                color=category_data['color'],
                description=category_data['description'],
                tool_count=len(category_data['tools']),
                is_active=True,
                sort_order=list(Config.TOOL_CATEGORIES.keys()).index(category_name)
            )
            db.session.add(category)
            db.session.flush()  # Get category ID
            
            # Add all tools for this category
            for tool_name in category_data['tools']:
                display_name = tool_name.replace('-', ' ').replace('_', ' ').title()
                
                # Custom descriptions for better tools
                descriptions = {
                    'pdf-merge': 'Combine multiple PDF files into one seamlessly',
                    'pdf-split': 'Split large PDF files into smaller documents',
                    'image-compress': 'Reduce image file size while maintaining quality',
                    'image-resize': 'Resize images to any dimension quickly',
                    'video-to-mp3': 'Extract audio from video files as MP3',
                    'qr-generator': 'Generate QR codes for any text or URL',
                    'resume-generator': 'Create professional resumes with AI assistance',
                    'background-remover': 'Remove background from images automatically'
                }
                
                description = descriptions.get(tool_name, f'Professional {display_name.lower()} tool with advanced features')
                
                tool = Tool(
                    name=tool_name,
                    display_name=display_name,
                    description=description,
                    category_id=category.id,
                    icon=category_data['icon'],
                    is_active=True,
                    is_premium=False,
                    usage_count=0,
                    features=['High Quality', 'Fast Processing', 'No Registration Required'],
                    file_types=['*/*'],
                    max_file_size_mb=16
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
        
        # Show sample tools per category
        for category in categories:
            category_tools = Tool.query.filter_by(category_id=category.id).limit(3).all()
            tool_names = [t.display_name for t in category_tools]
            print(f'   {category.display_name}: {", ".join(tool_names)}...')

if __name__ == '__main__':
    setup_fresh_database()
