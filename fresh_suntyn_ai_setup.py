
#!/usr/bin/env python3
"""
Fresh Suntyn AI Database Setup
Clean setup with Suntyn AI branding
"""
from app import app, db
from models import Tool, ToolCategory
from config import Config

def setup_fresh_suntyn_ai():
    """Setup fresh database with Suntyn AI branding"""
    
    with app.app_context():
        print("🚀 Setting up fresh Suntyn AI database...")
        
        # Clear all existing data
        Tool.query.delete()
        ToolCategory.query.delete()
        db.session.commit()
        print("✅ Cleared all old data")
        
        # Tool descriptions for Suntyn AI
        tool_descriptions = {
            # PDF Tools
            'pdf-merge': 'Merge multiple PDF files instantly with Suntyn AI',
            'pdf-split': 'Split PDF documents into separate pages',
            'pdf-compress': 'Compress PDF files while maintaining quality',
            'pdf-to-word': 'Convert PDF to editable Word documents',
            'word-to-pdf': 'Convert Word documents to PDF format',
            'pdf-to-jpg': 'Extract images from PDF files',
            'jpg-to-pdf': 'Convert images to PDF documents',
            'pdf-watermark': 'Add watermarks to PDF files',
            'pdf-annotator': 'Add notes and comments to PDFs',
            'pdf-page-numbers': 'Add page numbers to PDF documents',
            'pdf-unlock': 'Remove password protection from PDFs',
            'pdf-protect': 'Add password protection to PDFs',
            'pdf-rotate': 'Rotate PDF pages',
            'pdf-extract-pages': 'Extract specific pages from PDFs',
            'pdf-chat': 'Chat with your PDF using Suntyn AI',
            
            # Image Tools
            'image-compress': 'Compress images without quality loss',
            'image-resize': 'Resize images to any dimension',
            'image-convert': 'Convert between image formats',
            'image-crop': 'Crop images precisely',
            'background-remover': 'Remove backgrounds with AI',
            'image-enhancer': 'Enhance image quality using AI',
            'image-watermark': 'Add watermarks to images',
            'image-rotate': 'Rotate and flip images',
            'image-ocr': 'Extract text from images',
            'color-picker': 'Pick colors from images',
            'social-crop': 'Crop for social media platforms',
            'image-caption': 'Generate captions with AI',
            'profile-pic-maker': 'Create professional profile pictures',
            'meme-generator': 'Create memes easily',
            'text-to-image': 'Generate images from text',
            
            # Video Tools
            'video-to-mp3': 'Extract audio from videos',
            'audio-remover': 'Remove audio from videos',
            'video-trimmer': 'Trim and cut video clips',
            'voice-remover': 'Remove vocals from audio',
            'subtitle-generator': 'Auto-generate subtitles',
            'subtitle-merger': 'Add subtitles to videos',
            'video-compress': 'Compress videos efficiently',
            'video-converter': 'Convert video formats',
            'dubbing-tool': 'Add voice dubbing',
            'shorts-cropper': 'Create short-form videos',
            
            # AI Tools
            'resume-generator': 'Generate professional resumes with AI',
            'business-name-generator': 'Generate creative business names',
            'blog-title-generator': 'Create engaging blog titles',
            'product-description': 'Write product descriptions',
            'ad-copy-generator': 'Create advertising copy',
            'script-writer': 'Generate video scripts',
            'bio-generator': 'Create professional bios',
            'faq-generator': 'Generate FAQ sections',
            'idea-explainer': 'Explain ideas simply',
            'doc-to-slides': 'Convert documents to slides',
            
            # Utility Tools
            'text-case-converter': 'Convert text cases',
            'password-generator': 'Generate secure passwords',
            'qr-generator': 'Create QR codes instantly',
            'barcode-generator': 'Generate product barcodes',
            'url-shortener': 'Shorten long URLs',
            'clipboard-notepad': 'Online notepad tool',
            'age-bmi-calculator': 'Calculate age and BMI',
            'currency-converter': 'Convert currencies',
            'file-renamer': 'Batch rename files',
            'zip-unzip': 'Compress and extract files',
            
            # Government Tools
            'aadhaar-masker': 'Mask Aadhaar card details',
            'aadhaar-explainer': 'Understand Aadhaar features',
            'pan-form-filler': 'Fill PAN application forms',
            'ration-card-checker': 'Check ration card status',
            'govt-format-converter': 'Convert government documents',
            'legal-term-explainer': 'Explain legal terms',
            'rent-agreement-reader': 'Analyze rent agreements',
            'stamp-paper-splitter': 'Split stamp documents',
            'doc-translator': 'Translate documents',
            'govt-signature-extractor': 'Extract signatures',
            
            # Student Tools
            'notes-summarizer': 'Summarize study notes',
            'notes-to-mcq': 'Convert notes to questions',
            'chat-with-notes': 'Chat with study material',
            'handwriting-to-text': 'Convert handwriting to text',
            'mindmap-creator': 'Create mind maps',
            'flashcard-generator': 'Generate study flashcards',
            'timetable-generator': 'Create study schedules',
            'syllabus-extractor': 'Extract syllabus points',
            'whiteboard-saver': 'Save whiteboard content',
            
            # Finance Tools
            'budget-planner': 'Plan your budget smartly',
            'loan-emi-calculator': 'Calculate loan EMIs',
            'gst-calculator': 'Calculate GST amounts',
            'income-tax-estimator': 'Estimate income tax',
        }
        
        # Create categories for Suntyn AI
        categories = {}
        for cat_id, cat_data in Config.TOOL_CATEGORIES.items():
            category = ToolCategory(
                name=cat_id,
                display_name=f"Suntyn AI {cat_data['name']}",
                description=f"Suntyn AI powered {cat_data['name'].lower()}",
                icon=cat_data['icon'],
                color=cat_data['color']
            )
            db.session.add(category)
            categories[cat_id] = category
        
        db.session.commit()
        print(f"✅ Created {len(categories)} Suntyn AI categories")
        
        # Create all tools with Suntyn AI branding
        tools_created = 0
        for cat_id, cat_data in Config.TOOL_CATEGORIES.items():
            category = categories[cat_id]
            
            for tool_name in cat_data['tools']:
                tool = Tool(
                    name=tool_name,
                    display_name=tool_name.replace('-', ' ').title(),
                    description=tool_descriptions.get(tool_name, f"Suntyn AI {tool_name.replace('-', ' ')} tool"),
                    category_id=category.id,
                    icon=tool_name.replace('-', '_'),
                    color=cat_data['color'],
                    is_popular=tool_name in ['pdf-merge', 'image-compress', 'video-to-mp3', 'resume-generator', 'qr-generator'],
                    is_active=True
                )
                db.session.add(tool)
                tools_created += 1
        
        db.session.commit()
        
        print(f"\n🎉 Suntyn AI Database Setup Complete!")
        print(f"   Categories: {len(categories)}")
        print(f"   Tools: {tools_created}")
        print(f"   Popular Tools: {Tool.query.filter_by(is_popular=True).count()}")
        
        return True

if __name__ == "__main__":
    success = setup_fresh_suntyn_ai()
    if success:
        print("\n✅ Suntyn AI is ready to go!")
    else:
        print("\n❌ Setup failed!")
