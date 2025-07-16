import os
import random
import string
import qrcode
from io import BytesIO
from PIL import Image

def generate_password(length=12, include_uppercase=True, include_lowercase=True, include_numbers=True, include_symbols=True):
    """Generate secure password"""
    try:
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
            return None
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        print(f"Error generating password: {e}")
        return None

def generate_qr_code(text, output_path, size=256, color='#000000', bg_color='#ffffff'):
    """Generate QR code"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Convert hex colors to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        fill_color = hex_to_rgb(color)
        back_color = hex_to_rgb(bg_color)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Resize if needed
        if img.size[0] != size:
            img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return False

def convert_text_case(text, case_type='upper'):
    """Convert text case"""
    try:
        if case_type == 'upper':
            return text.upper()
        elif case_type == 'lower':
            return text.lower()
        elif case_type == 'title':
            return text.title()
        elif case_type == 'sentence':
            return text.capitalize()
        elif case_type == 'toggle':
            return text.swapcase()
        else:
            return text
    except Exception as e:
        print(f"Error converting text case: {e}")
        return text

def calculate_bmi(weight, height):
    """Calculate BMI"""
    try:
        # Assuming weight in kg and height in meters
        bmi = weight / (height ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        return {
            'bmi': round(bmi, 2),
            'category': category
        }
    except Exception as e:
        print(f"Error calculating BMI: {e}")
        return None

def calculate_age(birth_date):
    """Calculate age from birth date"""
    try:
        from datetime import datetime
        today = datetime.now()
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        
        age = today.year - birth.year
        if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
            age -= 1
        
        return age
    except Exception as e:
        print(f"Error calculating age: {e}")
        return None

def shorten_url(long_url, custom_code=None):
    """Generate shortened URL (placeholder implementation)"""
    try:
        # In production, you'd use a URL shortening service
        # This is a simple placeholder
        
        if custom_code:
            short_code = custom_code
        else:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        # Store mapping in database (placeholder)
        shortened_url = f"https://short.ly/{short_code}"
        
        return {
            'short_url': shortened_url,
            'short_code': short_code,
            'original_url': long_url
        }
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return None