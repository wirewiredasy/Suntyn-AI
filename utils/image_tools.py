import os
from PIL import Image, ImageEnhance, ImageFilter
import io

def compress_image(input_path, output_path, quality=85):
    """Compress image file"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save with compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return True
    except Exception as e:
        print(f"Error compressing image: {e}")
        return False

def resize_image(input_path, output_path, width, height, maintain_aspect=True):
    """Resize image to specified dimensions"""
    try:
        with Image.open(input_path) as img:
            if maintain_aspect:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            img.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False

def convert_image(input_path, output_path, output_format):
    """Convert image to different format"""
    try:
        with Image.open(input_path) as img:
            # Handle transparency for formats that don't support it
            if output_format.upper() in ['JPEG', 'JPG'] and img.mode in ('RGBA', 'LA'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.save(output_path, output_format.upper())
        
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def crop_image(input_path, output_path, x, y, width, height):
    """Crop image to specified rectangle"""
    try:
        with Image.open(input_path) as img:
            cropped = img.crop((x, y, x + width, y + height))
            cropped.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error cropping image: {e}")
        return False

def flip_image(input_path, output_path, direction='horizontal'):
    """Flip image horizontally or vertically"""
    try:
        with Image.open(input_path) as img:
            if direction == 'horizontal':
                flipped = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            else:
                flipped = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            
            flipped.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error flipping image: {e}")
        return False

def rotate_image(input_path, output_path, angle=90):
    """Rotate image by specified angle"""
    try:
        with Image.open(input_path) as img:
            rotated = img.rotate(angle, expand=True)
            rotated.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error rotating image: {e}")
        return False

def add_watermark_image(input_path, output_path, watermark_text, position='bottom-right'):
    """Add text watermark to image"""
    try:
        from PIL import ImageDraw, ImageFont
        
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            if position == 'bottom-right':
                x = img.width - text_width - 10
                y = img.height - text_height - 10
            elif position == 'bottom-left':
                x = 10
                y = img.height - text_height - 10
            elif position == 'top-right':
                x = img.width - text_width - 10
                y = 10
            else:  # top-left
                x = 10
                y = 10
            
            # Draw text with shadow
            draw.text((x + 2, y + 2), watermark_text, font=font, fill=(0, 0, 0, 128))
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 200))
            
            img.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error adding watermark: {e}")
        return False

def enhance_image(input_path, output_path, brightness=1.0, contrast=1.0, saturation=1.0):
    """Enhance image brightness, contrast, and saturation"""
    try:
        with Image.open(input_path) as img:
            # Apply enhancements
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            img.save(output_path)
        
        return True
    except Exception as e:
        print(f"Error enhancing image: {e}")
        return False
