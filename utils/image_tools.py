"""
Image processing utilities for Toolora AI
Handles image compression, resizing, format conversion, and other operations
"""

import os
import uuid
from PIL import Image, ImageEnhance, ImageFilter
import tempfile
import logging

class ImageProcessor:
    """Image processing utilities"""
    
    @staticmethod
    def compress_image(input_file, quality=85):
        """Compress image file"""
        try:
            with Image.open(input_file) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Generate output filename
                file_ext = os.path.splitext(input_file)[1].lower()
                if file_ext not in ['.jpg', '.jpeg']:
                    file_ext = '.jpg'
                
                output_filename = f"compressed_{uuid.uuid4()}{file_ext}"
                output_path = os.path.join('uploads', output_filename)
                
                # Ensure uploads directory exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save compressed image
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                
                return output_path
                
        except Exception as e:
            logging.error(f"Image compress error: {str(e)}")
            return None
    
    @staticmethod
    def resize_image(input_file, width=None, height=None, maintain_aspect=True):
        """Resize image file"""
        try:
            with Image.open(input_file) as img:
                original_width, original_height = img.size
                
                if width and height and not maintain_aspect:
                    new_size = (width, height)
                elif width and maintain_aspect:
                    aspect_ratio = original_height / original_width
                    new_size = (width, int(width * aspect_ratio))
                elif height and maintain_aspect:
                    aspect_ratio = original_width / original_height
                    new_size = (int(height * aspect_ratio), height)
                else:
                    new_size = (original_width // 2, original_height // 2)
                
                # Resize image
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Generate output filename
                file_ext = os.path.splitext(input_file)[1].lower()
                output_filename = f"resized_{uuid.uuid4()}{file_ext}"
                output_path = os.path.join('uploads', output_filename)
                
                # Ensure uploads directory exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save resized image
                resized_img.save(output_path)
                
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                
                return output_path
                
        except Exception as e:
            logging.error(f"Image resize error: {str(e)}")
            return None
    
    @staticmethod
    def convert_image(input_file, output_format='JPEG'):
        """Convert image to different format"""
        try:
            with Image.open(input_file) as img:
                # Convert format
                if output_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Generate output filename
                format_extensions = {
                    'JPEG': '.jpg',
                    'PNG': '.png',
                    'WEBP': '.webp',
                    'BMP': '.bmp'
                }
                
                file_ext = format_extensions.get(output_format.upper(), '.jpg')
                output_filename = f"converted_{uuid.uuid4()}{file_ext}"
                output_path = os.path.join('uploads', output_filename)
                
                # Ensure uploads directory exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save converted image
                save_kwargs = {}
                if output_format.upper() == 'JPEG':
                    save_kwargs['quality'] = 90
                    save_kwargs['optimize'] = True
                
                img.save(output_path, output_format.upper(), **save_kwargs)
                
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                
                return output_path
                
        except Exception as e:
            logging.error(f"Image convert error: {str(e)}")
            return None
    
    @staticmethod
    def crop_image(input_file, left=0, top=0, right=None, bottom=None):
        """Crop image"""
        try:
            with Image.open(input_file) as img:
                width, height = img.size
                
                # Default crop to center if not specified
                if right is None:
                    right = width
                if bottom is None:
                    bottom = height
                
                # Crop image
                cropped_img = img.crop((left, top, right, bottom))
                
                # Generate output filename
                file_ext = os.path.splitext(input_file)[1].lower()
                output_filename = f"cropped_{uuid.uuid4()}{file_ext}"
                output_path = os.path.join('uploads', output_filename)
                
                # Ensure uploads directory exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save cropped image
                cropped_img.save(output_path)
                
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                
                return output_path
                
        except Exception as e:
            logging.error(f"Image crop error: {str(e)}")
            return None
    
    @staticmethod
    def enhance_image(input_file, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
        """Enhance image with brightness, contrast, saturation, and sharpness"""
        try:
            with Image.open(input_file) as img:
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
                
                if sharpness != 1.0:
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(sharpness)
                
                # Generate output filename
                file_ext = os.path.splitext(input_file)[1].lower()
                output_filename = f"enhanced_{uuid.uuid4()}{file_ext}"
                output_path = os.path.join('uploads', output_filename)
                
                # Ensure uploads directory exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save enhanced image
                img.save(output_path)
                
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                
                return output_path
                
        except Exception as e:
            logging.error(f"Image enhance error: {str(e)}")
            return None