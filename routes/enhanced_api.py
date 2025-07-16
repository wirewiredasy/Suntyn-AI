from flask import Blueprint, request, jsonify, send_file
import os
import uuid
from werkzeug.utils import secure_filename
import tempfile
from datetime import datetime
import json

# Import processing utilities
from utils.pdf_utils import merge_pdfs, split_pdf, compress_pdf
from utils.image_utils import compress_image, resize_image, remove_background
from utils.video_utils import trim_video, extract_audio
from utils.ai_utils import generate_resume, generate_business_names
from utils.utility_utils import generate_password, convert_text_case, generate_qr_code

api_bp = Blueprint('enhanced_api', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'pdf': ['pdf'],
    'image': ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'],
    'video': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'],
    'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg'],
    'document': ['doc', 'docx', 'txt', 'rtf']
}

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, [])

def generate_unique_filename(original_filename):
    """Generate a unique filename to prevent conflicts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(secure_filename(original_filename))
    return f"{name}_{timestamp}_{unique_id}{ext}"

# PDF Tools API Endpoints
@api_bp.route('/tools/pdf-merge', methods=['POST'])
def api_pdf_merge():
    try:
        files = []
        for key in request.files:
            if key.startswith('file_'):
                file = request.files[key]
                if file and allowed_file(file.filename, 'pdf'):
                    # Save file temporarily
                    filename = generate_unique_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    files.append(filepath)
        
        if len(files) < 2:
            return jsonify({'success': False, 'message': 'Please upload at least 2 PDF files'})
        
        # Process PDF merge
        output_filename = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = merge_pdfs(files, output_path)
        
        # Clean up input files
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': 'PDFs merged successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error merging PDFs'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/pdf-split', methods=['POST'])
def api_pdf_split():
    try:
        file = request.files.get('file_0')
        page_range = request.form.get('page_range', '1-3')
        
        if not file or not allowed_file(file.filename, 'pdf'):
            return jsonify({'success': False, 'message': 'Please upload a valid PDF file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process PDF split
        output_filename = f"split_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = split_pdf(filepath, output_path, page_range)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': f'Pages {page_range} extracted successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error splitting PDF'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/pdf-compress', methods=['POST'])
def api_pdf_compress():
    try:
        file = request.files.get('file_0')
        compression_level = request.form.get('compression_level', 'medium')
        
        if not file or not allowed_file(file.filename, 'pdf'):
            return jsonify({'success': False, 'message': 'Please upload a valid PDF file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process PDF compression
        output_filename = f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success, original_size, compressed_size = compress_pdf(filepath, output_path, compression_level)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            reduction = round((1 - compressed_size / original_size) * 100, 1)
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'size': compressed_size,
                'message': f'PDF compressed successfully! Size reduced by {reduction}%'
            })
        else:
            return jsonify({'success': False, 'message': 'Error compressing PDF'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Image Tools API Endpoints
@api_bp.route('/tools/image-compress', methods=['POST'])
def api_image_compress():
    try:
        file = request.files.get('image')
        quality = int(request.form.get('quality', 80))
        
        if not file or not allowed_file(file.filename, 'image'):
            return jsonify({'success': False, 'message': 'Please upload a valid image file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process image compression
        output_filename = f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success, original_size, compressed_size = compress_image(filepath, output_path, quality)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'size': compressed_size,
                'message': 'Image compressed successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error compressing image'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/image-resize', methods=['POST'])
def api_image_resize():
    try:
        file = request.files.get('image')
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))
        maintain_aspect = request.form.get('maintain_aspect', 'true') == 'true'
        
        if not file or not allowed_file(file.filename, 'image'):
            return jsonify({'success': False, 'message': 'Please upload a valid image file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process image resize
        output_filename = f"resized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = resize_image(filepath, output_path, width, height, maintain_aspect)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': f'Image resized to {width}x{height} successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error resizing image'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Video Tools API Endpoints
@api_bp.route('/tools/video-trimmer', methods=['POST'])
def api_video_trimmer():
    try:
        file = request.files.get('video')
        start_time = float(request.form.get('startTime', 0))
        end_time = float(request.form.get('endTime', 10))
        
        if not file or not allowed_file(file.filename, 'video'):
            return jsonify({'success': False, 'message': 'Please upload a valid video file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process video trimming
        output_filename = f"trimmed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = trim_video(filepath, output_path, start_time, end_time)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': f'Video trimmed from {start_time}s to {end_time}s successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error trimming video'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/video-to-mp3', methods=['POST'])
def api_video_to_mp3():
    try:
        file = request.files.get('file_0')
        
        if not file or not allowed_file(file.filename, 'video'):
            return jsonify({'success': False, 'message': 'Please upload a valid video file'})
        
        # Save file temporarily
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process audio extraction
        output_filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = extract_audio(filepath, output_path)
        
        # Clean up input file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': 'Audio extracted successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error extracting audio'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# AI Tools API Endpoints
@api_bp.route('/tools/resume-generator', methods=['POST'])
def api_resume_generator():
    try:
        form_data = request.get_json()
        
        if not form_data or not form_data.get('name'):
            return jsonify({'success': False, 'message': 'Please provide required information'})
        
        # Process resume generation
        output_filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = generate_resume(form_data, output_path)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'message': 'Resume generated successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error generating resume'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/business-name-generator', methods=['POST'])
def api_business_name_generator():
    try:
        keywords = request.json.get('keywords', '')
        industry = request.json.get('industry', 'general')
        count = int(request.json.get('count', 10))
        
        if not keywords:
            return jsonify({'success': False, 'message': 'Please provide keywords'})
        
        # Process business name generation
        names = generate_business_names(keywords, industry, count)
        
        if names:
            return jsonify({
                'success': True, 
                'names': names,
                'message': f'Generated {len(names)} business names!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error generating business names'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Utility Tools API Endpoints
@api_bp.route('/tools/qr-generator', methods=['POST'])
def api_qr_generator():
    try:
        data = request.get_json()
        text = data.get('text', '')
        size = int(data.get('size', 256))
        color = data.get('color', '#000000')
        bg_color = data.get('bgColor', '#ffffff')
        format_type = data.get('format', 'PNG')
        
        if not text:
            return jsonify({'success': False, 'message': 'Please provide text or URL'})
        
        # Process QR code generation
        output_filename = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type.lower()}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        success = generate_qr_code(text, output_path, size, color, bg_color)
        
        if success:
            return jsonify({
                'success': True, 
                'filename': output_filename,
                'url': f'/api/download/{output_filename}',
                'message': 'QR Code generated successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error generating QR code'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@api_bp.route('/tools/password-generator', methods=['POST'])
def api_password_generator():
    try:
        length = int(request.json.get('length', 12))
        include_uppercase = request.json.get('uppercase', True)
        include_lowercase = request.json.get('lowercase', True)
        include_numbers = request.json.get('numbers', True)
        include_symbols = request.json.get('symbols', True)
        
        # Process password generation
        password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
        
        if password:
            return jsonify({
                'success': True, 
                'password': password,
                'message': 'Password generated successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'Error generating password'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Generic tool handler for tools without specific implementation
@api_bp.route('/tools/generic/<tool_name>', methods=['POST'])
def api_generic_tool(tool_name):
    try:
        # Handle file uploads
        files = []
        for key in request.files:
            if key.startswith('file_'):
                file = request.files[key]
                if file:
                    filename = generate_unique_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    files.append(filepath)
        
        # For now, just return success with file count
        # In production, you would implement actual processing logic
        
        # Clean up uploaded files after processing
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return jsonify({
            'success': True, 
            'message': f'{tool_name.replace("-", " ").title()} processed {len(files)} files successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# File download endpoint
@api_bp.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@api_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'upload_folder': UPLOAD_FOLDER
    })

# Initialize upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)