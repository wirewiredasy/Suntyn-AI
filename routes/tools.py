from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import Tool, ToolCategory, db
import logging
import os
from config import Config

# Custom icon mapping for all tools
TOOL_CUSTOM_ICONS = {
    # PDF Tools
    'pdf-merge': 'layers', 'pdf-split': 'scissors', 'pdf-compress': 'archive',
    'pdf-to-word': 'file-text', 'pdf-to-jpg': 'image', 'word-to-pdf': 'file-pdf',
    'jpg-to-pdf': 'file-image', 'pdf-watermark': 'droplets', 'pdf-annotator': 'edit-3',
    'pdf-page-numbers': 'hash', 'pdf-unlock': 'unlock', 'pdf-protect': 'lock',
    'pdf-rotate': 'rotate-cw', 'pdf-extract-pages': 'file-minus', 'pdf-chat': 'message-circle',
    'pdf-summarize': 'file-text',

    # Image Tools
    'image-compress': 'minimize-2', 'image-resize': 'maximize-2', 'image-convert': 'repeat',
    'image-crop': 'crop', 'background-remover': 'eraser', 'image-enhancer': 'sun',
    'image-watermark': 'droplets', 'image-rotate': 'rotate-cw', 'image-ocr': 'eye',
    'color-picker': 'palette', 'social-crop': 'smartphone', 'image-caption': 'type',
    'profile-pic-maker': 'user-circle', 'meme-generator': 'smile', 'text-to-image': 'image',

    # Video Tools
    'video-to-mp3': 'music', 'audio-remover': 'volume-x', 'video-trimmer': 'scissors',
    'voice-remover': 'mic-off', 'subtitle-generator': 'subtitles', 'subtitle-merger': 'video',
    'video-compress': 'minimize', 'video-converter': 'repeat', 'dubbing-tool': 'mic',
    'shorts-cropper': 'smartphone',

    # AI Tools
    'resume-generator': 'briefcase', 'business-name-generator': 'building', 
    'blog-title-generator': 'pen-tool', 'product-description': 'package',
    'ad-copy-generator': 'megaphone', 'script-writer': 'film', 'bio-generator': 'user',
    'faq-generator': 'help-circle', 'idea-explainer': 'lightbulb', 'notes-summarizer': 'file-text',
    'notes-to-mcq': 'list', 'chat-with-notes': 'message-square', 'doc-translator': 'globe',
    'mindmap-creator': 'git-branch', 'handwriting-to-text': 'edit',

    # Text Tools
    'text-case-converter': 'type', 'password-generator': 'key', 'qr-generator': 'qr-code',
    'barcode-generator': 'scan', 'url-shortener': 'link', 'clipboard-notepad': 'clipboard',
    'signature-extractor': 'pen-tool', 'whiteboard-saver': 'save',

    # Utility Tools
    'file-renamer': 'edit-2', 'zip-unzip': 'package', 'currency-converter': 'dollar-sign',
    'age-bmi-calculator': 'calculator', 'budget-planner': 'pie-chart', 'loan-emi-calculator': 'credit-card',
    'gst-calculator': 'percent', 'income-tax-estimator': 'trending-up', 'flashcard-generator': 'book',
    'timetable-generator': 'calendar', 'doc-to-slides': 'presentation', 'syllabus-extractor': 'bookmark',

    # Government Tools
    'aadhaar-masker': 'eye-off', 'aadhaar-explainer': 'info', 'pan-form-filler': 'file-plus',
    'ration-card-checker': 'check-circle', 'govt-format-converter': 'refresh-cw',
    'legal-term-explainer': 'scale', 'rent-agreement-reader': 'home', 'stamp-paper-splitter': 'divide'
}

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tools_bp.route('/')
def index():
    """Tools index page with category filtering"""
    try:
        from config import Config
        category = request.args.get('category', 'all')
        search_query = request.args.get('search', '')

        # Get all tools from database OR fallback to config
        try:
            tools_query = Tool.query.filter_by(is_active=True)
            
            # Filter by category if specified
            if category and category != 'all':
                tools_query = tools_query.join(ToolCategory).filter(ToolCategory.name == category)

            if search_query:
                tools_query = tools_query.filter(
                    Tool.display_name.ilike(f'%{search_query}%') |
                    Tool.description.ilike(f'%{search_query}%')
                )

            tools = tools_query.all()
            categories = ToolCategory.query.all()
            
            # If no tools found, use fallback
            if not tools:
                raise Exception("No tools in database, using fallback")
                
        except Exception as db_error:
            logger.warning(f"Database error, using fallback: {db_error}")
            # Fallback to config-based tools
            tools = []
            categories = []
            
            # Create tool objects from config
            for cat_id, cat_data in Config.TOOL_CATEGORIES.items():
                for tool_name in cat_data['tools']:
                    if category == 'all' or category == cat_id:
                        if not search_query or search_query.lower() in tool_name.lower():
                            # Create a mock tool object
                            tool_obj = type('Tool', (), {
                                'name': tool_name,
                                'display_name': tool_name.replace('-', ' ').title(),
                                'description': f"Professional {tool_name.replace('-', ' ')} tool",
                                'category': type('Category', (), {'name': cat_id})(),
                                'icon': TOOL_CUSTOM_ICONS.get(tool_name, 'tool'),
                                'color': cat_data['color'],
                                'is_popular': tool_name in ['pdf-merge', 'image-compress', 'qr-generator', 'resume-generator']
                            })
                            tools.append(tool_obj)
                
                # Create category object
                if category == 'all' or category == cat_id:
                    cat_obj = type('Category', (), {
                        'name': cat_id,
                        'display_name': cat_data['name']
                    })()
                    if cat_obj not in [c for c in categories if hasattr(c, 'name') and c.name == cat_id]:
                        categories.append(cat_obj)

        logger.info(f"Loading tools index: found {len(tools)} tools")

        return render_template('tools/index.html', 
                             tools=tools, 
                             categories=categories, 
                             selected_category=category,
                             search_query=search_query,
                             tool_icons=TOOL_CUSTOM_ICONS)
    except Exception as e:
        logger.error(f"Error loading tools index: {e}")
        # Final fallback with essential tools
        essential_tools = []
        for tool_name in ['pdf-merge', 'pdf-split', 'image-compress', 'image-resize', 'video-to-mp3', 'qr-generator']:
            tool_obj = type('Tool', (), {
                'name': tool_name,
                'display_name': tool_name.replace('-', ' ').title(),
                'description': f"Professional {tool_name.replace('-', ' ')} tool",
                'category': type('Category', (), {'name': 'utility'})(),
                'icon': TOOL_CUSTOM_ICONS.get(tool_name, 'tool'),
                'color': 'blue',
                'is_popular': True
            })
            essential_tools.append(tool_obj)
            
        return render_template('tools/index.html', 
                             tools=essential_tools, 
                             categories=[], 
                             selected_category='all',
                             search_query='',
                             tool_icons=TOOL_CUSTOM_ICONS)

