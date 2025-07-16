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
def compress_pdf_files():
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
def compress_image_files():
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
def resize_image_files():
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
def convert_image_files():
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
def extract_audio_files():
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
def trim_video_files():
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
def compress_image_files():
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
def resize_image_files():
    """Resize image file"""
    try:
        file = request.files['file']
        width = request.form.get('width')
        height = request.form.get('height')

        if not width and not height:
            return jsonify({'error': 'Width or height required'}), 400

        width = int(width) if width else None
        height = int(height) if height else None

        from utils.image_tools import ImageProcessor

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Resize image
        output_path = ImageProcessor.resize_image(temp_path, width, height)

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
def convert_image_files():
    """Convert image to different format"""
    try:
        file = request.files['file']
        output_format = request.form.get('format', 'PNG')

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
def extract_audio_files():
    """Extract audio from video"""
    try:
        file = request.files['file']
        audio_format = request.form.get('format', 'mp3')

        from utils.video_tools import extract_audio

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Extract audio
        output_filename = f"audio_{uuid.uuid4()}.{audio_format}"
        output_path = os.path.join('uploads', output_filename)

        success = extract_audio(temp_path, output_path, audio_format)

        if success:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to extract audio'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/video/trim', methods=['POST'])
def trim_video_files():
    """Trim video file"""
    try:
        file = request.files['file']
        start_time = request.form.get('start_time', '00:00:00')
        end_time = request.form.get('end_time', '00:01:00')

        from utils.video_tools import trim_video

        # Save uploaded file
        temp_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        temp_path = os.path.join('uploads', temp_filename)
        file.save(temp_path)

        # Trim video
        output_filename = f"trimmed_{uuid.uuid4()}.mp4"
        output_path = os.path.join('uploads', output_filename)

        success = trim_video(temp_path, output_path, start_time, end_time)

        if success:
            return jsonify({
                'success': True,
                'download_url': f'/api/download/{output_filename}',
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Failed to trim video'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Utility Tools
@api_bp.route('/utility/qr-code', methods=['POST'])
def generate_qr_code():
    """Generate QR code"""
    try:
        content = request.form.get('content', '')
        size = int(request.form.get('size', 300))

        if not content:
            return jsonify({'error': 'Content is required'}), 400

        # Generate QR code
        import qrcode

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size//25,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code
        output_filename = f"qr_{uuid.uuid4()}.png"
        output_path = os.path.join('uploads', output_filename)

        os.makedirs('uploads', exist_ok=True)
        img.save(output_path, 'PNG')

        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Tools
@api_bp.route('/ai/resume', methods=['POST'])
def generate_resume():
    """Generate resume using AI"""
    try:
        from utils.ai_tools import AIProcessor

        # Get form data
        data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'summary': request.form.get('summary', ''),
            'skills': request.form.get('skills', '').split(',') if request.form.get('skills') else [],
            'experience': [],
            'education': []
        }

        # Generate resume
        output_path = AIProcessor.generate_resume(data)

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

@api_bp.route('/ai/business-names', methods=['POST'])
def generate_business_names():
    """Generate business name suggestions"""
    try:
        from utils.ai_tools import AIProcessor

        industry = request.form.get('industry', '')
        keywords = request.form.get('keywords', '').split(',')
        count = int(request.form.get('count', 10))

        # Generate business names
        business_names = AIProcessor.generate_business_names(industry, keywords, count)

        return jsonify({
            'success': True,
            'business_names': business_names
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/blog-titles', methods=['POST'])
def generate_blog_titles():
    """Generate blog title suggestions"""
    try:
        from utils.ai_tools import AIProcessor

        topic = request.form.get('topic', '')
        keywords = request.form.get('keywords', '').split(',')
        count = int(request.form.get('count', 10))

        # Generate blog titles
        blog_titles = AIProcessor.generate_blog_titles(topic, keywords, count)

        return jsonify({
            'success': True,
            'blog_titles': blog_titles
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/product-description', methods=['POST'])
def generate_product_description():
    """Generate product description"""
    try:
        from utils.ai_tools import AIProcessor

        product_name = request.form.get('product_name', '')
        features = request.form.get('features', '').split(',')
        benefits = request.form.get('benefits', '').split(',')
        target_audience = request.form.get('target_audience', '')

        # Generate product description
        description = AIProcessor.generate_product_description(
            product_name, features, benefits, target_audience
        )

        return jsonify({
            'success': True,
            'description': description
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/ad-copy', methods=['POST'])
def generate_ad_copy():
    """Generate advertisement copy"""
    try:
        from utils.ai_tools import AIProcessor

        product = request.form.get('product', '')
        target_audience = request.form.get('target_audience', '')
        tone = request.form.get('tone', 'professional')
        length = request.form.get('length', 'short')

        # Generate ad copy
        ad_copy = AIProcessor.generate_ad_copy(product, target_audience, tone, length)

        return jsonify({
            'success': True,
            'ad_copy': ad_copy
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ai/faq', methods=['POST'])
def generate_faq():
    """Generate FAQ"""
    try:
        from utils.ai_tools import AIProcessor

        topic = request.form.get('topic', '')
        questions_count = int(request.form.get('questions_count', 10))

        # Generate FAQ
        faq_list = AIProcessor.generate_faq(topic, questions_count)

        return jsonify({
            'success': True,
            'faq': faq_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Generic tool processor
@api_bp.route('/tools/<category>/<tool_name>', methods=['POST'])
def process_generic_tool(category, tool_name):
    """Generic tool processing endpoint"""
    try:
        # Handle file uploads
        files = request.files.getlist('files')

        # Log tool usage
        user = get_current_user()
        if user:
            history = ToolHistory(
                user_id=user.id,
                tool_name=tool_name,
                tool_category=category,
                file_count=len(files)
            )
            db.session.add(history)
            db.session.commit()

        # For now, return a success message with demo processing
        return jsonify({
            'success': True,
            'message': f'Tool {tool_name} processed successfully',
            'tool_name': tool_name,
            'category': category,
            'files_processed': len(files)
        })

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

@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()

        # Log feedback to console (in production, save to database)
        print(f"FEEDBACK: Type={data.get('type')}, Message={data.get('message')}, URL={data.get('url')}")

        # Here you would save to database
        # feedback = Feedback(
        #     type=data.get('type'),
        #     message=data.get('message'),
        #     url=data.get('url'),
        #     user_agent=data.get('userAgent'),
        #     timestamp=datetime.utcnow()
        # )
        # db.session.add(feedback)
        # db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics', methods=['POST'])
def track_analytics():
    """Track user analytics"""
    try:
        data = request.get_json()

        # Log analytics (in production, save to database)
        print(f"ANALYTICS: Action={data.get('action')}, Tool={data.get('tool')}, Category={data.get('category')}")

        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/tool-feedback', methods=['POST'])
def submit_tool_feedback():
    """Submit tool-specific feedback"""
    try:
        data = request.get_json()

        # Log tool feedback to console (in production, save to database)
        print(f"TOOL FEEDBACK: Tool={data.get('tool_name')}, Category={data.get('tool_category')}, Rating={data.get('rating')}")
        print(f"Type={data.get('type')}, Message={data.get('message')}")

        # Here you would save to database
        # tool_feedback = ToolFeedback(
        #     tool_name=data.get('tool_name'),
        #     tool_category=data.get('tool_category'),
        #     rating=data.get('rating'),
        #     type=data.get('type'),
        #     message=data.get('message'),
        #     url=data.get('url'),
        #     timestamp=datetime.utcnow()
        # )
        # db.session.add(tool_feedback)
        # db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Tool feedback submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@api_bp.route('/contact', methods=['POST'])
def contact_form():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Log the contact form submission
        logging.info(f"Contact form submission from {data['email']} - Subject: {data['subject']}")

        # Here you would typically send an email or save to database
        # For now, we'll just log the submission
        contact_info = {
            'name': f"{data['firstName']} {data['lastName']}",
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'newsletter': data.get('newsletter', False)
        }

        print(f"New contact form submission: {contact_info}")

        return jsonify({
            'status': 'success', 
            'message': 'Thank you for your message! We will get back to you soon.'
        }), 200

    except Exception as e:
        logging.error(f"Contact form error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500