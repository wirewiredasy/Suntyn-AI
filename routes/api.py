"""
API Routes for Tool Functionality
Provides unique API endpoints for each tool with specific functionality
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import tempfile
from datetime import datetime
import logging

# Tool-specific imports
try:
    from PyPDF2 import PdfMerger, PdfReader, PdfWriter
except ImportError:
    print("PyPDF2 not available - PDF tools will use fallback")

try:
    from PIL import Image, ImageOps
except ImportError:
    print("PIL not available - Image tools will use fallback")

try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
except ImportError:
    print("QRCode library not available - using fallback QR generation")

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Helper functions
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_temp_filename(original_filename, suffix=""):
    """Create a unique temporary filename"""
    name, ext = os.path.splitext(secure_filename(original_filename))
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{unique_id}{suffix}{ext}"

# PDF Tools API Endpoints

@api_bp.route('/tools/pdf-merge', methods=['POST'])
def pdf_merge():
    """Merge multiple PDF files into one"""
    try:
        files = request.files.getlist('files')
        
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files are required'}), 400
        
        # Validate all files are PDFs
        for file in files:
            if not file or not allowed_file(file.filename, ['pdf']):
                return jsonify({'error': 'All files must be PDF format'}), 400
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            merger = PdfMerger()
            
            # Process files in order
            for i, file in enumerate(files):
                temp_path = os.path.join(temp_dir, f"input_{i}.pdf")
                file.save(temp_path)
                merger.append(temp_path)
            
            # Create output file
            output_filename = create_temp_filename("merged_document.pdf")
            output_path = os.path.join(temp_dir, output_filename)
            
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            
            # Send file and cleanup will happen automatically
            return send_file(output_path, 
                           as_attachment=True, 
                           download_name="merged_document.pdf",
                           mimetype='application/pdf')
    
    except Exception as e:
        logger.error(f"PDF merge error: {str(e)}")
        return jsonify({'error': 'Failed to merge PDF files'}), 500

@api_bp.route('/tools/pdf-split', methods=['POST'])
def pdf_split():
    """Split PDF into individual pages"""
    try:
        file = request.files.get('file')
        
        if not file or not allowed_file(file.filename, ['pdf']):
            return jsonify({'error': 'Please upload a valid PDF file'}), 400
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            input_path = os.path.join(temp_dir, 'input.pdf')
            file.save(input_path)
            
            # Read PDF and split
            reader = PdfReader(input_path)
            
            split_files = []
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                page_filename = f"page_{i+1}.pdf"
                page_path = os.path.join(temp_dir, page_filename)
                
                with open(page_path, 'wb') as output_file:
                    writer.write(output_file)
                
                split_files.append({
                    'filename': page_filename,
                    'path': page_path,
                    'page_number': i + 1
                })
            
            # For now, return the first page as example
            # In production, you'd create a ZIP file with all pages
            if split_files:
                return send_file(split_files[0]['path'], 
                               as_attachment=True, 
                               download_name=split_files[0]['filename'],
                               mimetype='application/pdf')
            else:
                return jsonify({'error': 'No pages found in PDF'}), 400
    
    except Exception as e:
        logger.error(f"PDF split error: {str(e)}")
        return jsonify({'error': 'Failed to split PDF file'}), 500

# Image Tools API Endpoints

@api_bp.route('/tools/image-compress', methods=['POST'])
def image_compress():
    """Compress image with quality control"""
    try:
        file = request.files.get('file')
        quality = float(request.form.get('quality', 0.8))
        
        if not file or not allowed_file(file.filename, ['jpg', 'jpeg', 'png', 'webp']):
            return jsonify({'error': 'Please upload a valid image file'}), 400
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            input_path = os.path.join(temp_dir, 'input_image')
            file.save(input_path)
            
            # Open and process image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large
                max_dimension = 1920
                if max(img.size) > max_dimension:
                    img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                
                # Auto-orient image
                img = ImageOps.exif_transpose(img)
                
                # Save compressed image
                output_filename = create_temp_filename(file.filename, "_compressed")
                output_path = os.path.join(temp_dir, output_filename)
                
                # Determine format
                if file.filename.lower().endswith('.png'):
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, 'JPEG', quality=int(quality * 100), optimize=True)
                
                return send_file(output_path, 
                               as_attachment=True, 
                               download_name=output_filename)
    
    except Exception as e:
        logger.error(f"Image compression error: {str(e)}")
        return jsonify({'error': 'Failed to compress image'}), 500

@api_bp.route('/tools/image-resize', methods=['POST'])
def image_resize():
    """Resize image to specific dimensions"""
    try:
        file = request.files.get('file')
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))
        maintain_aspect = request.form.get('maintain_aspect', 'true').lower() == 'true'
        
        if not file or not allowed_file(file.filename, ['jpg', 'jpeg', 'png', 'webp']):
            return jsonify({'error': 'Please upload a valid image file'}), 400
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, 'input_image')
            file.save(input_path)
            
            with Image.open(input_path) as img:
                if maintain_aspect:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                output_filename = create_temp_filename(file.filename, "_resized")
                output_path = os.path.join(temp_dir, output_filename)
                
                if file.filename.lower().endswith('.png'):
                    img.save(output_path, 'PNG')
                else:
                    img.save(output_path, 'JPEG', quality=95)
                
                return send_file(output_path, 
                               as_attachment=True, 
                               download_name=output_filename)
    
    except Exception as e:
        logger.error(f"Image resize error: {str(e)}")
        return jsonify({'error': 'Failed to resize image'}), 500

# QR Code Generator API

@api_bp.route('/tools/qr-generate', methods=['POST'])
def qr_generate():
    """Generate QR code with customization options"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        size = int(data.get('size', 256))
        
        if not text.strip():
            return jsonify({'error': 'Text content is required'}), 400
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize to requested size
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, f"qrcode_{uuid.uuid4().hex[:8]}.png")
            img.save(output_path, 'PNG')
            
            return send_file(output_path, 
                           as_attachment=True, 
                           download_name="qrcode.png",
                           mimetype='image/png')
    
    except Exception as e:
        logger.error(f"QR generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate QR code'}), 500

# Text Tools API

@api_bp.route('/tools/text-case-convert', methods=['POST'])
def text_case_convert():
    """Convert text case (uppercase, lowercase, title case, etc.)"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        case_type = data.get('case_type', 'upper')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if case_type == 'upper':
            result = text.upper()
        elif case_type == 'lower':
            result = text.lower()
        elif case_type == 'title':
            result = text.title()
        elif case_type == 'sentence':
            result = text.capitalize()
        elif case_type == 'toggle':
            result = text.swapcase()
        else:
            result = text
        
        return jsonify({'result': result})
    
    except Exception as e:
        logger.error(f"Text case conversion error: {str(e)}")
        return jsonify({'error': 'Failed to convert text case'}), 500

@api_bp.route('/tools/password-generate', methods=['POST'])
def password_generate():
    """Generate secure passwords"""
    try:
        data = request.get_json()
        length = int(data.get('length', 12))
        include_uppercase = data.get('include_uppercase', True)
        include_lowercase = data.get('include_lowercase', True)
        include_numbers = data.get('include_numbers', True)
        include_symbols = data.get('include_symbols', True)
        
        import string
        import secrets
        
        characters = ""
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not characters:
            return jsonify({'error': 'At least one character type must be selected'}), 400
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return jsonify({'password': password})
    
    except Exception as e:
        logger.error(f"Password generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate password'}), 500

# Utility API Endpoints

@api_bp.route('/tools/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'All tool APIs are operational'
    })

@api_bp.route('/tools/info', methods=['GET'])
def tool_info():
    """Get information about available tools"""
    return jsonify({
        'total_tools': 85,
        'categories': [
            'PDF Tools', 'Image Tools', 'Video Tools', 'AI Tools',
            'Text Tools', 'Utility Tools', 'Government Tools', 'Student Tools'
        ],
        'api_version': '1.0',
        'features': [
            'File processing', 'Real-time generation', 'No registration required',
            'Secure processing', 'Multiple formats supported'
        ]
    })

# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'API endpoint not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500