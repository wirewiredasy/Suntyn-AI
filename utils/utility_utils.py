"""
Utility processing functions for various tools
"""
import os
import uuid
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tempfile
import logging

class UtilityProcessor:
    """Utility processing functions"""

    @staticmethod
    def generate_qr_code(content, qr_type='url', size=300):
        """Generate QR code image"""
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # Add content based on type
            if qr_type == 'url':
                if not content.startswith(('http://', 'https://')):
                    content = 'https://' + content
            elif qr_type == 'wifi':
                # Format: WIFI:T:WPA;S:NetworkName;P:Password;;
                parts = content.split(',')
                if len(parts) >= 2:
                    ssid = parts[0].strip()
                    password = parts[1].strip()
                    content = f"WIFI:T:WPA;S:{ssid};P:{password};;"
            elif qr_type == 'contact':
                # Basic vCard format
                lines = content.split('\n')
                name = lines[0] if lines else content
                content = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nEND:VCARD"

            qr.add_data(content)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color="black", back_color="white")

            # Resize to specified size
            img = img.resize((size, size), Image.Resampling.LANCZOS)

            # Generate output filename
            output_filename = f"qr_code_{uuid.uuid4()}.png"
            output_path = os.path.join('uploads', output_filename)

            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)

            # Save image
            img.save(output_path, 'PNG')

            return output_path

        except Exception as e:
            logging.error(f"QR code generation error: {str(e)}")
            return None

    @staticmethod
    def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                         include_numbers=True, include_symbols=True):
        """Generate secure password"""
        try:
            import random
            import string

            characters = ""
            if include_lowercase:
                characters += string.ascii_lowercase
            if include_uppercase:
                characters += string.ascii_uppercase
            if include_numbers:
                characters += string.digits
            if include_symbols:
                characters += "!@#$%^&*"

            if not characters:
                characters = string.ascii_letters + string.digits

            password = ''.join(random.choice(characters) for _ in range(length))
            return password

        except Exception as e:
            logging.error(f"Password generation error: {str(e)}")
            return None

    @staticmethod
    def convert_text_case(text, case_type):
        """Convert text case"""
        try:
            if case_type == 'uppercase':
                return text.upper()
            elif case_type == 'lowercase':
                return text.lower()
            elif case_type == 'title':
                return text.title()
            elif case_type == 'sentence':
                sentences = text.split('. ')
                return '. '.join(s.capitalize() for s in sentences)
            elif case_type == 'camel':
                words = text.split()
                return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
            elif case_type == 'pascal':
                words = text.split()
                return ''.join(word.capitalize() for word in words)
            elif case_type == 'snake':
                return text.lower().replace(' ', '_')
            elif case_type == 'kebab':
                return text.lower().replace(' ', '-')
            else:
                return text

        except Exception as e:
            logging.error(f"Text case conversion error: {str(e)}")
            return text
`