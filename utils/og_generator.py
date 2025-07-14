"""
OG Image Generator for Toolora AI
Generates social media preview images for each tool
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

class OGImageGenerator:
    def __init__(self):
        self.width = 1200
        self.height = 630
        self.output_dir = "static/images/og"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Brand colors
        self.purple = (139, 92, 246)
        self.cyan = (6, 182, 212)
        self.emerald = (16, 185, 129)
        
    def create_gradient_bg(self):
        """Create gradient background"""
        img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Create gradient
        for y in range(self.height):
            # Interpolate between purple and cyan
            ratio = y / self.height
            r = int(self.purple[0] + (self.cyan[0] - self.purple[0]) * ratio)
            g = int(self.purple[1] + (self.cyan[1] - self.purple[1]) * ratio)
            b = int(self.purple[2] + (self.cyan[2] - self.purple[2]) * ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
        
    def get_font(self, size):
        """Get font with fallback"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        
        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
            except:
                continue
        
        return ImageFont.load_default()
    
    def generate_tool_og_image(self, tool_name, tool_description, category_name):
        """Generate OG image for a specific tool"""
        # Create gradient background
        img = self.create_gradient_bg()
        
        # Add semi-transparent overlay
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 120))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        
        draw = ImageDraw.Draw(img)
        
        # Fonts
        title_font = self.get_font(64)
        subtitle_font = self.get_font(32)
        desc_font = self.get_font(24)
        brand_font = self.get_font(40)
        
        # Brand name
        brand_text = "Toolora AI"
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = brand_bbox[2] - brand_bbox[0]
        draw.text((50, 50), brand_text, font=brand_font, fill=(255, 255, 255))
        
        # Tool name
        tool_display_name = tool_name.replace('-', ' ').title()
        title_bbox = draw.textbbox((0, 0), tool_display_name, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        
        title_x = (self.width - title_width) // 2
        title_y = 200
        draw.text((title_x, title_y), tool_display_name, font=title_font, fill=(255, 255, 255))
        
        # Category badge
        category_text = f"📁 {category_name}"
        category_bbox = draw.textbbox((0, 0), category_text, font=subtitle_font)
        category_width = category_bbox[2] - category_bbox[0]
        category_x = (self.width - category_width) // 2
        category_y = title_y + title_height + 20
        
        # Category background
        draw.rounded_rectangle([category_x - 20, category_y - 10, category_x + category_width + 20, category_y + 40], 
                             radius=20, fill=(255, 255, 255, 80))
        draw.text((category_x, category_y), category_text, font=subtitle_font, fill=(255, 255, 255))
        
        # Description
        if tool_description:
            wrapped_desc = textwrap.fill(tool_description, width=60)
            desc_lines = wrapped_desc.split('\n')
            
            desc_y = category_y + 80
            for line in desc_lines:
                desc_bbox = draw.textbbox((0, 0), line, font=desc_font)
                desc_width = desc_bbox[2] - desc_bbox[0]
                desc_x = (self.width - desc_width) // 2
                draw.text((desc_x, desc_y), line, font=desc_font, fill=(255, 255, 255, 200))
                desc_y += 30
        
        # Bottom branding
        footer_text = "Free • Fast • Secure • 85+ Tools"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=subtitle_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        footer_x = (self.width - footer_width) // 2
        draw.text((footer_x, self.height - 100), footer_text, font=subtitle_font, fill=(255, 255, 255, 180))
        
        # Save image
        filename = f"{tool_name}-og.png"
        filepath = os.path.join(self.output_dir, filename)
        img.convert('RGB').save(filepath, "PNG", optimize=True)
        
        return filepath
        
    def generate_default_og_image(self):
        """Generate default OG image for main pages"""
        img = self.create_gradient_bg()
        
        # Add semi-transparent overlay
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 100))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        
        draw = ImageDraw.Draw(img)
        
        # Fonts
        title_font = self.get_font(72)
        subtitle_font = self.get_font(36)
        desc_font = self.get_font(28)
        
        # Main title
        title_text = "Toolora AI"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        title_x = (self.width - title_width) // 2
        title_y = 180
        draw.text((title_x, title_y), title_text, font=title_font, fill=(255, 255, 255))
        
        # Subtitle
        subtitle_text = "One Place. All Tools."
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (self.width - subtitle_width) // 2
        subtitle_y = title_y + title_height + 20
        draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill=(255, 255, 255, 200))
        
        # Description
        desc_text = "85+ Professional Tools for PDF, Image, Video, AI & More"
        desc_bbox = draw.textbbox((0, 0), desc_text, font=desc_font)
        desc_width = desc_bbox[2] - desc_bbox[0]
        desc_x = (self.width - desc_width) // 2
        desc_y = subtitle_y + 80
        draw.text((desc_x, desc_y), desc_text, font=desc_font, fill=(255, 255, 255, 180))
        
        # Features
        features_text = "🚀 Fast • 🔒 Secure • 🆓 Free • 🌐 No Sign-up Required"
        features_bbox = draw.textbbox((0, 0), features_text, font=desc_font)
        features_width = features_bbox[2] - features_bbox[0]
        features_x = (self.width - features_width) // 2
        draw.text((features_x, self.height - 100), features_text, font=desc_font, fill=(255, 255, 255, 160))
        
        # Save image
        filepath = os.path.join(self.output_dir, "default-og.png")
        img.convert('RGB').save(filepath, "PNG", optimize=True)
        
        return filepath

# Generate default OG image on import
if __name__ == "__main__":
    generator = OGImageGenerator()
    generator.generate_default_og_image()
    print("Default OG image generated successfully!")