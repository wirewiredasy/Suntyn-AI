#!/usr/bin/env python3
"""
Simple Tool Restoration - Fix Database with Correct Schema
"""

import logging
from app import app, db
from models import Tool, ToolCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simple_restore_all_tools():
    """Simple restore all tools with correct schema"""
    
    with app.app_context():
        logger.info("🔧 Simple Tool Restoration...")
        
        # Clear existing data
        Tool.query.delete()
        ToolCategory.query.delete()
        db.session.commit()
        
        # Get Tool model attributes to know what fields exist
        tool_columns = [column.name for column in Tool.__table__.columns]
        logger.info(f"Tool model columns: {tool_columns}")
        
        # Simple categories with tools 
        categories_data = [
            {
                'name': 'PDF Toolkit',
                'display_name': 'PDF Tools', 
                'description': 'Professional PDF tools',
                'icon': 'file-text',
                'color': 'red',
                'tools': [
                    ('PDF Merge', 'Combine multiple PDF files into one'),
                    ('PDF Split', 'Split PDF into separate pages'),
                    ('PDF Compress', 'Reduce PDF file size'),
                    ('PDF to Word', 'Convert PDF to Word documents'),
                    ('Word to PDF', 'Convert Word to PDF format'),
                    ('PDF to Excel', 'Extract tables to Excel'),
                    ('Excel to PDF', 'Convert Excel to PDF'),
                    ('PDF Password Remove', 'Remove PDF passwords'),
                    ('PDF Password Add', 'Add password protection'),
                    ('PDF Rotate', 'Rotate PDF pages'),
                    ('PDF Watermark', 'Add watermarks to PDF'),
                    ('PDF OCR', 'Extract text from scanned PDFs'),
                    ('PDF Page Delete', 'Remove specific pages'),
                    ('PDF to PowerPoint', 'Convert to PPT'),
                    ('PowerPoint to PDF', 'Convert PPT to PDF')
                ]
            },
            {
                'name': 'Image Toolkit',
                'display_name': 'Image Tools',
                'description': 'Professional image editing tools',
                'icon': 'image',
                'color': 'green',
                'tools': [
                    ('Image Compressor', 'Reduce image file size'),
                    ('Image Resizer', 'Resize images to dimensions'),
                    ('Image Crop', 'Crop images precisely'),
                    ('Image Rotate', 'Rotate images correctly'),
                    ('Image Flip', 'Flip images horizontally/vertically'),
                    ('Image Converter', 'Convert image formats'),
                    ('Background Remover', 'Remove image backgrounds'),
                    ('Image Enhancer', 'Enhance image quality'),
                    ('Image Blur', 'Apply blur effects'),
                    ('Brightness Adjuster', 'Adjust brightness/contrast'),
                    ('Grayscale Converter', 'Convert to black & white'),
                    ('Sepia Effect', 'Apply vintage sepia tone'),
                    ('Image Watermark', 'Add protective watermarks'),
                    ('Image Border', 'Add decorative borders'),
                    ('Favicon Generator', 'Create website favicons')
                ]
            },
            {
                'name': 'Video & Audio',
                'display_name': 'Video & Audio',
                'description': 'Video and audio processing',
                'icon': 'video',
                'color': 'purple',
                'tools': [
                    ('Video to MP3', 'Extract audio from videos'),
                    ('Video to GIF', 'Convert videos to GIFs'),
                    ('Video Compressor', 'Reduce video file size'),
                    ('Video Trimmer', 'Cut and trim videos'),
                    ('Video Merger', 'Combine multiple videos'),
                    ('Audio Converter', 'Convert audio formats'),
                    ('Audio Trimmer', 'Cut and edit audio'),
                    ('Audio Merger', 'Combine audio files'),
                    ('Volume Adjuster', 'Adjust audio levels'),
                    ('Audio Compressor', 'Reduce audio size'),
                    ('YouTube Thumbnail', 'Download video thumbnails')
                ]
            },
            {
                'name': 'AI Tools',
                'display_name': 'AI Tools',
                'description': 'AI-powered content generation',
                'icon': 'brain',
                'color': 'indigo',
                'tools': [
                    ('AI Resume Generator', 'Create professional resumes'),
                    ('Business Name Generator', 'Generate business names'),
                    ('Blog Title Generator', 'Create engaging titles'),
                    ('Meta Description Generator', 'Generate SEO descriptions'),
                    ('Product Description Generator', 'Create product descriptions'),
                    ('Ad Copy Generator', 'Generate advertising copy'),
                    ('FAQ Generator', 'Create FAQ sections'),
                    ('Email Template Generator', 'Design email templates'),
                    ('Social Media Caption', 'Generate social captions'),
                    ('Content Rewriter', 'Rewrite content effectively')
                ]
            },
            {
                'name': 'Government Documents',
                'display_name': 'Government',
                'description': 'Indian government services',
                'icon': 'shield',
                'color': 'blue',
                'tools': [
                    ('Aadhar Download', 'Download Aadhar card'),
                    ('PAN Verification', 'Verify PAN details'),
                    ('Voter ID Download', 'Download voter ID'),
                    ('Passport Status', 'Check passport status'),
                    ('Driving License Download', 'Download license'),
                    ('Ration Card Download', 'Download ration card'),
                    ('Income Certificate', 'Apply for certificate'),
                    ('Domicile Certificate', 'Apply for domicile'),
                    ('Caste Certificate', 'Apply for caste certificate'),
                    ('Birth Certificate', 'Download birth certificate')
                ]
            },
            {
                'name': 'Student Tools',
                'display_name': 'Student Tools',
                'description': 'Educational tools for students',
                'icon': 'graduation-cap',
                'color': 'yellow',
                'tools': [
                    ('GPA Calculator', 'Calculate Grade Point Average'),
                    ('CGPA Calculator', 'Calculate Cumulative GPA'),
                    ('Percentage Calculator', 'Convert grades to percentage'),
                    ('Study Planner', 'Plan study schedule'),
                    ('Assignment Tracker', 'Track assignment deadlines'),
                    ('Note Organizer', 'Organize study notes'),
                    ('Exam Timer', 'Practice with timed exams'),
                    ('Citation Generator', 'Generate academic citations'),
                    ('Research Helper', 'Assist with research'),
                    ('Essay Checker', 'Check essays for errors')
                ]
            },
            {
                'name': 'Finance Tools',
                'display_name': 'Finance',
                'description': 'Financial calculators',
                'icon': 'dollar-sign',
                'color': 'emerald',
                'tools': [
                    ('EMI Calculator', 'Calculate loan EMI'),
                    ('SIP Calculator', 'Calculate SIP returns'),
                    ('Tax Calculator', 'Calculate income tax'),
                    ('FD Calculator', 'Calculate FD returns'),
                    ('Loan Calculator', 'Calculate loan details')
                ]
            },
            {
                'name': 'Utility Tools',
                'display_name': 'Utilities',
                'description': 'Essential utility tools',
                'icon': 'tool',
                'color': 'gray',
                'tools': [
                    ('QR Code Generator', 'Generate QR codes'),
                    ('Barcode Generator', 'Generate barcodes'),
                    ('Password Generator', 'Generate secure passwords'),
                    ('Hash Generator', 'Generate MD5, SHA hashes'),
                    ('Base64 Encoder', 'Encode/decode Base64'),
                    ('URL Shortener', 'Create short URLs'),
                    ('Color Picker', 'Pick and convert colors'),
                    ('JSON Formatter', 'Format and validate JSON'),
                    ('XML Formatter', 'Format and validate XML'),
                    ('Lorem Ipsum Generator', 'Generate placeholder text')
                ]
            }
        ]
        
        total_tools = 0
        
        # Create categories and tools
        for cat_data in categories_data:
            # Create category
            category = ToolCategory(
                name=cat_data['name'],
                display_name=cat_data['display_name'],
                description=cat_data['description'],
                icon=cat_data['icon'],
                color=cat_data['color'],
                tool_count=len(cat_data['tools']),
                is_active=True,
                sort_order=0
            )
            db.session.add(category)
            db.session.flush()
            
            # Create tools for this category
            for tool_name, tool_description in cat_data['tools']:
                # Create tool with all required fields
                tool_data = {
                    'name': tool_name,
                    'display_name': tool_name,  # Required field
                    'description': tool_description,
                    'category_id': category.id,
                    'icon': 'tool',
                    'is_active': True
                }
                
                # Add optional fields if they exist in the model
                if 'usage_count' in tool_columns:
                    tool_data['usage_count'] = 0
                if 'difficulty_level' in tool_columns:
                    tool_data['difficulty_level'] = 'easy'
                if 'processing_time' in tool_columns:
                    tool_data['processing_time'] = 'fast'
                if 'file_formats' in tool_columns:
                    tool_data['file_formats'] = 'multiple'
                if 'max_file_size' in tool_columns:
                    tool_data['max_file_size'] = '16MB'
                
                tool = Tool(**tool_data)
                db.session.add(tool)
                total_tools += 1
            
            logger.info(f"✅ Created '{cat_data['name']}' with {len(cat_data['tools'])} tools")
        
        # Commit all changes
        db.session.commit()
        
        # Verify count
        db_tools = Tool.query.count()
        db_categories = ToolCategory.query.count()
        
        logger.info(f"🎉 Successfully restored {db_tools} tools across {db_categories} categories!")
        
        return db_tools

if __name__ == "__main__":
    count = simple_restore_all_tools()
    print(f"✅ Database restored with {count} tools!")
    print("🚀 All 85+ tools are now available!")