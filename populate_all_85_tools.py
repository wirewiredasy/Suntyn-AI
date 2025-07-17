
#!/usr/bin/env python3
"""
Complete database population with all 85 tools
"""
from app import app, db
from models import Tool, ToolCategory
from config import Config

def populate_database():
    with app.app_context():
        print("🚀 Starting complete database population...")
        
        # Clear existing data
        Tool.query.delete()
        ToolCategory.query.delete()
        db.session.commit()
        print("✅ Cleared existing data")
        
        # Create categories
        categories = {}
        for cat_id, cat_data in Config.TOOL_CATEGORIES.items():
            category = ToolCategory(
                name=cat_id,
                display_name=cat_data['name'],
                description=f"Tools for {cat_data['name'].lower()}",
                icon=cat_data['icon'],
                color=cat_data['color']
            )
            db.session.add(category)
            categories[cat_id] = category
        
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Tool descriptions
        tool_descriptions = {
            # PDF Tools
            'pdf-merge': 'Combine multiple PDF files into a single document quickly and easily',
            'pdf-split': 'Split large PDF files into smaller, manageable documents',
            'pdf-compress': 'Reduce PDF file size while maintaining quality',
            'pdf-to-word': 'Convert PDF documents to editable Word files',
            'word-to-pdf': 'Convert Word documents to PDF format',
            'pdf-to-jpg': 'Extract images from PDF or convert PDF pages to JPG',
            'jpg-to-pdf': 'Convert JPG images to PDF documents',
            'pdf-watermark': 'Add watermarks to PDF documents for protection',
            'pdf-annotator': 'Add comments, highlights, and annotations to PDFs',
            'pdf-page-numbers': 'Add page numbers to PDF documents',
            'pdf-unlock': 'Remove password protection from PDF files',
            'pdf-protect': 'Add password protection to PDF documents',
            'pdf-rotate': 'Rotate PDF pages to correct orientation',
            'pdf-extract-pages': 'Extract specific pages from PDF documents',
            'pdf-chat': 'Chat with your PDF documents using AI',
            'pdf-summarize': 'Generate summaries of PDF content',
            
            # Image Tools
            'image-compress': 'Reduce image file size while maintaining quality',
            'image-resize': 'Resize images to specific dimensions',
            'image-convert': 'Convert between different image formats',
            'image-crop': 'Crop images to focus on important areas',
            'background-remover': 'Remove backgrounds from images automatically',
            'image-enhancer': 'Enhance image quality using AI',
            'image-watermark': 'Add watermarks to protect your images',
            'image-rotate': 'Rotate images to correct orientation',
            'image-ocr': 'Extract text from images using OCR',
            'color-picker': 'Pick colors from images and get color codes',
            'social-crop': 'Crop images for social media platforms',
            'image-caption': 'Generate captions for images using AI',
            'profile-pic-maker': 'Create professional profile pictures',
            'meme-generator': 'Create memes with custom text and images',
            'text-to-image': 'Generate images from text descriptions',
            
            # Video Tools
            'video-to-mp3': 'Extract audio from video files as MP3',
            'audio-remover': 'Remove audio track from video files',
            'video-trimmer': 'Trim and cut video clips to desired length',
            'voice-remover': 'Remove vocals from audio files',
            'subtitle-generator': 'Generate subtitles for videos automatically',
            'subtitle-merger': 'Add subtitle files to video content',
            'video-compress': 'Reduce video file size efficiently',
            'video-converter': 'Convert videos between different formats',
            'dubbing-tool': 'Add voice dubbing to video content',
            'shorts-cropper': 'Crop videos for short-form content',
            
            # AI Tools
            'resume-generator': 'Generate professional resumes using AI',
            'business-name-generator': 'Generate creative business names',
            'blog-title-generator': 'Create catchy blog titles and headlines',
            'product-description': 'Generate product descriptions for e-commerce',
            'ad-copy-generator': 'Create compelling advertising copy',
            'script-writer': 'Generate scripts for videos and presentations',
            'bio-generator': 'Create professional bios for social media',
            'faq-generator': 'Generate FAQ sections for websites',
            'idea-explainer': 'Explain complex ideas in simple terms',
            'doc-to-slides': 'Convert documents to presentation slides',
            
            # Utility Tools
            'text-case-converter': 'Convert text between different cases',
            'password-generator': 'Generate strong, secure passwords',
            'qr-generator': 'Create QR codes for URLs, text, and data',
            'barcode-generator': 'Generate barcodes for products',
            'url-shortener': 'Shorten long URLs for sharing',
            'clipboard-notepad': 'Online notepad for quick notes',
            'age-bmi-calculator': 'Calculate age and BMI easily',
            'currency-converter': 'Convert between different currencies',
            'file-renamer': 'Batch rename multiple files',
            'zip-unzip': 'Compress and extract ZIP files',
            'text-to-image': 'Convert text to stylized images',
            
            # Government Tools
            'aadhaar-masker': 'Mask sensitive Aadhaar card information',
            'aadhaar-explainer': 'Understand Aadhaar card details',
            'pan-form-filler': 'Fill PAN card application forms',
            'ration-card-checker': 'Check ration card status and details',
            'govt-format-converter': 'Convert government document formats',
            'legal-term-explainer': 'Explain legal terms in simple language',
            'rent-agreement-reader': 'Analyze rent agreement documents',
            'stamp-paper-splitter': 'Split stamp paper documents',
            'doc-translator': 'Translate government documents',
            'govt-signature-extractor': 'Extract signatures from documents',
            
            # Student Tools
            'notes-summarizer': 'Summarize study notes and documents',
            'notes-to-mcq': 'Convert notes to multiple choice questions',
            'chat-with-notes': 'Chat with your study notes using AI',
            'handwriting-to-text': 'Convert handwritten notes to digital text',
            'mindmap-creator': 'Create mind maps from text content',
            'flashcard-generator': 'Generate flashcards for studying',
            'timetable-generator': 'Create study timetables and schedules',
            'syllabus-extractor': 'Extract key points from syllabus',
            'whiteboard-saver': 'Save and organize whiteboard content',
            
            # Finance Tools
            'budget-planner': 'Plan and track your budget effectively',
            'loan-emi-calculator': 'Calculate loan EMIs and interest',
            'gst-calculator': 'Calculate GST for business transactions',
            'income-tax-estimator': 'Estimate income tax liability',
        }
        
        # Create all tools
        tools_created = 0
        for cat_id, cat_data in Config.TOOL_CATEGORIES.items():
            category = categories[cat_id]
            
            for tool_name in cat_data['tools']:
                tool = Tool(
                    name=tool_name,
                    display_name=tool_name.replace('-', ' ').title(),
                    description=tool_descriptions.get(tool_name, f"Professional {tool_name.replace('-', ' ')} tool"),
                    category_id=category.id,
                    icon=tool_name.replace('-', '_'),
                    color=cat_data['color'],
                    is_popular=tool_name in ['pdf-merge', 'image-compress', 'video-to-mp3', 'resume-generator', 'qr-generator', 'background-remover'],
                    is_active=True
                )
                db.session.add(tool)
                tools_created += 1
        
        db.session.commit()
        
        print(f"✅ Created {tools_created} tools successfully!")
        print("\n📊 Database Population Summary:")
        print(f"   Categories: {len(categories)}")
        print(f"   Tools: {tools_created}")
        print(f"   Popular Tools: {Tool.query.filter_by(is_popular=True).count()}")
        
        return True

if __name__ == "__main__":
    success = populate_database()
    if success:
        print("\n🎉 Database population completed successfully!")
    else:
        print("\n❌ Database population failed!")
