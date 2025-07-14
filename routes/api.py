from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from models import User, ToolHistory, SavedFile
from app import db
from utils.pdf_tools import merge_pdfs, split_pdf, compress_pdf
from utils.image_tools import compress_image, resize_image, convert_image
from utils.video_tools import trim_video, extract_audio
from utils.ai_tools import generate_resume, generate_business_names

api_bp = Blueprint('api', __name__)

def get_current_user():
    """Get current user from session"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Generate unique filename
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        
        # Ensure uploads directory exists
        os.makedirs('uploads', exist_ok=True)
        
        file.save(file_path)
        
        # Save file info if user is logged in
        user = get_current_user()
        if user:
            saved_file = SavedFile(
                user_id=user.id,
                original_filename=file.filename,
                saved_filename=filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                mime_type=file.content_type or 'application/octet-stream',
                tool_used=request.form.get('tool', 'unknown')
            )
            db.session.add(saved_file)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'original_filename': file.filename,
            'file_path': file_path
        })

@api_bp.route('/download/<filename>')
def download_file(filename):
    """Download processed file"""
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

# PDF Tool APIs
@api_bp.route('/pdf/merge', methods=['POST'])
def merge_pdf_files():
    """Merge multiple PDF files"""
    try:
        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files required'}), 400
        
        # Save uploaded files
        file_paths = []
        for file in files:
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            file_paths.append(file_path)
        
        # Merge PDFs
        output_filename = f"merged_{uuid.uuid4()}.pdf"
        output_path = os.path.join('uploads', output_filename)
        
        success = merge_pdfs(file_paths, output_path)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='pdf-merge',
                    tool_category='pdf',
                    file_count=len(files)
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to merge PDFs'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/image/compress', methods=['POST'])
def compress_image_file():
    """Compress image file"""
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 85))
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Compress image
        output_filename = f"compressed_{uuid.uuid4()}.jpg"
        output_path = os.path.join('uploads', output_filename)
        
        success = compress_image(input_path, output_path, quality)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='image-compress',
                    tool_category='image'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to compress image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/resume', methods=['POST'])
def generate_resume_api():
    """Generate resume using AI"""
    try:
        data = request.get_json()
        
        # Extract resume data
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        experience = data.get('experience', [])
        education = data.get('education', [])
        skills = data.get('skills', [])
        
        # Generate resume
        output_filename = f"resume_{uuid.uuid4()}.pdf"
        output_path = os.path.join('uploads', output_filename)
        
        success = generate_resume(name, email, phone, experience, education, skills, output_path)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='resume-generator',
                    tool_category='ai'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to generate resume'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/user/history')
def get_user_history():
    """Get user's tool usage history"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    history = ToolHistory.query.filter_by(user_id=user.id)\
        .order_by(ToolHistory.used_at.desc())\
        .limit(50).all()
    
    return jsonify([{
        'tool_name': h.tool_name,
        'tool_category': h.tool_category,
        'used_at': h.used_at.isoformat(),
        'file_count': h.file_count
    } for h in history])

@api_bp.route('/user/files')
def get_user_files():
    """Get user's saved files"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    files = SavedFile.query.filter_by(user_id=user.id)\
        .order_by(SavedFile.created_at.desc())\
        .limit(50).all()
    
    return jsonify([{
        'id': f.id,
        'original_filename': f.original_filename,
        'file_size': f.file_size,
        'mime_type': f.mime_type,
        'tool_used': f.tool_used,
        'created_at': f.created_at.isoformat(),
        'download_url': f'/api/download/{f.saved_filename}'
    } for f in files])
