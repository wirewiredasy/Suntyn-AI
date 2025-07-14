import os
import shutil
import mimetypes
from werkzeug.utils import secure_filename
import qrcode

class FileHandler:
    """Utility class for handling file operations"""
    
    ALLOWED_EXTENSIONS = {
        'pdf': ['pdf'],
        'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
        'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'],
        'audio': ['mp3', 'wav', 'ogg', 'aac', 'm4a'],
        'document': ['doc', 'docx', 'txt', 'rtf']
    }
    
    @staticmethod
    def is_allowed_file(filename, file_type):
        """Check if file extension is allowed for given type"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileHandler.ALLOWED_EXTENSIONS.get(file_type, [])
    
    @staticmethod
    def get_file_type(filename):
        """Get file type based on extension"""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        for file_type, extensions in FileHandler.ALLOWED_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        
        return 'unknown'
    
    @staticmethod
    def get_safe_filename(filename):
        """Generate safe filename"""
        return secure_filename(filename)
    
    @staticmethod
    def ensure_upload_dir():
        """Ensure upload directory exists"""
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        return upload_dir
    
    @staticmethod
    def cleanup_file(file_path):
        """Remove file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    @staticmethod
    def get_mime_type(file_path):
        """Get MIME type of file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'

    @staticmethod
    def generate_qr_code(content, size=300, format='PNG'):
        """Generate QR code"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))

        os.makedirs('uploads', exist_ok=True)
        output_filename = f"qr_code_{hash(content) % 10000}.{format.lower()}"
        output_path = os.path.join('uploads', output_filename)

        img.save(output_path)
        return output_path