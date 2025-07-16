import os

class Config:
    # Firebase Configuration
    FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "AIzaSyBInx-JTjhFilUKR61lZLqj7o-UBv18BME")
    FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "tooloraai-eccee")
    FIREBASE_APP_ID = os.environ.get("FIREBASE_APP_ID", "1:258154771843:web:b08bdc010bdfa191a872b6")
    
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
