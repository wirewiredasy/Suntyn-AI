from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
from utils.pdf_tools import PDFProcessor
from utils.image_tools import ImageProcessor
from utils.video_tools import VideoProcessor
from utils.ai_tools import AIProcessor
from utils.file_handler import FileHandler

api_bp = Blueprint('api', __name__)

# PDF Tools
@api_bp.route('/pdf/merge', methods=['POST'])
def merge_pdfs():
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'success': False, 'error': 'No files provided'})

        output_path = PDFProcessor.merge_pdfs([file for file in files])
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/pdf/split', methods=['POST'])
def split_pdf():
    try:
        file = request.files.get('file')
        pages_per_file = int(request.form.get('pages_per_file', 1))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_files = PDFProcessor.split_pdf(file, pages_per_file)
        return jsonify({
            'success': True,
            'files': [{'filename': os.path.basename(f), 'download_url': f'/api/download/{os.path.basename(f)}'} for f in output_files]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/pdf/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files.get('file')
        quality = float(request.form.get('quality', 0.7))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = PDFProcessor.compress_pdf(file, quality)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/pdf/watermark', methods=['POST'])
def add_pdf_watermark():
    try:
        file = request.files.get('file')
        watermark_text = request.form.get('watermark_text', 'Watermark')
        position = request.form.get('position', 'center')
        opacity = float(request.form.get('opacity', 0.5))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = PDFProcessor.add_watermark(file, watermark_text, position, opacity)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/pdf/rotate', methods=['POST'])
def rotate_pdf():
    try:
        file = request.files.get('file')
        rotation = int(request.form.get('rotation', 90))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = PDFProcessor.rotate_pdf(file, rotation)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/pdf/extract-pages', methods=['POST'])
def extract_pdf_pages():
    try:
        file = request.files.get('file')
        pages = request.form.get('pages', '[1]')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        import json
        page_list = json.loads(pages)
        output_path = PDFProcessor.extract_pages(file, page_list)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Image Tools
@api_bp.route('/image/compress', methods=['POST'])
def compress_image():
    try:
        file = request.files.get('file')
        quality = int(request.form.get('quality', 85))
        format = request.form.get('format', 'jpeg')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.compress_image(file, quality, format)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/resize', methods=['POST'])
def resize_image():
    try:
        file = request.files.get('file')
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))
        maintain_aspect = request.form.get('maintain_aspect', 'true').lower() == 'true'

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.resize_image(file, width, height, maintain_aspect)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/convert', methods=['POST'])
def convert_image():
    try:
        file = request.files.get('file')
        format = request.form.get('format', 'png')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.convert_image(file, format)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/crop', methods=['POST'])
def crop_image():
    try:
        file = request.files.get('file')
        x = int(request.form.get('x', 0))
        y = int(request.form.get('y', 0))
        width = int(request.form.get('width', 100))
        height = int(request.form.get('height', 100))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.crop_image(file, x, y, width, height)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/rotate', methods=['POST'])
def rotate_image():
    try:
        file = request.files.get('file')
        angle = int(request.form.get('angle', 90))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.rotate_image(file, angle)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/watermark', methods=['POST'])
def add_image_watermark():
    try:
        file = request.files.get('file')
        watermark_text = request.form.get('watermark_text', 'Watermark')
        position = request.form.get('position', 'bottom-right')
        opacity = float(request.form.get('opacity', 0.7))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.add_watermark(file, watermark_text, position, opacity)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/image/remove-background', methods=['POST'])
def remove_background():
    try:
        file = request.files.get('file')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = ImageProcessor.remove_background(file)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Video Tools
@api_bp.route('/video/trim', methods=['POST'])
def trim_video():
    try:
        file = request.files.get('file')
        start_time = float(request.form.get('start_time', 0))
        end_time = float(request.form.get('end_time', 10))

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = VideoProcessor.trim_video(file, start_time, end_time)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/video/extract-audio', methods=['POST'])
def extract_audio():
    try:
        file = request.files.get('file')
        format = request.form.get('format', 'mp3')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = VideoProcessor.extract_audio(file, format)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/video/compress', methods=['POST'])
def compress_video():
    try:
        file = request.files.get('file')
        quality = request.form.get('quality', 'medium')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = VideoProcessor.compress_video(file, quality)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/video/convert', methods=['POST'])
def convert_video():
    try:
        file = request.files.get('file')
        format = request.form.get('format', 'mp4')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = VideoProcessor.convert_video(file, format)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/video/crop-vertical', methods=['POST'])
def crop_vertical():
    try:
        file = request.files.get('file')
        aspect_ratio = request.form.get('aspect_ratio', '9:16')

        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})

        output_path = VideoProcessor.crop_vertical(file, aspect_ratio)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# AI Tools
@api_bp.route('/ai/resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        output_path = AIProcessor.generate_resume(data)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/ai/business-names', methods=['POST'])
def generate_business_names():
    try:
        data = request.get_json()
        result = AIProcessor.generate_business_names(data)
        return jsonify({'success': True, 'names': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/ai/blog-titles', methods=['POST'])
def generate_blog_titles():
    try:
        data = request.get_json()
        result = AIProcessor.generate_blog_titles(data)
        return jsonify({'success': True, 'titles': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/ai/product-description', methods=['POST'])
def generate_product_description():
    try:
        data = request.get_json()
        result = AIProcessor.generate_product_description(data)
        return jsonify({'success': True, 'description': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/ai/ad-copy', methods=['POST'])
def generate_ad_copy():
    try:
        data = request.get_json()
        result = AIProcessor.generate_ad_copy(data)
        return jsonify({'success': True, 'copy': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Utility Tools
@api_bp.route('/utility/qr-code', methods=['POST'])
def generate_qr_code():
    try:
        content = request.form.get('content')
        size = int(request.form.get('size', 300))
        format = request.form.get('format', 'png')

        if not content:
            return jsonify({'success': False, 'error': 'No content provided'})

        output_path = FileHandler.generate_qr_code(content, size, format)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{os.path.basename(output_path)}',
            'filename': os.path.basename(output_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Download endpoint
@api_bp.route('/download/<filename>')
def download_file(filename):
    try:
        # Security: Only allow files from uploads directory
        safe_filename = secure_filename(filename)
        file_path = os.path.join('uploads', safe_filename)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User data endpoints
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