@tools_bp.route('/api/tools')
def api_tools():
    """API endpoint to get all tools data"""
    try:
        tools = Tool.query.filter_by(is_active=True).all()

        tools_data = []
        for tool in tools:
            tools_data.append({
                'name': tool.name,
                'display_name': tool.display_name,
                'description': tool.description,
                'category': tool.category.name if tool.category else 'utility',
                'icon': tool.icon or 'tool',
                'color': tool.color or 'blue',
                'is_popular': tool.is_popular
            })

        logger.info(f"API returning {len(tools_data)} tools")

        return jsonify({
            'success': True,
            'tools': tools_data,
            'count': len(tools_data)
        })

    except Exception as e:
        logger.error(f"Error in API tools endpoint: {e}")

        # Return fallback tools data
        fallback_tools = [
            {'name': 'pdf-merge', 'display_name': 'PDF Merge', 'category': 'pdf', 'icon': 'file-text', 'color': 'red'},
            {'name': 'image-compress', 'display_name': 'Image Compress', 'category': 'image', 'icon': 'image', 'color': 'green'},
            {'name': 'video-to-mp3', 'display_name': 'Video to MP3', 'category': 'video', 'icon': 'music', 'color': 'purple'},
            {'name': 'qr-generator', 'display_name': 'QR Generator', 'category': 'utility', 'icon': 'qr-code', 'color': 'gray'}
        ]

        return jsonify({
            'success': True,
            'tools': fallback_tools,
            'count': len(fallback_tools),
            'fallback': True
        })

@tools_bp.route('/<tool_name>')
def tool_page(tool_name):
    """Individual tool page"""
    try:
        tool = Tool.query.filter_by(name=tool_name, is_active=True).first()

        if not tool:
            logger.warning(f"Tool not found: {tool_name}")
            return redirect(url_for('tools.index'))

        logger.info(f"Loading tool page: {tool_name}")

        # Try to load specific template, fallback to generic
        try:
            return render_template(f'tools/{tool_name}.html', 
                                 tool=tool,
                                 # No authentication required
                                 firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                                 firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
        except:
            logger.info(f"Using generic template for: {tool_name}")
            return render_template('tools/generic_tool.html', 
                                 tool_name=tool_name, 
                                 tool_info=tool,
                                 # No authentication required
                                 firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                                 firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

    except Exception as e:
        logger.error(f"Error loading tool page {tool_name}: {e}")
        return redirect(url_for('tools.index'))