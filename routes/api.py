from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import tempfile
from models import User, ToolHistory, SavedFile
from app import db
import logging

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

# PDF Tools
@api_bp.route('/pdf/merge', methods=['POST'])
def merge_pdf_files():
    """Merge multiple PDF files"""
    try:
        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files required'}), 400

        from utils.pdf_tools import PDFProcessor

        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            temp_path = os.path.join('uploads', temp_filename)
            file.save(temp_path)
            temp_files.append(temp_path)

        # Merge PDFs
        output_path = PDFProcessor.merge_pdfs(temp_files)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to merge PDFs'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/pdf/split', methods=['POST'])
def split_pdf_files():
    """Split PDF into multiple files"""
    try:
        file = request.files['file']
        pages_per_file = int(request.form.get('pages_per_file', 1))

        from utils.pdf_tools import PDFProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Split PDF
        output_files = PDFProcessor.split_pdf(temp_path, pages_per_file)

        if output_files:
            return jsonify({
                'success': True,
                'files': [{'filename': os.path.basename(f), 'download_url': f'/api/download/{os.path.basename(f)}'} for f in output_files]
            })
        else:
            return jsonify({'error': 'Failed to split PDF'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/pdf/compress', methods=['POST'])
def compress_pdf():
    """Compress PDF file"""
    try:
        file = request.files['file']
        quality = float(request.form.get('quality', 0.7))

        from utils.pdf_tools import PDFProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Compress PDF
        output_path = PDFProcessor.compress_pdf(temp_path, quality)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to compress PDF'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Image Tools
@api_bp.route('/image/compress', methods=['POST'])
def compress_image():
    """Compress image file"""
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 85))

        from utils.image_tools import ImageProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Compress image
        output_path = ImageProcessor.compress_image(temp_path, quality)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to compress image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/image/resize', methods=['POST'])
def resize_image():
    """Resize image file"""
    try:
        file = request.files['file']
        width = request.form.get('width')
        height = request.form.get('height')
        maintain_aspect = request.form.get('maintain_aspect', 'true').lower() == 'true'

        from utils.image_tools import ImageProcessor

        # Convert dimensions to integers if provided
        width = int(width) if width else None
        height = int(height) if height else None

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Resize image
        output_path = ImageProcessor.resize_image(temp_path, width, height, maintain_aspect)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to resize image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/image/convert', methods=['POST'])
def convert_image():
    """Convert image to different format"""
    try:
        file = request.files['file']
        output_format = request.form.get('format', 'JPEG').upper()

        from utils.image_tools import ImageProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Convert image
        output_path = ImageProcessor.convert_image(temp_path, output_format)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to convert image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Video Tools
@api_bp.route('/video/extract-audio', methods=['POST'])
def extract_audio():
    """Extract audio from video"""
    try:
        file = request.files['file']
        output_format = request.form.get('format', 'mp3')

        from utils.video_tools import VideoProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Extract audio
        output_path = VideoProcessor.extract_audio(temp_path, output_format)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to extract audio'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/video/trim', methods=['POST'])
def trim_video():
    """Trim video file"""
    try:
        file = request.files['file']
        start_time = float(request.form.get('start_time', 0))
        duration = request.form.get('duration')
        duration = float(duration) if duration else None

        from utils.video_tools import VideoProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Trim video
        output_path = VideoProcessor.trim_video(temp_path, start_time, duration)

        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to trim video'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Tools
@api_bp.route('/ai/generate-resume', methods=['POST'])
def generate_resume():
    """Generate resume using AI"""
    try:
        name = request.form.get('name', 'John Doe')
        experience = request.form.get('experience', 'Software Developer')
        skills = request.form.get('skills', 'Python, JavaScript, React')
        
        from utils.ai_tools import AIProcessor
        
        # Generate resume PDF
        output_path = AIProcessor.generate_resume(name, experience, skills)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to generate resume'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/generate-business-names', methods=['POST'])
def generate_business_names():
    """Generate business name suggestions"""
    try:
        industry = request.form.get('industry', 'Technology')
        keywords = request.form.get('keywords', '')
        
        from utils.ai_tools import AIProcessor
        
        # Generate business names
        names = AIProcessor.generate_business_names(industry, keywords)
        
        return jsonify({
            'success': True,
            'business_names': names
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@api_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'tools': 'operational'})

# Generic tool processing endpoint
@api_bp.route('/tools/generic/<tool_name>', methods=['POST'])
def process_generic_tool(tool_name):
    """Generic tool processing endpoint"""
    try:
        # Log tool usage
        logging.info(f"Processing tool: {tool_name}")
        
        # Return demo response for now
        return jsonify({
            'success': True,
            'message': f'Tool {tool_name} processed successfully',
            'demo_mode': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500