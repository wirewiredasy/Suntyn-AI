#!/usr/bin/env python3
"""
Script to populate the database with all 85+ tools and categories
"""
from app import app, db
from models import ToolCategory, Tool
from config import Config

def populate_categories_and_tools():
    """Populate the database with categories and tools from config"""
    
    with app.app_context():
        sort_order = 0
        
        for category_id, category_data in Config.TOOL_CATEGORIES.items():
            # Check if category exists
            category = ToolCategory.query.filter_by(name=category_id).first()
            if not category:
                # Create category
                category = ToolCategory(
                    name=category_id,
                    display_name=category_data['name'],
                    icon=category_data['icon'],
                    description=category_data['description'],
                    color=category_data['color'],
                    tool_count=len(category_data['tools']),
                    sort_order=sort_order
                )
                db.session.add(category)
                db.session.flush()  # To get the category ID
            
            # Create tools for this category
            for tool_name in category_data['tools']:
                # Check if tool exists
                existing_tool = Tool.query.filter_by(name=tool_name).first()
                if not existing_tool:
                    tool_display_name = tool_name.replace('-', ' ').title()
                    
                    # Tool-specific descriptions and features
                    tool_configs = {
                        'pdf-merge': {
                            'description': 'Combine multiple PDF files into one seamlessly. Perfect for organizing documents and reports.',
                            'features': ['Unlimited files', 'Preserve quality', 'Fast processing'],
                            'file_types': ['.pdf']
                        },
                        'pdf-split': {
                            'description': 'Split large PDF files into smaller documents or individual pages with ease.',
                            'features': ['Split by pages', 'Custom ranges', 'Batch processing'],
                            'file_types': ['.pdf']
                        },
                        'image-compress': {
                            'description': 'Reduce image file size while maintaining visual quality using advanced compression.',
                            'features': ['Smart compression', 'Quality control', 'Batch processing'],
                            'file_types': ['.jpg', '.jpeg', '.png', '.webp']
                        },
                        'video-trimmer': {
                            'description': 'Cut and trim video clips with precision timing and frame accuracy.',
                            'features': ['Frame accuracy', 'Multiple formats', 'Quality preserved'],
                            'file_types': ['.mp4', '.avi', '.mov', '.mkv']
                        },
                        'resume-generator': {
                            'description': 'Create professional resumes with AI assistance and modern templates.',
                            'features': ['AI-powered', 'Professional templates', 'ATS-friendly'],
                            'file_types': ['text'],
                            'is_premium': False
                        }
                    }
                    
                    config = tool_configs.get(tool_name, {
                        'description': f'Professional {tool_display_name.lower()} tool for your creative and business needs.',
                        'features': ['Fast processing', 'High quality', 'Secure'],
                        'file_types': ['*/*']
                    })
                    
                    tool = Tool(
                        name=tool_name,
                        display_name=tool_display_name,
                        description=config['description'],
                        category_id=category.id,
                        icon=category_data['icon'],
                        features=config['features'],
                        file_types=config['file_types'],
                        is_premium=config.get('is_premium', False),
                        max_file_size_mb=config.get('max_file_size_mb', 16)
                    )
                    db.session.add(tool)
            
            sort_order += 1
        
        # Commit all changes
        db.session.commit()
        print(f"Successfully populated database with {ToolCategory.query.count()} categories and {Tool.query.count()} tools!")

if __name__ == "__main__":
    populate_categories_and_tools()