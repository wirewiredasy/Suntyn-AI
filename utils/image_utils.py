import os
from PIL import Image, ImageOps
import io

def compress_image(input_file, output_path, quality=80):
    """Compress image with specified quality"""
    try:
        with Image.open(input_file) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Get original size
            original_size = os.path.getsize(input_file)
            
            # Save with compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get compressed size
            compressed_size = os.path.getsize(output_path)
            
            return True, original_size, compressed_size
    except Exception as e:
        print(f"Error compressing image: {e}")
        return False, 0, 0

def resize_image(input_file, output_path, width, height, maintain_aspect=True):
    """Resize image to specified dimensions"""
    try:
        with Image.open(input_file) as img:
            if maintain_aspect:
                # Calculate aspect ratio
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                # Resize without maintaining aspect ratio
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save resized image
            img.save(output_path, 'JPEG', quality=95)
            
            return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False

def remove_background(input_file, output_path):
    """Remove background from image (placeholder implementation)"""
    try:
        # This is a placeholder - in production you'd use AI services
        # or libraries like rembg
        with Image.open(input_file) as img:
            # Convert to RGBA for transparency
            img = img.convert('RGBA')
            
            # Simple color-based background removal (very basic)
            # In production, use proper AI-based background removal
            
            img.save(output_path, 'PNG')
            return True
    except Exception as e:
        print(f"Error removing background: {e}")
        return False

def convert_image_format(input_file, output_path, output_format):
    """Convert image to different format"""
    try:
        with Image.open(input_file) as img:
            # Handle different formats
            if output_format.upper() == 'JPEG':
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
            elif output_format.upper() == 'PNG':
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            
            img.save(output_path, output_format.upper())
            return True
    except Exception as e:
        print(f"Error converting image format: {e}")
        return False