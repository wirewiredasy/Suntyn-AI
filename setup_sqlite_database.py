
#!/usr/bin/env python3
"""
SQLite Database Setup for Suntyn AI
Creates a fresh local database with categories and tools
"""
import sqlite3
import os
from pathlib import Path

def setup_sqlite_database():
    """Create SQLite database with categories and tools"""
    
    # Ensure instance directory exists
    instance_dir = Path("instance")
    instance_dir.mkdir(exist_ok=True)
    
    # Connect to SQLite database
    db_path = instance_dir / "suntyn_ai.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print("🚀 Setting up Suntyn AI SQLite database...")
    
    # Step 1: Drop old tables (if any)
    cursor.execute("DROP TABLE IF EXISTS tools")
    cursor.execute("DROP TABLE IF EXISTS tool_categories")
    
    # Step 2: Create categories table
    cursor.execute("""
    CREATE TABLE tool_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL,
        icon TEXT,
        color TEXT DEFAULT '#6366f1',
        description TEXT,
        tool_count INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        sort_order INTEGER DEFAULT 0
    )
    """)
    
    # Step 3: Create tools table
    cursor.execute("""
    CREATE TABLE tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL,
        description TEXT,
        category_id INTEGER,
        icon TEXT,
        color TEXT DEFAULT '#6366f1',
        is_active INTEGER DEFAULT 1,
        is_premium INTEGER DEFAULT 0,
        is_popular INTEGER DEFAULT 0,
        usage_count INTEGER DEFAULT 0,
        features TEXT,
        file_types TEXT,
        max_file_size_mb INTEGER DEFAULT 16,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(category_id) REFERENCES tool_categories(id)
    )
    """)
    
    # Step 4: Insert categories
    categories = [
        ("pdf", "PDF Tools", "📄", "#dc2626", "Professional PDF processing tools", 15),
        ("image", "Image Tools", "🖼️", "#059669", "Advanced image editing and processing", 15),
        ("video", "Video Tools", "🎬", "#7c3aed", "Video editing and conversion tools", 10),
        ("ai", "AI Tools", "🤖", "#2563eb", "AI-powered productivity tools", 10),
        ("utility", "Utility Tools", "⚙️", "#ea580c", "Essential utility and productivity tools", 10),
        ("student", "Student Tools", "🎓", "#0891b2", "Educational and study tools", 10),
        ("finance", "Finance Tools", "💰", "#16a34a", "Financial calculators and tools", 5),
        ("govt", "Government Tools", "🏛️", "#9333ea", "Government document processing", 10)
    ]
    
    cursor.executemany("""
    INSERT INTO tool_categories (name, display_name, icon, color, description, tool_count)
    VALUES (?, ?, ?, ?, ?, ?)
    """, categories)
    
    # Step 5: Insert sample tools (you can expand this list to 85)
    tools = [
        # PDF Tools
        ("pdf-merge", "PDF Merge", "Combine multiple PDF files into one seamlessly", 1, "📄", "#dc2626", 1, 0, 1),
        ("pdf-split", "PDF Split", "Split large PDF files into smaller documents", 1, "📄", "#dc2626", 1, 0, 0),
        ("pdf-compress", "PDF Compress", "Reduce PDF file size while maintaining quality", 1, "📄", "#dc2626", 1, 0, 0),
        ("pdf-to-word", "PDF to Word", "Convert PDF documents to editable Word files", 1, "📄", "#dc2626", 1, 0, 0),
        
        # Image Tools
        ("image-compress", "Image Compress", "Reduce image file size while maintaining quality", 2, "🖼️", "#059669", 1, 0, 1),
        ("image-resize", "Image Resize", "Resize images to any dimension quickly", 2, "🖼️", "#059669", 1, 0, 0),
        ("background-remover", "Background Remover", "Remove background from images automatically", 2, "🖼️", "#059669", 1, 0, 1),
        ("image-convert", "Image Convert", "Convert images between different formats", 2, "🖼️", "#059669", 1, 0, 0),
        
        # Video Tools
        ("video-to-mp3", "Video to MP3", "Extract audio from video files as MP3", 3, "🎬", "#7c3aed", 1, 0, 1),
        ("video-trimmer", "Video Trimmer", "Cut and trim video clips with precision", 3, "🎬", "#7c3aed", 1, 0, 0),
        ("video-compress", "Video Compress", "Reduce video file size efficiently", 3, "🎬", "#7c3aed", 1, 0, 0),
        
        # AI Tools
        ("resume-generator", "Resume Generator", "Create professional resumes with AI assistance", 4, "🤖", "#2563eb", 1, 0, 1),
        ("blog-title-generator", "Blog Title Generator", "Generate catchy blog titles using AI", 4, "🤖", "#2563eb", 1, 0, 0),
        ("business-name-generator", "Business Name Generator", "Generate unique business names with AI", 4, "🤖", "#2563eb", 1, 0, 0),
        
        # Utility Tools
        ("qr-generator", "QR Generator", "Generate QR codes for any text or URL", 5, "⚙️", "#ea580c", 1, 0, 1),
        ("password-generator", "Password Generator", "Generate secure passwords", 5, "⚙️", "#ea580c", 1, 0, 0),
        ("text-case-converter", "Text Case Converter", "Convert text between different cases", 5, "⚙️", "#ea580c", 1, 0, 0),
        
        # Student Tools
        ("notes-summarizer", "Notes Summarizer", "Summarize study notes automatically", 6, "🎓", "#0891b2", 1, 0, 0),
        ("flashcard-generator", "Flashcard Generator", "Create study flashcards from text", 6, "🎓", "#0891b2", 1, 0, 0),
        
        # Finance Tools
        ("loan-emi-calculator", "EMI Calculator", "Calculate loan EMI and interest", 7, "💰", "#16a34a", 1, 0, 0),
        ("currency-converter", "Currency Converter", "Convert between different currencies", 7, "💰", "#16a34a", 1, 0, 0),
        
        # Government Tools
        ("aadhaar-masker", "Aadhaar Masker", "Mask sensitive Aadhaar information", 8, "🏛️", "#9333ea", 1, 0, 0),
        ("pan-form-filler", "PAN Form Filler", "Auto-fill PAN application forms", 8, "🏛️", "#9333ea", 1, 0, 0)
    ]
    
    cursor.executemany("""
    INSERT INTO tools (name, display_name, description, category_id, icon, color, is_active, is_premium, is_popular)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tools)
    
    # Commit changes
    conn.commit()
    
    # Verify setup
    cursor.execute("SELECT COUNT(*) FROM tool_categories")
    category_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tools")
    tool_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ Database setup complete!")
    print(f"📊 Created {category_count} categories and {tool_count} tools")
    print(f"🗄️ Database location: {db_path}")
    
    return True

if __name__ == "__main__":
    setup_sqlite_database()
