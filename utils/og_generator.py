"""
OG Image Generator for Toolora AI
Generates social media preview images with the new logo
"""

from PIL import Image, ImageDraw, ImageFont
import os
import io
import base64

def generate_og_image(title, description="Professional tools for creators", tool_category=None):
    """
    Generate OG image with enhanced Toolora branding
    """
    # Image dimensions for social media
    width, height = 1200, 630
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        gradient_ratio = y / height
        r = int(139 * (1 - gradient_ratio) + 16 * gradient_ratio)  # Purple to dark
        g = int(92 * (1 - gradient_ratio) + 185 * gradient_ratio)   # Purple to emerald
        b = int(246 * (1 - gradient_ratio) + 129 * gradient_ratio)  # Purple to emerald
        
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add subtle pattern overlay
    for x in range(0, width, 40):
        for y in range(0, height, 40):
            draw.ellipse([x, y, x+2, y+2], fill=(255, 255, 255, 20))
    
    # Load or create logo
    try:
        logo_path = os.path.join('static', 'images', 'toolora-logo.svg')
        if os.path.exists(logo_path):
            # In a real implementation, you'd convert SVG to PIL Image
            # For now, we'll create a simple logo representation
            pass
    except:
        pass
    
    # Create logo representation
    logo_size = 120
    logo_x = 60
    logo_y = 60
    
    # Draw logo background circle
    draw.ellipse([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], 
                fill=(255, 255, 255, 240))
    
    # Draw T letter
    t_color = (139, 92, 246)  # Purple
    t_size = 80
    t_x = logo_x + (logo_size - t_size) // 2
    t_y = logo_y + (logo_size - t_size) // 2
    
    # T horizontal bar
    draw.rectangle([t_x, t_y, t_x + t_size, t_y + 15], fill=t_color)
    # T vertical bar
    draw.rectangle([t_x + t_size//2 - 10, t_y, t_x + t_size//2 + 10, t_y + t_size], fill=t_color)
    
    # Add title text
    try:
        title_font = ImageFont.truetype("Arial", 64)
        subtitle_font = ImageFont.truetype("Arial", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Title
    title_x = logo_x + logo_size + 40
    title_y = logo_y + 10
    draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)
    
    # Subtitle
    draw.text((title_x, title_y + 80), description, fill=(200, 200, 200), font=subtitle_font)
    
    # Add category badge if provided
    if tool_category:
        badge_x = title_x
        badge_y = title_y + 140
        badge_width = 200
        badge_height = 40
        
        # Badge background
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_width, badge_y + badge_height], 
                             radius=20, fill=(6, 182, 212))
        
        # Badge text
        draw.text((badge_x + 20, badge_y + 8), tool_category.title(), 
                 fill=(255, 255, 255), font=subtitle_font)
    
    # Add bottom branding
    brand_text = "Toolora AI - Professional Tools Platform"
    brand_y = height - 60
    draw.text((60, brand_y), brand_text, fill=(160, 160, 160), font=subtitle_font)
    
    return img

def save_og_image(img, filename):
    """Save OG image to static folder"""
    og_dir = os.path.join('static', 'images', 'og')
    os.makedirs(og_dir, exist_ok=True)
    
    filepath = os.path.join(og_dir, filename)
    img.save(filepath, 'PNG', optimize=True)
    
    return filepath

def generate_tool_og_image(tool_name, category):
    """Generate OG image for specific tool"""
    title = tool_name.replace('-', ' ').title()
    description = f"Professional {category} tool - Free online"
    
    img = generate_og_image(title, description, category)
    filename = f"{tool_name}-og.png"
    
    return save_og_image(img, filename)

def generate_category_og_image(category_name, tool_count):
    """Generate OG image for tool category"""
    title = f"{category_name} Tools"
    description = f"{tool_count} professional tools available"
    
    img = generate_og_image(title, description, category_name)
    filename = f"{category_name}-category-og.png"
    
    return save_og_image(img, filename)