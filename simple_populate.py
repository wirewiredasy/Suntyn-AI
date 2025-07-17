#!/usr/bin/env python3
"""
Simple script to populate basic categories and tools
"""
from app import app, db
from models import ToolCategory, Tool

def create_basic_tools():
    """Create basic tools and categories"""

    with app.app_context():
        # Clear existing data
        Tool.query.delete()
        ToolCategory.query.delete()
        db.session.commit()

        # Create categories
        categories_data = [
            ('pdf', 'PDF Toolkit', 'file-text', 'red', 'Complete PDF processing toolkit'),
            ('image', 'Image Toolkit', 'image', 'green', 'Professional image editing tools'),
            ('video', 'Video & Audio', 'video', 'purple', 'Video and audio processing tools'),
            ('ai', 'AI Powered', 'cpu', 'blue', 'AI-powered content generation tools'),
            ('utility', 'Utility Tools', 'settings', 'gray', 'Essential utility tools'),
            ('govt', 'Government', 'shield', 'orange', 'Government document tools'),
            ('finance', 'Finance', 'dollar-sign', 'emerald', 'Financial calculation tools'),
            ('student', 'Student', 'book', 'pink', 'Educational and study tools')
        ]

        categories = {}
        for name, display_name, icon, color, description in categories_data:
            category = ToolCategory(
                name=name,
                display_name=display_name,
                icon=icon,
                color=color,
                description=description,
                tool_count=0,
                is_active=True,
                sort_order=len(categories)
            )
            db.session.add(category)
            categories[name] = category

        db.session.flush()

        # Create essential tools
        essential_tools = [
            ('pdf-merge', 'PDF Merge', 'Combine multiple PDF files into one', 'pdf'),
            ('pdf-split', 'PDF Split', 'Split PDF files into smaller documents', 'pdf'),
            ('pdf-compress', 'PDF Compress', 'Reduce PDF file size', 'pdf'),
            ('image-compress', 'Image Compress', 'Reduce image file size', 'image'),
            ('image-resize', 'Image Resize', 'Resize images to any dimension', 'image'),
            ('background-remover', 'Background Remover', 'Remove image backgrounds', 'image'),
            ('video-to-mp3', 'Video to MP3', 'Extract audio from videos', 'video'),
            ('video-trimmer', 'Video Trimmer', 'Cut and trim video clips', 'video'),
            ('qr-generator', 'QR Generator', 'Generate QR codes', 'utility'),
            ('password-generator', 'Password Generator', 'Generate secure passwords', 'utility'),
            ('resume-generator', 'Resume Generator', 'Create professional resumes', 'ai'),
            ('text-to-image', 'Text to Image', 'Generate images from text', 'ai')
        ]

        for tool_name, display_name, description, category_name in essential_tools:
            tool = Tool(
                name=tool_name,
                display_name=display_name,
                description=description,
                category_id=categories[category_name].id,
                icon=categories[category_name].icon,
                is_active=True,
                is_premium=False,
                usage_count=0,
                features=['High Quality', 'Fast Processing', 'Free'],
                file_types=['*/*'],
                max_file_size_mb=16
            )
            db.session.add(tool)

        db.session.commit()

        # Update tool counts
        for category in categories.values():
            category.tool_count = Tool.query.filter_by(category_id=category.id).count()

        db.session.commit()

        print(f"✅ Successfully created {ToolCategory.query.count()} categories and {Tool.query.count()} tools!")

if __name__ == "__main__":
    create_basic_tools()