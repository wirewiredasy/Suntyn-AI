#!/usr/bin/env python3
"""
Complete script to restore all 85+ tools across 8 categories
This will restore the exact tools you specified without duplicates
"""

import sqlite3
from datetime import datetime

def restore_all_tools():
    """Restore all tools from the user's specification"""
    
    conn = sqlite3.connect('instance/toolora.db')
    cursor = conn.cursor()
    
    # Get category IDs
    cursor.execute('SELECT id, name FROM tool_categories')
    category_map = {name: id for id, name in cursor.fetchall()}
    
    # Complete tools specification based on user's requirements
    all_tools = {
        'pdf': [
            ('pdf-merge', 'Merge PDF', 'Combine multiple PDFs into one', 'file-text'),
            ('pdf-split', 'Split PDF', 'Break a PDF into multiple files', 'scissors'),
            ('pdf-compress', 'Compress PDF', 'Reduce file size without quality loss', 'archive'),
            ('pdf-to-word', 'PDF to Word', 'Convert PDF into editable DOCX', 'file-text'),
            ('word-to-pdf', 'Word to PDF', 'Convert Word to PDF', 'file-text'),
            ('pdf-to-jpg', 'PDF to JPG', 'Convert PDF pages to images', 'image'),
            ('jpg-to-pdf', 'JPG to PDF', 'Convert image files to PDF', 'image'),
            ('pdf-watermark', 'Add Watermark', 'Insert watermark in PDF', 'shield'),
            ('pdf-page-numbers', 'Add Page Numbers', 'Auto-number PDF pages', 'hash'),
            ('pdf-unlock', 'Unlock PDF', 'Remove password protection', 'unlock'),
            ('pdf-protect', 'Protect PDF', 'Add password to PDF', 'lock'),
            ('pdf-rotate', 'Rotate PDF', 'Rotate pages of PDF', 'rotate-cw'),
            ('pdf-extract-pages', 'Extract PDF Pages', 'Select & export certain pages', 'file-minus'),
            ('pdf-chat', 'Chat with PDF (AI)', 'Ask questions from a PDF (local)', 'message-circle'),
            ('pdf-summarize', 'Summarize PDF (AI)', 'Get auto-summary of uploaded PDF', 'file-text')
        ],
        'image': [
            ('image-compress', 'Compress Image', 'Reduce size without quality drop', 'minimize-2'),
            ('image-resize', 'Resize Image', 'Set dimensions manually', 'maximize-2'),
            ('image-convert', 'Convert Format', 'JPG ↔ PNG ↔ WEBP etc.', 'refresh-cw'),
            ('image-crop', 'Crop Tool', 'Free crop/Fixed aspect ratios', 'crop'),
            ('image-rotate', 'Flip/Rotate Image', 'Orientation adjustment', 'rotate-cw'),
            ('image-ocr', 'Image to Text (OCR)', 'Extract text from image', 'type'),
            ('background-remover', 'Background Remover', 'Remove bg using AI', 'scissors'),
            ('meme-generator', 'Meme Generator', 'Add text to image easily', 'smile'),
            ('image-watermark', 'Add Watermark', 'Overlay logo/text', 'shield'),
            ('signature-extractor', 'Signature Extractor', 'Extract signature from doc/photo', 'edit-3'),
            ('image-enhancer', 'Image Enhancer (AI)', 'Upscale low-quality images', 'zap'),
            ('color-picker', 'Color Picker', 'Pick HEX/RGB from image', 'dropper'),
            ('social-crop', 'Social Crop Tool', 'Insta/Facebook/YouTube sizes', 'crop'),
            ('image-caption', 'Image Caption Generator', 'AI suggests alt text/captions', 'message-square'),
            ('profile-pic-maker', 'AI Profile Pic Maker', 'Convert selfie to pro avatar style', 'user-circle')
        ],
        'video': [
            ('video-to-mp3', 'Video to MP3', 'Extract audio', 'music'),
            ('audio-remover', 'Audio Remover', 'Remove audio track', 'volume-x'),
            ('video-trimmer', 'Video Trimmer', 'Cut selected time', 'scissors'),
            ('voice-remover', 'Voice Remover', 'AI stem splitter', 'mic-off'),
            ('subtitle-generator', 'Subtitle Generator', 'Auto transcribe (offline AI)', 'subtitles'),
            ('subtitle-merger', 'Subtitle Merger', 'Add subtitle to video', 'plus-circle'),
            ('video-compress', 'Compress Video', 'Reduce size (FFmpeg)', 'minimize-2'),
            ('video-converter', 'Format Converter', 'MP4 ↔ AVI ↔ MOV etc.', 'refresh-cw'),
            ('dubbing-tool', 'Dubbing Tool', 'AI text-to-speech dubbing', 'mic'),
            ('shorts-cropper', 'Shorts/Story Cropper', 'Auto-resize for vertical formats', 'crop')
        ],
        'govt': [
            ('pan-form-filler', 'PAN Form Filler', 'Auto-filled PAN card form', 'file-text'),
            ('aadhaar-explainer', 'Aadhaar Explainer', 'Read & explain Aadhaar PDF', 'info'),
            ('rent-agreement-reader', 'Rent Agreement Reader', 'Smart parsing tool', 'home'),
            ('ration-card-checker', 'Ration Card Checker', 'Detect errors in image/PDF', 'check-circle'),
            ('doc-translator', 'Doc Translator', 'Hindi ↔ English ↔ Assamese', 'globe'),
            ('legal-term-explainer', 'Legal Term Explainer', 'AI converts complex terms', 'book-open'),
            ('govt-signature-extractor', 'Signature Extractor', 'Only sign cut-out', 'edit-3'),
            ('stamp-paper-splitter', 'Stamp Paper Splitter', 'Divide multi-purpose papers', 'scissors'),
            ('aadhaar-masker', 'Aadhaar Masker', 'Mask personal info for KYC', 'eye-off'),
            ('govt-format-converter', 'Govt Format Converter', 'JPEG to 200 DPI PDF (Upload Format)', 'refresh-cw')
        ],
        'student': [
            ('handwriting-to-text', 'Handwriting to Text', 'OCR handwritten notes', 'edit-3'),
            ('notes-summarizer', 'Notes Summarizer', 'Shorten long notes', 'file-minus'),
            ('flashcard-generator', 'Flashcard Generator', 'Q/A style cards', 'layers'),
            ('mindmap-creator', 'Mindmap Creator', 'Auto-structured visual map', 'git-branch'),
            ('chat-with-notes', 'Chat with Notes', 'Ask doubt from file', 'message-circle'),
            ('notes-to-mcq', 'Notes to MCQ', 'AI converts text to quiz', 'help-circle'),
            ('timetable-generator', 'Timetable Generator', 'Weekly study schedule', 'calendar'),
            ('pdf-annotator', 'PDF Annotator', 'Highlight & comment tool', 'edit-2'),
            ('whiteboard-saver', 'Whiteboard Saver', 'Convert board photo to clean notes', 'camera'),
            ('syllabus-extractor', 'Syllabus Extractor', 'Detect units from syllabus file', 'book')
        ],
        'finance': [
            ('loan-emi-calculator', 'Loan EMI Calculator', 'Calculate monthly EMI payments', 'calculator'),
            ('gst-calculator', 'GST Calculator', 'Calculate GST for Indian businesses', 'percent'),
            ('currency-converter', 'Currency Converter', 'Convert between currencies', 'dollar-sign'),
            ('budget-planner', 'Budget Planner', 'Plan and track expenses', 'pie-chart'),
            ('income-tax-estimator', 'Income Tax Estimator', 'Estimate Indian income tax', 'receipt')
        ],
        'utility': [
            ('qr-generator', 'QR Generator', 'Generate QR codes', 'qr-code'),
            ('barcode-generator', 'Barcode Generator', 'Generate barcodes', 'scan'),
            ('text-case-converter', 'Text Case Converter', 'Convert text case', 'type'),
            ('age-bmi-calculator', 'Age BMI Calculator', 'Calculate age and BMI', 'activity'),
            ('password-generator', 'Password Generator', 'Generate secure passwords', 'key'),
            ('clipboard-notepad', 'Clipboard Notepad', 'Online notepad tool', 'clipboard'),
            ('file-renamer', 'File Renamer', 'Batch rename files', 'edit'),
            ('url-shortener', 'URL Shortener', 'Shorten long URLs', 'link'),
            ('text-to-image', 'Text to Image', 'Convert text to image', 'image'),
            ('zip-unzip', 'ZIP/UnZIP', 'Compress and extract files', 'archive')
        ],
        'ai': [
            ('resume-generator', 'Resume Generator', 'Generate professional resume', 'user'),
            ('business-name-generator', 'Business Name Generator', 'Generate business names', 'briefcase'),
            ('blog-title-generator', 'Blog Title Generator', 'Generate catchy blog titles', 'edit-3'),
            ('product-description', 'Product Description', 'Generate product descriptions', 'package'),
            ('script-writer', 'Script Writer', 'AI script writing tool', 'file-text'),
            ('ad-copy-generator', 'Ad Copy Generator', 'Generate advertising copy', 'megaphone'),
            ('faq-generator', 'FAQ Generator', 'Generate FAQ sections', 'help-circle'),
            ('idea-explainer', 'Idea Explainer', 'Explain complex ideas simply', 'lightbulb'),
            ('bio-generator', 'Bio Generator', 'Generate professional bios', 'user-check'),
            ('doc-to-slides', 'Doc to Slides', 'Convert documents to slides', 'presentation')
        ]
    }
    
    # Insert all tools
    tools_added = 0
    for category_name, tools in all_tools.items():
        if category_name in category_map:
            category_id = category_map[category_name]
            for tool_name, display_name, description, icon in tools:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO tools 
                        (name, display_name, description, category_id, icon, is_active, created_at)
                        VALUES (?, ?, ?, ?, ?, 1, ?)
                    ''', (tool_name, display_name, description, category_id, icon, datetime.utcnow()))
                    
                    if cursor.rowcount > 0:
                        tools_added += 1
                        print(f'Added: {display_name} ({tool_name})')
                except Exception as e:
                    print(f'Error adding {tool_name}: {e}')
    
    # Update category tool counts
    cursor.execute('''
        UPDATE tool_categories 
        SET tool_count = (
            SELECT COUNT(*) FROM tools 
            WHERE tools.category_id = tool_categories.id
        )
    ''')
    
    conn.commit()
    
    # Final verification
    cursor.execute('''
        SELECT tc.display_name, COUNT(t.id) as tool_count 
        FROM tool_categories tc 
        LEFT JOIN tools t ON tc.id = t.category_id 
        GROUP BY tc.id 
        ORDER BY tc.sort_order
    ''')
    
    print(f'\n=== Tools Restoration Complete ===')
    print(f'Total tools added: {tools_added}')
    print('\n=== Final Category Status ===')
    for category, count in cursor.fetchall():
        print(f'{category}: {count} tools')
    
    conn.close()
    return tools_added

if __name__ == '__main__':
    restore_all_tools()