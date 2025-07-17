import os

class Config:
    # Clean configuration - no external services

    # Tool Categories Configuration
    TOOL_CATEGORIES = {
        'pdf': {
            'name': 'PDF Toolkit',
            'icon': 'file-text',
            'color': 'red',
            'description': 'Complete PDF processing toolkit',
            'tools': [
                'pdf-merge', 'pdf-split', 'pdf-compress', 'pdf-to-word',
                'word-to-pdf', 'pdf-to-jpg', 'jpg-to-pdf', 'pdf-watermark',
                'pdf-page-numbers', 'pdf-unlock', 'pdf-protect', 'pdf-rotate',
                'pdf-extract-pages', 'pdf-chat', 'pdf-summarize'
            ]
        },
        'image': {
            'name': 'Image Toolkit',
            'icon': 'image',
            'color': 'green',
            'description': 'Professional image editing tools',
            'tools': [
                'image-compress', 'image-resize', 'image-convert', 'image-crop',
                'image-rotate', 'image-ocr', 'background-remover', 'meme-generator',
                'image-watermark', 'signature-extractor', 'image-enhancer',
                'color-picker', 'social-crop', 'image-caption', 'profile-pic-maker'
            ]
        },
        'video': {
            'name': 'Video & Audio',
            'icon': 'video',
            'color': 'purple',
            'description': 'Video and audio processing tools',
            'tools': [
                'video-to-mp3', 'audio-remover', 'video-trimmer', 'voice-remover',
                'subtitle-generator', 'subtitle-merger', 'video-compress',
                'video-converter', 'dubbing-tool', 'shorts-cropper'
            ]
        },
        'govt': {
            'name': 'Govt Documents',
            'icon': 'shield',
            'color': 'orange',
            'description': 'India-specific government document tools',
            'tools': [
                'pan-form-filler', 'aadhaar-explainer', 'rent-agreement-reader',
                'ration-card-checker', 'doc-translator', 'legal-term-explainer',
                'govt-signature-extractor', 'stamp-paper-splitter', 'aadhaar-masker',
                'govt-format-converter'
            ]
        },
        'student': {
            'name': 'Student Toolkit',
            'icon': 'graduation-cap',
            'color': 'blue',
            'description': 'Educational tools for students',
            'tools': [
                'handwriting-to-text', 'notes-summarizer', 'flashcard-generator',
                'mindmap-creator', 'chat-with-notes', 'notes-to-mcq',
                'timetable-generator', 'pdf-annotator', 'whiteboard-saver',
                'syllabus-extractor'
            ]
        },
        'finance': {
            'name': 'Finance Toolkit',
            'icon': 'calculator',
            'color': 'emerald',
            'description': 'Financial calculation tools',
            'tools': [
                'loan-emi-calculator', 'gst-calculator', 'currency-converter',
                'budget-planner', 'income-tax-estimator'
            ]
        },
        'utility': {
            'name': 'Utility Tools',
            'icon': 'settings',
            'color': 'slate',
            'description': 'General purpose utility tools',
            'tools': [
                'qr-generator', 'barcode-generator', 'text-case-converter',
                'age-bmi-calculator', 'password-generator', 'clipboard-notepad',
                'file-renamer', 'url-shortener', 'text-to-image', 'zip-unzip'
            ]
        },
        'ai': {
            'name': 'AI Tools',
            'icon': 'brain',
            'color': 'violet',
            'description': 'Smart AI-powered tools',
            'tools': [
                'resume-generator', 'business-name-generator', 'blog-title-generator',
                'product-description', 'script-writer', 'ad-copy-generator',
                'faq-generator', 'idea-explainer', 'bio-generator', 'doc-to-slides'
            ]
        }
    }

    basedir = os.path.abspath(os.path.dirname(__file__))
    database_url = os.environ.get('DATABASE_URL')

    # Database Configuration - Suntyn AI
    if database_url and 'postgresql' in database_url:
        SQLALCHEMY_DATABASE_URI = database_url
        print("🗄️ Using PostgreSQL database for Suntyn AI")
    else:
        # Local SQLite database for Suntyn AI
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance", "suntyn_ai.db")}'
        print("🚀 Using Fresh Suntyn AI Local Database")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'suntyn-ai-secret-key-2024'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size