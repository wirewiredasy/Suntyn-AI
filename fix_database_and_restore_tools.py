#!/usr/bin/env python3
"""
Fix Database Schema and Restore All 85+ Tools
Fix the database model issues and populate with all tools
"""

import logging
from app import app, db
from models import Tool, ToolCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_and_restore_all_tools():
    """Fix database and restore all 85+ tools"""
    
    with app.app_context():
        logger.info("🔧 Fixing Database Schema and Restoring All Tools...")
        
        # Drop and recreate all tables to fix schema issues
        db.drop_all()
        db.create_all()
        
        # Complete tool catalog with all 85+ tools
        categories_data = [
            {
                'name': 'PDF Toolkit',
                'display_name': 'PDF Tools',
                'description': 'Professional PDF tools for all your document needs',
                'icon': 'file-text',
                'color': 'red',
                'tools': [
                    ('pdf-merge', 'PDF Merge', 'Combine multiple PDF files into one document'),
                    ('pdf-split', 'PDF Split', 'Split PDF into separate pages or ranges'),
                    ('pdf-compress', 'PDF Compress', 'Reduce PDF file size while maintaining quality'),
                    ('pdf-to-word', 'PDF to Word', 'Convert PDF documents to editable Word files'),
                    ('word-to-pdf', 'Word to PDF', 'Convert Word documents to PDF format'),
                    ('pdf-to-excel', 'PDF to Excel', 'Extract tables from PDF to Excel spreadsheets'),
                    ('excel-to-pdf', 'Excel to PDF', 'Convert Excel files to PDF documents'),
                    ('pdf-to-ppt', 'PDF to PowerPoint', 'Convert PDF to PowerPoint presentations'),
                    ('ppt-to-pdf', 'PowerPoint to PDF', 'Convert PowerPoint to PDF format'),
                    ('pdf-password-remove', 'Remove PDF Password', 'Remove password protection from PDFs'),
                    ('pdf-password-add', 'Add PDF Password', 'Add password protection to PDF files'),
                    ('pdf-rotate', 'Rotate PDF', 'Rotate PDF pages to correct orientation'),
                    ('pdf-watermark', 'PDF Watermark', 'Add watermarks to PDF documents'),
                    ('pdf-page-delete', 'Delete PDF Pages', 'Remove specific pages from PDF'),
                    ('pdf-ocr', 'PDF OCR', 'Extract text from scanned PDF documents')
                ]
            },
            {
                'name': 'Image Toolkit',
                'display_name': 'Image Tools',
                'description': 'Professional image editing and conversion tools',
                'icon': 'image',
                'color': 'green',
                'tools': [
                    ('image-compress', 'Image Compressor', 'Reduce image file size without quality loss'),
                    ('image-resize', 'Image Resizer', 'Resize images to specific dimensions'),
                    ('image-crop', 'Image Crop', 'Crop images to focus on important areas'),
                    ('image-rotate', 'Image Rotate', 'Rotate images to correct orientation'),
                    ('image-flip', 'Image Flip', 'Flip images horizontally or vertically'),
                    ('image-format-converter', 'Image Converter', 'Convert between image formats (JPG, PNG, WebP)'),
                    ('background-remover', 'Background Remover', 'Remove backgrounds from images automatically'),
                    ('image-enhancer', 'Image Enhancer', 'Enhance image quality and sharpness'),
                    ('image-blur', 'Image Blur', 'Apply blur effects to images'),
                    ('image-brightness', 'Brightness Adjuster', 'Adjust image brightness and contrast'),
                    ('image-grayscale', 'Grayscale Converter', 'Convert images to black and white'),
                    ('image-sepia', 'Sepia Effect', 'Apply vintage sepia tone to images'),
                    ('image-watermark', 'Image Watermark', 'Add watermarks to protect images'),
                    ('image-border', 'Add Image Border', 'Add decorative borders to images'),
                    ('favicon-generator', 'Favicon Generator', 'Create favicons for websites')
                ]
            },
            {
                'name': 'Video & Audio',
                'display_name': 'Video & Audio',
                'description': 'Professional video and audio processing tools',
                'icon': 'video',
                'color': 'purple',
                'tools': [
                    ('video-to-mp3', 'Video to MP3', 'Extract audio from video files'),
                    ('video-to-gif', 'Video to GIF', 'Convert video clips to animated GIFs'),
                    ('video-compressor', 'Video Compressor', 'Reduce video file size'),
                    ('video-trimmer', 'Video Trimmer', 'Cut and trim video clips'),
                    ('video-merger', 'Video Merger', 'Combine multiple videos into one'),
                    ('audio-converter', 'Audio Converter', 'Convert between audio formats'),
                    ('audio-trimmer', 'Audio Trimmer', 'Cut and edit audio files'),
                    ('audio-merger', 'Audio Merger', 'Combine multiple audio files'),
                    ('volume-adjuster', 'Volume Adjuster', 'Adjust audio volume levels'),
                    ('audio-compressor', 'Audio Compressor', 'Reduce audio file size'),
                    ('youtube-thumbnail', 'YouTube Thumbnail Downloader', 'Download video thumbnails')
                ]
            },
            {
                'name': 'AI Tools',
                'display_name': 'AI Tools',
                'description': 'AI-powered content generation and automation tools',
                'icon': 'brain',
                'color': 'indigo',
                'tools': [
                    ('resume-generator', 'AI Resume Generator', 'Create professional resumes with AI'),
                    ('business-name-generator', 'Business Name Generator', 'Generate creative business names'),
                    ('blog-title-generator', 'Blog Title Generator', 'Create engaging blog titles'),
                    ('meta-description-generator', 'Meta Description Generator', 'Generate SEO meta descriptions'),
                    ('product-description-generator', 'Product Description Generator', 'Create compelling product descriptions'),
                    ('ad-copy-generator', 'Ad Copy Generator', 'Generate effective advertising copy'),
                    ('faq-generator', 'FAQ Generator', 'Create comprehensive FAQ sections'),
                    ('email-template-generator', 'Email Template Generator', 'Design professional email templates'),
                    ('social-media-caption', 'Social Media Caption', 'Generate engaging social media captions'),
                    ('content-rewriter', 'Content Rewriter', 'Rewrite content for better readability')
                ]
            },
            {
                'name': 'Government Documents',
                'display_name': 'Government',
                'description': 'Indian government document tools and services',
                'icon': 'shield',
                'color': 'blue',
                'tools': [
                    ('aadhar-download', 'Aadhar Download', 'Download Aadhar card from UIDAI portal'),
                    ('pan-verification', 'PAN Verification', 'Verify PAN card details'),
                    ('voter-id-download', 'Voter ID Download', 'Download voter ID card'),
                    ('passport-status', 'Passport Status', 'Check passport application status'),
                    ('driving-license-download', 'Driving License Download', 'Download driving license'),
                    ('ration-card-download', 'Ration Card Download', 'Download ration card'),
                    ('income-certificate', 'Income Certificate', 'Apply for income certificate'),
                    ('domicile-certificate', 'Domicile Certificate', 'Apply for domicile certificate'),
                    ('caste-certificate', 'Caste Certificate', 'Apply for caste certificate'),
                    ('birth-certificate', 'Birth Certificate', 'Download birth certificate')
                ]
            },
            {
                'name': 'Student Tools',
                'display_name': 'Student Tools',
                'description': 'Educational tools for students and learners',
                'icon': 'graduation-cap',
                'color': 'yellow',
                'tools': [
                    ('gpa-calculator', 'GPA Calculator', 'Calculate Grade Point Average'),
                    ('cgpa-calculator', 'CGPA Calculator', 'Calculate Cumulative GPA'),
                    ('percentage-calculator', 'Percentage Calculator', 'Convert grades to percentage'),
                    ('study-planner', 'Study Planner', 'Plan your study schedule'),
                    ('assignment-tracker', 'Assignment Tracker', 'Track assignment deadlines'),
                    ('note-organizer', 'Note Organizer', 'Organize study notes'),
                    ('exam-timer', 'Exam Timer', 'Practice with timed exams'),
                    ('citation-generator', 'Citation Generator', 'Generate academic citations'),
                    ('research-helper', 'Research Helper', 'Assist with research projects'),
                    ('essay-checker', 'Essay Checker', 'Check essays for errors')
                ]
            },
            {
                'name': 'Finance Tools',
                'display_name': 'Finance',
                'description': 'Financial calculators and planning tools',
                'icon': 'dollar-sign',
                'color': 'emerald',
                'tools': [
                    ('emi-calculator', 'EMI Calculator', 'Calculate loan EMI amounts'),
                    ('sip-calculator', 'SIP Calculator', 'Calculate SIP investment returns'),
                    ('tax-calculator', 'Tax Calculator', 'Calculate income tax'),
                    ('fd-calculator', 'FD Calculator', 'Calculate fixed deposit returns'),
                    ('loan-calculator', 'Loan Calculator', 'Calculate loan details')
                ]
            },
            {
                'name': 'Utility Tools',
                'display_name': 'Utilities',
                'description': 'Essential utility tools for everyday tasks',
                'icon': 'tool',
                'color': 'gray',
                'tools': [
                    ('qr-generator', 'QR Code Generator', 'Generate QR codes for text, URLs'),
                    ('barcode-generator', 'Barcode Generator', 'Generate various types of barcodes'),
                    ('password-generator', 'Password Generator', 'Generate secure passwords'),
                    ('hash-generator', 'Hash Generator', 'Generate MD5, SHA1, SHA256 hashes'),
                    ('base64-encoder', 'Base64 Encoder/Decoder', 'Encode and decode Base64'),
                    ('url-shortener', 'URL Shortener', 'Create short URLs'),
                    ('color-picker', 'Color Picker', 'Pick and convert colors'),
                    ('json-formatter', 'JSON Formatter', 'Format and validate JSON'),
                    ('xml-formatter', 'XML Formatter', 'Format and validate XML'),
                    ('lorem-ipsum', 'Lorem Ipsum Generator', 'Generate placeholder text')
                ]
            }
        ]
        
        total_tools = 0
        
        # Create categories and tools
        for cat_data in categories_data:
            # Create category with all required fields
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
            for tool_slug, tool_name, tool_description in cat_data['tools']:
                tool = Tool(
                    name=tool_name,
                    slug=tool_slug,
                    description=tool_description,
                    category_id=category.id,
                    icon='tool',
                    is_active=True,
                    usage_count=0,
                    difficulty_level='easy',
                    processing_time='fast',
                    file_formats='multiple',
                    max_file_size='16MB'
                )
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
    count = fix_and_restore_all_tools()
    print(f"✅ Database fixed and restored with {count} tools!")
    print("🚀 All 85+ tools are now available in database!")