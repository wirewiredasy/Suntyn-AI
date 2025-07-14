
import os
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename

class ImageProcessor:
    @staticmethod
    def compress_image(file, quality=85, format='JPEG'):
        """Compress image file"""
        image = Image.open(file)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"compressed_{name}.{format.lower()}"
        output_path = os.path.join('uploads', output_filename)
        
        image.save(output_path, format=format, quality=quality, optimize=True)
        return output_path
    
    @staticmethod
    def resize_image(file, width, height, maintain_aspect=True):
        """Resize image"""
        image = Image.open(file)
        
        if maintain_aspect:
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"resized_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)
        
        image.save(output_path)
        return output_path
    
    @staticmethod
    def convert_image(file, format='PNG'):
        """Convert image format"""
        image = Image.open(file)
        
        # Convert to RGB for JPEG
        if format.upper() == 'JPEG' and image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"converted_{name}.{format.lower()}"
        output_path = os.path.join('uploads', output_filename)
        
        image.save(output_path, format=format.upper())
        return output_path
    
    @staticmethod
    def crop_image(file, x, y, width, height):
        """Crop image"""
        image = Image.open(file)
        cropped = image.crop((x, y, x + width, y + height))
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"cropped_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)
        
        cropped.save(output_path)
        return output_path
    
    @staticmethod
    def rotate_image(file, angle):
        """Rotate image"""
        image = Image.open(file)
        rotated = image.rotate(angle, expand=True)
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"rotated_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)
        
        rotated.save(output_path)
        return output_path
    
    @staticmethod
    def add_watermark(file, watermark_text, position='bottom-right', opacity=0.7):
        """Add text watermark to image"""
        image = Image.open(file)
        
        # Create transparent overlay
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position watermark
        if position == 'bottom-right':
            x = image.width - text_width - 10
            y = image.height - text_height - 10
        elif position == 'bottom-left':
            x = 10
            y = image.height - text_height - 10
        elif position == 'top-right':
            x = image.width - text_width - 10
            y = 10
        elif position == 'top-left':
            x = 10
            y = 10
        else:  # center
            x = (image.width - text_width) // 2
            y = (image.height - text_height) // 2
        
        # Draw watermark
        alpha = int(255 * opacity)
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, alpha))
        
        # Composite
        watermarked = Image.alpha_composite(image.convert('RGBA'), overlay)
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"watermarked_{name}.png"
        output_path = os.path.join('uploads', output_filename)
        
        watermarked.save(output_path)
        return output_path
    
    @staticmethod
    def remove_background(file):
        """Remove background from image (simple version)"""
        # This is a simplified version - for real background removal, 
        # you'd need a more sophisticated library like rembg
        image = Image.open(file)
        
        # Convert to RGBA
        image = image.convert('RGBA')
        
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"no_bg_{name}.png"
        output_path = os.path.join('uploads', output_filename)
        
        image.save(output_path)
        return output_path
