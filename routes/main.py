from flask import Blueprint, render_template, request, jsonify
from models import User, ToolHistory, ToolCategory
from app import db
from config import Config
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
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

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
    return render_template('auth/dashboard.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@main_bp.route('/login')
def login():
    """Login page"""
    return render_template('auth/login.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

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

@main_bp.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404
