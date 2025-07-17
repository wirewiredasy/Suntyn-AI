
from flask import Blueprint, request, jsonify, send_file
import os
import uuid
from werkzeug.utils import secure_filename
import tempfile
import logging

# Import tool utilities
from utils.pdf_tools import PDFProcessor
from utils.image_tools import ImageProcessor
from utils.video_tools import VideoProcessor
from utils.ai_tools import AIProcessor

enhanced_api_bp = Blueprint('enhanced_api', __name__, url_prefix='/api/v2')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'document': ['.txt', '.doc', '.docx', '.rtf']
}

def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = '.' + filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, [])

def save_uploaded_file(file, prefix='uploaded'):
    """Save uploaded file and return path"""
    if not file or file.filename == '':
        return None
    
    filename = secure_filename(file.filename)
    unique_filename = f"{prefix}_{uuid.uuid4()}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(file_path)
    return file_path

# PDF Tool APIs
@enhanced_api_bp.route('/pdf/merge', methods=['POST'])
def pdf_merge():
    """Merge multiple PDF files"""
    try:
        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files required'}), 400
        
        # Save uploaded files
        file_paths = []
        for file in files:
            if not allowed_file(file.filename, 'pdf'):
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
            
            file_path = save_uploaded_file(file, 'pdf')
            if file_path:
                file_paths.append(file_path)
        
        # Process PDFs
        output_path = PDFProcessor.merge_pdfs(file_paths)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/v2/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path),
                'message': 'PDFs merged successfully'
            })
        else:
            return jsonify({'error': 'PDF merge failed'}), 500
            
    except Exception as e:
        logger.error(f"PDF merge error: {e}")
        return jsonify({'error': str(e)}), 500

@enhanced_api_bp.route('/pdf/split', methods=['POST'])
def pdf_split():
    """Split PDF file"""
    try:
        file = request.files.get('file')
        if not file or not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Valid PDF file required'}), 400
        
        # Get split options
        split_type = request.form.get('split_type', 'pages')
        page_ranges = request.form.get('page_ranges', '')
        
        file_path = save_uploaded_file(file, 'pdf')
        output_files = PDFProcessor.split_pdf(file_path, split_type, page_ranges)
        
        if output_files:
            file_links = []
            for output_file in output_files:
                file_links.append({
                    'filename': os.path.basename(output_file),
                    'download_url': f'/api/v2/download/{os.path.basename(output_file)}'
                })
            
            return jsonify({
                'success': True,
                'files': file_links,
                'message': 'PDF split successfully'
            })
        else:
            return jsonify({'error': 'PDF split failed'}), 500
            
    except Exception as e:
        logger.error(f"PDF split error: {e}")
        return jsonify({'error': str(e)}), 500

@enhanced_api_bp.route('/pdf/compress', methods=['POST'])
def pdf_compress():
    """Compress PDF file"""
    try:
        file = request.files.get('file')
        if not file or not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Valid PDF file required'}), 400
        
        quality = request.form.get('quality', 'medium')
        
        file_path = save_uploaded_file(file, 'pdf')
        output_path = PDFProcessor.compress_pdf(file_path, quality)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/v2/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path),
                'message': 'PDF compressed successfully'
            })
        else:
            return jsonify({'error': 'PDF compression failed'}), 500
            
    except Exception as e:
        logger.error(f"PDF compress error: {e}")
        return jsonify({'error': str(e)}), 500

# Image Tool APIs
@enhanced_api_bp.route('/image/compress', methods=['POST'])
def image_compress():
    """Compress image files"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No image files provided'}), 400
        
        quality = int(request.form.get('quality', 85))
        
        processed_files = []
        for file in files:
            if not allowed_file(file.filename, 'image'):
                continue
            
            file_path = save_uploaded_file(file, 'image')
            output_path = ImageProcessor.compress_image(file_path, quality)
            
            if output_path:
                processed_files.append({
                    'filename': os.path.basename(output_path),
                    'download_url': f'/api/v2/download/{os.path.basename(output_path)}'
                })
        
        if processed_files:
            return jsonify({
                'success': True,
                'files': processed_files,
                'message': 'Images compressed successfully'
            })
        else:
            return jsonify({'error': 'Image compression failed'}), 500
            
    except Exception as e:
        logger.error(f"Image compress error: {e}")
        return jsonify({'error': str(e)}), 500

@enhanced_api_bp.route('/image/resize', methods=['POST'])
def image_resize():
    """Resize image files"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No image files provided'}), 400
        
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))
        maintain_aspect = request.form.get('maintain_aspect', 'true') == 'true'
        
        processed_files = []
        for file in files:
            if not allowed_file(file.filename, 'image'):
                continue
            
            file_path = save_uploaded_file(file, 'image')
            output_path = ImageProcessor.resize_image(file_path, width, height, maintain_aspect)
            
            if output_path:
                processed_files.append({
                    'filename': os.path.basename(output_path),
                    'download_url': f'/api/v2/download/{os.path.basename(output_path)}'
                })
        
        if processed_files:
            return jsonify({
                'success': True,
                'files': processed_files,
                'message': 'Images resized successfully'
            })
        else:
            return jsonify({'error': 'Image resize failed'}), 500
            
    except Exception as e:
        logger.error(f"Image resize error: {e}")
        return jsonify({'error': str(e)}), 500

