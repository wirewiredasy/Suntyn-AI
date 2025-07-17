
#!/usr/bin/env python3
"""
Initialize Suntyn AI Database
Run this script to set up the database using Flask models
"""
from app import app, db
from models import ToolCategory, Tool

def init_database():
    """Initialize database using Flask models"""
    
    with app.app_context():
        print("🚀 Initializing Suntyn AI database...")
        
        # Create all tables
        db.drop_all()
        db.create_all()
        print("✅ Created database tables")
        
        # Create categories
        categories_data = [
            {"name": "pdf", "display_name": "PDF Tools", "icon": "📄", "color": "#dc2626", "description": "Professional PDF processing tools"},
            {"name": "image", "display_name": "Image Tools", "icon": "🖼️", "color": "#059669", "description": "Advanced image editing and processing"},
            {"name": "video", "display_name": "Video Tools", "icon": "🎬", "color": "#7c3aed", "description": "Video editing and conversion tools"},
            {"name": "ai", "display_name": "AI Tools", "icon": "🤖", "color": "#2563eb", "description": "AI-powered productivity tools"},
            {"name": "utility", "display_name": "Utility Tools", "icon": "⚙️", "color": "#ea580c", "description": "Essential utility and productivity tools"},
            {"name": "student", "display_name": "Student Tools", "icon": "🎓", "color": "#0891b2", "description": "Educational and study tools"},
            {"name": "finance", "display_name": "Finance Tools", "icon": "💰", "color": "#16a34a", "description": "Financial calculators and tools"},
            {"name": "govt", "display_name": "Government Tools", "icon": "🏛️", "color": "#9333ea", "description": "Government document processing"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = ToolCategory(
                name=cat_data["name"],
                display_name=cat_data["display_name"],
                icon=cat_data["icon"],
                color=cat_data["color"],
                description=cat_data["description"],
                tool_count=0,
                is_active=True
            )
            db.session.add(category)
            categories[cat_data["name"]] = category
        
        db.session.flush()  # Get category IDs
        
        # Create tools
        tools_data = [
            # PDF Tools
            {"name": "pdf-merge", "display_name": "PDF Merge", "description": "Combine multiple PDF files into one seamlessly", "category": "pdf", "is_popular": True},
            {"name": "pdf-split", "display_name": "PDF Split", "description": "Split large PDF files into smaller documents", "category": "pdf"},
            {"name": "pdf-compress", "display_name": "PDF Compress", "description": "Reduce PDF file size while maintaining quality", "category": "pdf"},
            {"name": "pdf-to-word", "display_name": "PDF to Word", "description": "Convert PDF documents to editable Word files", "category": "pdf"},
            
            # Image Tools
            {"name": "image-compress", "display_name": "Image Compress", "description": "Reduce image file size while maintaining quality", "category": "image", "is_popular": True},
            {"name": "image-resize", "display_name": "Image Resize", "description": "Resize images to any dimension quickly", "category": "image"},
            {"name": "background-remover", "display_name": "Background Remover", "description": "Remove background from images automatically", "category": "image", "is_popular": True},
            {"name": "image-convert", "display_name": "Image Convert", "description": "Convert images between different formats", "category": "image"},
            
            # Video Tools
            {"name": "video-to-mp3", "display_name": "Video to MP3", "description": "Extract audio from video files as MP3", "category": "video", "is_popular": True},
            {"name": "video-trimmer", "display_name": "Video Trimmer", "description": "Cut and trim video clips with precision", "category": "video"},
            {"name": "video-compress", "display_name": "Video Compress", "description": "Reduce video file size efficiently", "category": "video"},
            
            # AI Tools
            {"name": "resume-generator", "display_name": "Resume Generator", "description": "Create professional resumes with AI assistance", "category": "ai", "is_popular": True},
            {"name": "blog-title-generator", "display_name": "Blog Title Generator", "description": "Generate catchy blog titles using AI", "category": "ai"},
            {"name": "business-name-generator", "display_name": "Business Name Generator", "description": "Generate unique business names with AI", "category": "ai"},
            
            # Utility Tools
            {"name": "qr-generator", "display_name": "QR Generator", "description": "Generate QR codes for any text or URL", "category": "utility", "is_popular": True},
            {"name": "password-generator", "display_name": "Password Generator", "description": "Generate secure passwords", "category": "utility"},
            {"name": "text-case-converter", "display_name": "Text Case Converter", "description": "Convert text between different cases", "category": "utility"},
            
            # Student Tools
            {"name": "notes-summarizer", "display_name": "Notes Summarizer", "description": "Summarize study notes automatically", "category": "student"},
            {"name": "flashcard-generator", "display_name": "Flashcard Generator", "description": "Create study flashcards from text", "category": "student"},
            
            # Finance Tools
            {"name": "loan-emi-calculator", "display_name": "EMI Calculator", "description": "Calculate loan EMI and interest", "category": "finance"},
            {"name": "currency-converter", "display_name": "Currency Converter", "description": "Convert between different currencies", "category": "finance"},
            
            # Government Tools
            {"name": "aadhaar-masker", "display_name": "Aadhaar Masker", "description": "Mask sensitive Aadhaar information", "category": "govt"},
            {"name": "pan-form-filler", "display_name": "PAN Form Filler", "description": "Auto-fill PAN application forms", "category": "govt"}
        ]
        
        for tool_data in tools_data:
            category = categories[tool_data["category"]]
            tool = Tool(
                name=tool_data["name"],
                display_name=tool_data["display_name"],
                description=tool_data["description"],
                category_id=category.id,
                icon=category.icon,
                color=category.color,
                is_active=True,
                is_popular=tool_data.get("is_popular", False),
                features=["High Quality", "Fast Processing", "No Registration Required"],
                file_types=["*/*"],
                max_file_size_mb=16
            )
            db.session.add(tool)
        
        db.session.commit()
        
        # Update tool counts
        for category in categories.values():
            tool_count = Tool.query.filter_by(category_id=category.id).count()
            category.tool_count = tool_count
        
        db.session.commit()
        
        print(f"✅ Database initialized successfully!")
        print(f"📊 Created {len(categories_data)} categories and {len(tools_data)} tools")
        return True

if __name__ == "__main__":
    init_database()
