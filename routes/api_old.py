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

# Additional PDF Tools
@api_bp.route('/pdf/split', methods=['POST'])
def split_pdf_file():
    """Split PDF into multiple files"""
    try:
        file = request.files['file']
        pages_per_file = int(request.form.get('pages_per_file', 1))
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Split PDF
        output_dir = os.path.join('uploads', f"split_{uuid.uuid4()}")
        os.makedirs(output_dir, exist_ok=True)
        
        output_files = split_pdf(input_path, output_dir, pages_per_file)
        
        if output_files:
            # Create zip file for download
            zip_filename = f"split_pdf_{uuid.uuid4()}.zip"
            zip_path = os.path.join('uploads', zip_filename)
            
            import zipfile
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='pdf-split',
                    tool_category='pdf'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{zip_filename}',
                'filename': zip_filename,
                'files_created': len(output_files)
            })
        else:
            return jsonify({'error': 'Failed to split PDF'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/pdf/compress', methods=['POST'])
def compress_pdf_file():
    """Compress PDF file"""
    try:
        file = request.files['file']
        quality = float(request.form.get('quality', 0.7))
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Compress PDF
        output_filename = f"compressed_{uuid.uuid4()}.pdf"
        output_path = os.path.join('uploads', output_filename)
        
        success = compress_pdf(input_path, output_path, quality)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='pdf-compress',
                    tool_category='pdf'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to compress PDF'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Additional Image Tools
@api_bp.route('/image/resize', methods=['POST'])
def resize_image_file():
    """Resize image file"""
    try:
        file = request.files['file']
        width = request.form.get('width')
        height = request.form.get('height')
        
        if not width and not height:
            return jsonify({'error': 'Width or height required'}), 400
        
        width = int(width) if width else None
        height = int(height) if height else None
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Resize image
        output_filename = f"resized_{uuid.uuid4()}.jpg"
        output_path = os.path.join('uploads', output_filename)
        
        success = resize_image(input_path, output_path, width, height)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='image-resize',
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
            return jsonify({'error': 'Failed to resize image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/image/convert', methods=['POST'])
def convert_image_file():
    """Convert image to different format"""
    try:
        file = request.files['file']
        output_format = request.form.get('format', 'jpg').lower()
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Convert image
        output_filename = f"converted_{uuid.uuid4()}.{output_format}"
        output_path = os.path.join('uploads', output_filename)
        
        success = convert_image(input_path, output_path, output_format)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='image-convert',
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
            return jsonify({'error': 'Failed to convert image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Video Tools
@api_bp.route('/video/trim', methods=['POST'])
def trim_video_file():
    """Trim video file"""
    try:
        file = request.files['file']
        start_time = request.form.get('start_time', '0')
        end_time = request.form.get('end_time')
        
        if not end_time:
            return jsonify({'error': 'End time required'}), 400
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Trim video
        output_filename = f"trimmed_{uuid.uuid4()}.mp4"
        output_path = os.path.join('uploads', output_filename)
        
        success = trim_video(input_path, output_path, start_time, end_time)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='video-trim',
                    tool_category='video'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to trim video'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/video/extract_audio', methods=['POST'])
def extract_audio_from_video():
    """Extract audio from video"""
    try:
        file = request.files['file']
        audio_format = request.form.get('format', 'mp3')
        
        # Save uploaded file
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        input_path = os.path.join('uploads', filename)
        file.save(input_path)
        
        # Extract audio
        output_filename = f"audio_{uuid.uuid4()}.{audio_format}"
        output_path = os.path.join('uploads', output_filename)
        
        success = extract_audio(input_path, output_path, audio_format)
        
        if success:
            # Log tool usage
            user = get_current_user()
            if user:
                history = ToolHistory(
                    user_id=user.id,
                    tool_name='video-to-mp3',
                    tool_category='video'
                )
                db.session.add(history)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to extract audio'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Tools
@api_bp.route('/ai/business_names', methods=['POST'])
def generate_business_names_api():
    """Generate business name suggestions"""
    try:
        data = request.get_json()
        industry = data.get('industry', '')
        keywords = data.get('keywords', [])
        count = int(data.get('count', 10))
        
        names = generate_business_names(industry, keywords, count)
        
        # Log tool usage
        user = get_current_user()
        if user:
            history = ToolHistory(
                user_id=user.id,
                tool_name='business-name-generator',
                tool_category='ai'
            )
            db.session.add(history)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'names': names
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Utility route for dynamic tool processing
@api_bp.route('/<category>/<tool_name>', methods=['POST'])
def process_generic_tool(category, tool_name):
    """Generic tool processing endpoint"""
    try:
        # Map tool names to functions
        tool_map = {
            'pdf': {
                'merge': merge_pdf_files,
                'split': split_pdf_file,
                'compress': compress_pdf_file,
            },
            'image': {
                'compress': compress_image_file,
                'resize': resize_image_file,
                'convert': convert_image_file,
            },
            'video': {
                'trim': trim_video_file,
                'extract_audio': extract_audio_from_video,
            },
            'ai': {
                'resume': generate_resume_api,
                'business_names': generate_business_names_api,
            }
        }
        
        if category in tool_map and tool_name in tool_map[category]:
            return tool_map[category][tool_name]()
        else:
            return jsonify({'error': 'Tool not implemented yet'}), 501
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
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
