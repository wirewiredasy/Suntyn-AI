import os
from werkzeug.utils import secure_filename
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import random

class AIProcessor:
    @staticmethod
    def generate_resume(data):
        """Generate resume from data"""
        # Placeholder HTML resume
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume - {data.get('name', 'Unknown')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .section {{ margin-bottom: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{data.get('name', 'Your Name')}</h1>
                <p>{data.get('email', 'email@example.com')} | {data.get('phone', '+1234567890')}</p>
            </div>
            <div class="section">
                <h2>Professional Summary</h2>
                <p>Professional seeking new opportunities in technology.</p>
            </div>
            <div class="section">
                <h2>Experience</h2>
                <p>Work experience details...</p>
            </div>
            <div class="section">
                <h2>Education</h2>
                <p>Educational background...</p>
            </div>
        </body>
        </html>
        """

        os.makedirs('uploads', exist_ok=True)
        output_filename = f"resume_{data.get('name', 'user').replace(' ', '_')}.html"
        output_path = os.path.join('uploads', output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path

    @staticmethod
    def generate_business_names(data):
        """Generate business names"""
        # Placeholder business names
        names = [
            f"{data.get('industry', 'Tech')} Solutions",
            f"Smart {data.get('industry', 'Tech')}",
            f"{data.get('industry', 'Tech')} Pro",
            f"Digital {data.get('industry', 'Tech')}",
            f"{data.get('industry', 'Tech')} Hub"
        ]
        return names

    @staticmethod
    def generate_blog_titles(data):
        """Generate blog titles"""
        topic = data.get('topic', 'Technology')
        titles = [
            f"10 Amazing {topic} Tips You Need to Know",
            f"The Ultimate Guide to {topic}",
            f"How {topic} is Changing the World",
            f"5 Secrets About {topic} Revealed",
            f"The Future of {topic}: What to Expect"
        ]
        return titles

    @staticmethod
    def generate_product_description(data):
        """Generate product description"""
        product = data.get('product_name', 'Product')
        features = data.get('features', [])

        description = f"""
        Introducing {product} - the perfect solution for your needs!

        Key Features:
        {chr(10).join(f"• {feature}" for feature in features)}

        Experience the difference with {product}. Order now and transform your experience!
        """
        return description.strip()

    @staticmethod
    def generate_ad_copy(data):
        """Generate advertising copy"""
        product = data.get('product', 'Our Product')
        target = data.get('target_audience', 'everyone')

        copy = f"""
        🚀 Attention {target}! 

        Discover {product} - the game-changer you've been waiting for!

        ✅ Premium Quality
        ✅ Fast Results  
        ✅ Money-Back Guarantee

        Don't miss out! Limited time offer.

        Act now and transform your life with {product}!
        """
        return copy.strip()