#!/usr/bin/env python3
"""
Simple script to populate basic categories and tools
"""
from app import app, db
from models import ToolCategory, Tool

def create_basic_tools():
    """Create basic tools and categories"""
    
    with app.app_context():
        # Create PDF category
        pdf_cat = ToolCategory.query.filter_by(name='pdf').first()
        if not pdf_cat:
            pdf_cat = ToolCategory(
                name='pdf',
                display_name='PDF Toolkit',
                icon='file-text',
                description='Complete PDF processing toolkit',
                color='red',
                tool_count=3,
                sort_order=1
            )
            db.session.add(pdf_cat)
            db.session.flush()
        
        # Create Image category
        image_cat = ToolCategory.query.filter_by(name='image').first()
        if not image_cat:
            image_cat = ToolCategory(
                name='image',
                display_name='Image Toolkit',
                icon='image',
                description='Professional image editing tools',
                color='green',
                tool_count=3,
                sort_order=2
            )
            db.session.add(image_cat)
            db.session.flush()
        
        # Create Video category
        video_cat = ToolCategory.query.filter_by(name='video').first()
        if not video_cat:
            video_cat = ToolCategory(
                name='video',
                display_name='Video & Audio',
                icon='video',
                description='Video and audio processing tools',
                color='purple',
                tool_count=2,
                sort_order=3
            )
            db.session.add(video_cat)
            db.session.flush()
        
        # Basic tools
        basic_tools = [
            {
                'name': 'pdf-merge',
                'display_name': 'PDF Merge',
                'description': 'Combine multiple PDF files into one seamlessly',
                'category_id': pdf_cat.id,
                'icon': 'file-text',
                'features': ['Unlimited files', 'Preserve quality', 'Fast processing'],
                'file_types': ['.pdf']
            },
            {
                'name': 'pdf-split',
                'display_name': 'PDF Split',
                'description': 'Split large PDF files into smaller documents',
                'category_id': pdf_cat.id,
                'icon': 'file-text',
                'features': ['Split by pages', 'Custom ranges', 'Batch processing'],
                'file_types': ['.pdf']
            },
            {
                'name': 'pdf-compress',
                'display_name': 'PDF Compress',
                'description': 'Reduce PDF file size while maintaining quality',
                'category_id': pdf_cat.id,
                'icon': 'file-text',
                'features': ['Smart compression', 'Quality control', 'Fast processing'],
                'file_types': ['.pdf']
            },
            {
                'name': 'image-compress',
                'display_name': 'Image Compress',
                'description': 'Reduce image file size while maintaining visual quality',
                'category_id': image_cat.id,
                'icon': 'image',
                'features': ['Smart compression', 'Quality control', 'Batch processing'],
                'file_types': ['.jpg', '.jpeg', '.png', '.webp']
            },
            {
                'name': 'image-resize',
                'display_name': 'Image Resize',
                'description': 'Resize images to specific dimensions or percentages',
                'category_id': image_cat.id,
                'icon': 'image',
                'features': ['Custom dimensions', 'Aspect ratio', 'Multiple formats'],
                'file_types': ['.jpg', '.jpeg', '.png', '.webp']
            },
            {
                'name': 'image-convert',
                'display_name': 'Image Convert',
                'description': 'Convert images between different formats',
                'category_id': image_cat.id,
                'icon': 'image',
                'features': ['Multiple formats', 'Quality preserved', 'Fast conversion'],
                'file_types': ['.jpg', '.jpeg', '.png', '.webp', '.gif']
            },
            {
                'name': 'video-trim',
                'display_name': 'Video Trim',
                'description': 'Cut and trim video clips with precision timing',
                'category_id': video_cat.id,
                'icon': 'video',
                'features': ['Frame accuracy', 'Multiple formats', 'Quality preserved'],
                'file_types': ['.mp4', '.avi', '.mov', '.mkv']
            },
            {
                'name': 'video-to-mp3',
                'display_name': 'Video to MP3',
                'description': 'Extract audio from video files as MP3',
                'category_id': video_cat.id,
                'icon': 'video',
                'features': ['High quality audio', 'Multiple formats', 'Fast extraction'],
                'file_types': ['.mp4', '.avi', '.mov', '.mkv']
            }
        ]
        
        for tool_data in basic_tools:
            existing_tool = Tool.query.filter_by(name=tool_data['name']).first()
            if not existing_tool:
                tool = Tool(**tool_data)
                db.session.add(tool)
        
        db.session.commit()
        print(f"Successfully created {ToolCategory.query.count()} categories and {Tool.query.count()} tools!")

if __name__ == "__main__":
    create_basic_tools()