# Video Tool APIs
@enhanced_api_bp.route('/video/extract-audio', methods=['POST'])
def video_extract_audio():
    """Extract audio from video"""
    try:
        file = request.files.get('file')
        if not file or not allowed_file(file.filename, 'video'):
            return jsonify({'error': 'Valid video file required'}), 400
        
        quality = request.form.get('quality', '192kbps')
        
        file_path = save_uploaded_file(file, 'video')
        output_path = VideoProcessor.extract_audio(file_path, quality)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/v2/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path),
                'message': 'Audio extracted successfully'
            })
        else:
            return jsonify({'error': 'Audio extraction failed'}), 500
            
    except Exception as e:
        logger.error(f"Video extract audio error: {e}")
        return jsonify({'error': str(e)}), 500

# AI Tool APIs
@enhanced_api_bp.route('/ai/generate-resume', methods=['POST'])
def ai_generate_resume():
    """Generate professional resume"""
    try:
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        experience = request.form.get('experience', '')
        skills = request.form.get('skills', '')
        education = request.form.get('education', '')
        template = request.form.get('processing_option', 'modern-template')
        
        if not name or not experience or not skills:
            return jsonify({'error': 'Name, experience, and skills are required'}), 400
        
        output_path = AIProcessor.generate_resume(name, email, phone, experience, skills, education, template)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/v2/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path),
                'message': 'Resume generated successfully'
            })
        else:
            return jsonify({'error': 'Resume generation failed'}), 500
            
    except Exception as e:
        logger.error(f"Resume generation error: {e}")
        return jsonify({'error': str(e)}), 500

@enhanced_api_bp.route('/ai/generate-business-names', methods=['POST'])
def ai_generate_business_names():
    """Generate business name suggestions"""
    try:
        industry = request.form.get('industry', '')
        keywords = request.form.get('keywords', '')
        style = request.form.get('processing_option', 'modern')
        
        if not industry:
            return jsonify({'error': 'Industry is required'}), 400
        
        business_names = AIProcessor.generate_business_names(industry, keywords, style)
        
        return jsonify({
            'success': True,
            'business_names': business_names,
            'message': 'Business names generated successfully'
        })
            
    except Exception as e:
        logger.error(f"Business name generation error: {e}")
        return jsonify({'error': str(e)}), 500

# Utility APIs
@enhanced_api_bp.route('/utility/generate-qr', methods=['POST'])
def utility_generate_qr():
    """Generate QR code"""
    try:
        content = request.form.get('content', '')
        qr_type = request.form.get('processing_option', 'url')
        size = int(request.form.get('size', 300))
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        from utils.utility_utils import UtilityProcessor
        output_path = UtilityProcessor.generate_qr_code(content, qr_type, size)
        
        if output_path:
            return jsonify({
                'success': True,
                'download_url': f'/api/v2/download/{os.path.basename(output_path)}',
                'filename': os.path.basename(output_path),
                'message': 'QR code generated successfully'
            })
        else:
            return jsonify({'error': 'QR code generation failed'}), 500
            
    except Exception as e:
        logger.error(f"QR generation error: {e}")
        return jsonify({'error': str(e)}), 500

# Download endpoint
@enhanced_api_bp.route('/download/<filename>')
def download_file(filename):
    """Download processed file"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': 'Download failed'}), 500

# Health check
@enhanced_api_bp.route('/health')
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'features': ['pdf', 'image', 'video', 'ai', 'utility']
    })
