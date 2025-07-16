from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from config import Config
from models import Tool, ToolCategory
import os

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

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/')
def index():
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '')

    # Get tools from database
    tools_query = Tool.query.filter_by(is_active=True)
    
    if category != 'all':
        # Filter by category
        category_obj = ToolCategory.query.filter_by(name=category).first()
        if category_obj:
            tools_query = tools_query.filter_by(category_id=category_obj.id)
    
    if search_query:
        # Search in tool names and descriptions
        tools_query = tools_query.filter(
            Tool.display_name.ilike(f'%{search_query}%') |
            Tool.description.ilike(f'%{search_query}%')
        )
    
    tools = tools_query.all()
    
    # Get all categories
    all_categories = ToolCategory.query.filter_by(is_active=True).all()
    
    print(f"DEBUG: Found {len(tools)} tools")  # Debug line
    for tool in tools[:3]:
        print(f"DEBUG: Tool {tool.name} - {tool.display_name}")  # Debug line
        print(f"DEBUG: Tool category: {tool.category.name if tool.category else 'None'}")  # Debug line
    
    return render_template('tools/index.html',
                         categories=Config.TOOL_CATEGORIES,
                         tools=tools,
                         all_categories=all_categories,
                         selected_category=category,
                         search_query=search_query,
                         tool_icons=TOOL_CUSTOM_ICONS,
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@tools_bp.route('/<tool_name>')
def tool_page(tool_name):
    from flask import abort
    
    # Find which category this tool belongs to
    tool_category = None
    tool_info = None

    for category_id, category_data in Config.TOOL_CATEGORIES.items():
        if tool_name in category_data['tools']:
            tool_category = category_id
            tool_info = {
                'name': category_data['name'],
                'icon': category_data['icon'],
                'custom_icon': TOOL_CUSTOM_ICONS.get(tool_name, category_data['icon']),
                'color': category_data['color']
            }
            break

    if not tool_category:
        # Try to find the tool in database
        tool_from_db = Tool.query.filter_by(name=tool_name, is_active=True).first()
        if tool_from_db:
            tool_category = tool_from_db.category.name
            tool_info = {
                'name': tool_from_db.category.display_name,
                'icon': tool_from_db.category.icon,
                'custom_icon': TOOL_CUSTOM_ICONS.get(tool_name, tool_from_db.icon),
                'color': getattr(tool_from_db.category, 'color', 'blue')
            }
        else:
            # Return 404 if tool not found anywhere
            abort(404)

    # Try to use specific template for the tool, fallback to generic
    try:
        specific_template = f'tools/{tool_name}.html'
        print(f"DEBUG: Trying to load specific template: {specific_template}")
        return render_template(specific_template,
                             tool_name=tool_name,
                             tool_category=tool_category,
                             tool_info=tool_info,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
    except:
        # Fallback to generic template if specific doesn't exist
        print(f"DEBUG: Using generic template for {tool_name}")
        return render_template('tools/generic_tool.html',
                             tool_name=tool_name,
                             tool_category=tool_category,
                             tool_info=tool_info,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

# All tools use generic template through main route /<tool_name>