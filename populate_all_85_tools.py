#!/usr/bin/env python3
"""
Complete script to populate all 85 tools across 8 categories
"""
from app import app, db
from models import ToolCategory, Tool
from config import Config

def populate_all_tools():
    """Populate all 85 tools from config"""
    
    with app.app_context():
        # First clear existing data
        Tool.query.delete()
        ToolCategory.query.delete()
        db.session.commit()
        
        # Create all categories
        categories = {}
        for cat_name, cat_data in Config.TOOL_CATEGORIES.items():
            category = ToolCategory(
                name=cat_name,
                display_name=cat_data['name'],
                icon=cat_data['icon'],
                description=cat_data['description'],
                color=cat_data['color'],
                tool_count=len(cat_data['tools']),
                is_active=True,
                sort_order=list(Config.TOOL_CATEGORIES.keys()).index(cat_name) + 1
            )
            db.session.add(category)
            db.session.flush()
            categories[cat_name] = category
            print(f"Created category: {cat_data['name']} with {len(cat_data['tools'])} tools")
        
        # Create all tools
        total_tools = 0
        for cat_name, cat_data in Config.TOOL_CATEGORIES.items():
            category = categories[cat_name]
            
            for tool_name in cat_data['tools']:
                # Generate display name from tool name
                display_name = tool_name.replace('-', ' ').replace('_', ' ').title()
                
                # Generate description
                description = f"Professional {display_name.lower()} tool for {cat_data['description'].lower()}"
                
                # Determine file types based on category
                file_types = []
                if cat_name == 'pdf':
                    file_types = ['.pdf']
                elif cat_name == 'image':
                    file_types = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
                elif cat_name == 'video':
                    file_types = ['.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav']
                elif cat_name == 'govt':
                    file_types = ['.pdf', '.jpg', '.png']
                elif cat_name == 'student':
                    file_types = ['.pdf', '.txt', '.docx', '.jpg', '.png']
                elif cat_name == 'finance':
                    file_types = ['.pdf', '.csv', '.xlsx']
                elif cat_name == 'utility':
                    file_types = ['.txt', '.pdf', '.jpg', '.png']
                elif cat_name == 'ai':
                    file_types = ['.txt', '.pdf', '.docx']
                
                # Generate features based on tool type
                features = [
                    'Fast processing',
                    'High quality output', 
                    'Secure processing',
                    'No registration required'
                ]
                
                tool = Tool(
                    name=tool_name,
                    display_name=display_name,
                    description=description,
                    category_id=category.id,
                    icon=cat_data['icon'],
                    is_active=True,
                    is_premium=False,
                    usage_count=0,
                    features=features,
                    file_types=file_types,
                    max_file_size_mb=16
                )
                
                db.session.add(tool)
                total_tools += 1
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Successfully created {len(categories)} categories and {total_tools} tools!")
        print(f"🎉 All {total_tools} tools are now available in Toolora AI!")
        
        # Verify counts
        for cat_name, category in categories.items():
            tool_count = Tool.query.filter_by(category_id=category.id).count()
            print(f"   {category.display_name}: {tool_count} tools")

if __name__ == '__main__':
    populate_all_tools()