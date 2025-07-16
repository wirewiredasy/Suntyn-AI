from flask import Blueprint, render_template, request, jsonify
from models import User, ToolHistory, ToolCategory
from app import db
from config import Config
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get popular tools based on usage
    popular_tools = db.session.query(ToolHistory.tool_name, ToolHistory.tool_category, db.func.count(ToolHistory.id).label('usage_count'))\
        .group_by(ToolHistory.tool_name, ToolHistory.tool_category)\
        .order_by(db.func.count(ToolHistory.id).desc())\
        .limit(8).all()

    return render_template('index.html',
                         categories=Config.TOOL_CATEGORIES,
                         popular_tools=popular_tools,
                         firebase_api_key=Config.FIREBASE_API_KEY,
                         firebase_project_id=Config.FIREBASE_PROJECT_ID,
                         firebase_app_id=Config.FIREBASE_APP_ID)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []

    if query:
        for category_id, category_data in Config.TOOL_CATEGORIES.items():
            for tool in category_data['tools']:
                if query in tool.lower() or query in category_data['name'].lower():
                    results.append({
                        'tool': tool,
                        'category': category_id,
                        'category_name': category_data['name'],
                        'icon': category_data['icon'],
                        'color': category_data['color']
                    })

    return jsonify(results)

@main_bp.route('/dashboard')
def dashboard():
    # This will be protected by Firebase auth on frontend
    return render_template('dashboard.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@main_bp.route('/api/dashboard/stats')
def dashboard_stats():
    """Get real dashboard statistics for current user"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        # Return generic stats for demo mode
        return jsonify({
            'tools_used': 0,
            'files_processed': 0,
            'data_saved': '0 MB',
            'time_saved': '0 hours',
            'recent_activity': [],
            'quick_tools': get_popular_tools()
        })
    
    try:
        # Get user from database
        user = User.query.filter_by(firebase_uid=user_id).first()
        if not user:
            # Create new user record
            user = User(firebase_uid=user_id, email='', display_name='')
            db.session.add(user)
            db.session.commit()
        
        # Calculate real statistics
        total_tools_used = ToolHistory.query.filter_by(user_id=user.id).count()
        total_files = db.session.query(db.func.sum(ToolHistory.file_count)).filter_by(user_id=user.id).scalar() or 0
        
        # Calculate data saved (sum of file sizes)
        total_size_mb = db.session.query(db.func.sum(ToolHistory.file_size_mb)).filter_by(user_id=user.id).scalar() or 0
        data_saved = f"{total_size_mb:.1f} MB" if total_size_mb < 1024 else f"{total_size_mb/1024:.1f} GB"
        
        # Calculate time saved (estimated based on tool usage)
        time_saved_minutes = total_tools_used * 5  # Assume 5 minutes saved per tool use
        time_saved = f"{time_saved_minutes//60} hours {time_saved_minutes%60} min" if time_saved_minutes >= 60 else f"{time_saved_minutes} min"
        
        # Get recent activity
        recent_activity = ToolHistory.query.filter_by(user_id=user.id)\
            .order_by(ToolHistory.used_at.desc())\
            .limit(10).all()
        
        activity_data = []
        for activity in recent_activity:
            activity_data.append({
                'id': activity.id,
                'tool_name': activity.tool_name,
                'tool_category': activity.tool_category,
                'used_at': activity.used_at.isoformat(),
                'file_count': activity.file_count,
                'processing_time': activity.processing_time
            })
        
        return jsonify({
            'tools_used': total_tools_used,
            'files_processed': total_files,
            'data_saved': data_saved,
            'time_saved': time_saved,
            'recent_activity': activity_data,
            'quick_tools': get_popular_tools()
        })
        
    except Exception as e:
        print(f"Dashboard stats error: {e}")
        return jsonify({
            'tools_used': 0,
            'files_processed': 0,
            'data_saved': '0 MB',
            'time_saved': '0 hours',
            'recent_activity': [],
            'quick_tools': get_popular_tools()
        })

def get_popular_tools():
    """Get most popular tools across all users"""
    popular = db.session.query(
        ToolHistory.tool_name,
        ToolHistory.tool_category,
        db.func.count(ToolHistory.id).label('usage_count')
    ).group_by(ToolHistory.tool_name, ToolHistory.tool_category)\
     .order_by(db.func.count(ToolHistory.id).desc())\
     .limit(6).all()
    
    tools_data = []
    for tool in popular:
        tools_data.append({
            'name': tool.tool_name,
            'category': tool.tool_category,
            'usage_count': tool.usage_count,
            'display_name': tool.tool_name.replace('-', ' ').title()
        })
    
    # Add default tools if no usage data
    if len(tools_data) < 6:
        default_tools = [
            {'name': 'pdf-merge', 'category': 'pdf', 'display_name': 'PDF Merge', 'usage_count': 0},
            {'name': 'image-compress', 'category': 'image', 'display_name': 'Image Compress', 'usage_count': 0},
            {'name': 'video-to-mp3', 'category': 'video', 'display_name': 'Video To MP3', 'usage_count': 0},
            {'name': 'resume-generator', 'category': 'ai', 'display_name': 'Resume Generator', 'usage_count': 0},
            {'name': 'qr-generator', 'category': 'utility', 'display_name': 'QR Generator', 'usage_count': 0},
            {'name': 'text-case-converter', 'category': 'utility', 'display_name': 'Text Case Converter', 'usage_count': 0}
        ]
        tools_data.extend(default_tools[len(tools_data):])
    
    return tools_data[:6]

@main_bp.route('/api/dashboard/track', methods=['POST'])
def track_tool_usage():
    """Track tool usage for dashboard analytics"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        tool_name = data.get('tool_name')
        tool_category = data.get('tool_category')
        file_count = data.get('file_count', 1)
        file_size_mb = data.get('file_size_mb', 0)
        
        if not user_id or not tool_name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get or create user
        user = User.query.filter_by(firebase_uid=user_id).first()
        if not user:
            user = User(
                firebase_uid=user_id,
                email=data.get('email', ''),
                display_name=data.get('display_name', '')
            )
            db.session.add(user)
            db.session.commit()
        
        # Create tool history record
        tool_history = ToolHistory(
            user_id=user.id,
            tool_name=tool_name,
            tool_category=tool_category,
            file_count=file_count,
            file_size_mb=file_size_mb,
            used_at=datetime.utcnow(),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        db.session.add(tool_history)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tool usage tracked'})
        
    except Exception as e:
        print(f"Error tracking tool usage: {e}")
        return jsonify({'error': 'Failed to track usage'}), 500

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    return render_template('terms.html')

@main_bp.route('/cookies')
def cookies():
    return render_template('cookies.html')

@main_bp.route('/faq')
def faq():
    return render_template('faq.html')

@main_bp.route('/blog')
def blog():
    return render_template('blog.html')

@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap for SEO"""
    from flask import Response
    import datetime

    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://toolora-ai.replit.app/</loc>
            <lastmod>{}</lastmod>
            <changefreq>daily</changefreq>
            <priority>1.0</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/tools</loc>
            <lastmod>{}</lastmod>
            <changefreq>daily</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/about</loc>
            <lastmod>{}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/contact</loc>
            <lastmod>{}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/privacy</loc>
            <lastmod>{}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.6</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/terms</loc>
            <lastmod>{}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.6</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/cookies</loc>
            <lastmod>{}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.5</priority>
        </url>
        <url>
            <loc>https://toolora-ai.replit.app/faq</loc>
            <lastmod>{}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
    '''.format(
        datetime.datetime.now().strftime('%Y-%m-%d'), 
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d'),
        datetime.datetime.now().strftime('%Y-%m-%d')
    )

    # Add all tool URLs
    for category_id, category_data in Config.TOOL_CATEGORIES.items():
        for tool in category_data['tools']:
            sitemap_xml += '''
        <url>
            <loc>https://toolora-ai.replit.app/tools/{}</loc>
            <lastmod>{}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
            '''.format(tool, datetime.datetime.now().strftime('%Y-%m-%d'))

    sitemap_xml += '\n    </urlset>'

    return Response(sitemap_xml, mimetype='application/xml')

@main_bp.route('/robots.txt')
def robots():
    """Generate robots.txt for SEO"""
    from flask import Response

    robots_txt = '''User-agent: *
Allow: /
Sitemap: https://toolora-ai.replit.app/sitemap.xml
'''

    return Response(robots_txt, mimetype='text/plain')

# Remove this local 404 handler since we have a global one