"""
AI processing utilities for Toolora AI
Handles AI-powered text generation and document creation
"""

import os
import uuid
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import tempfile
import logging

class AIProcessor:
    """AI processing utilities"""
    
    @staticmethod
    def generate_resume(name, experience, skills):
        """Generate a professional resume PDF"""
        try:
            # Generate output filename
            output_filename = f"resume_{uuid.uuid4()}.pdf"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph(f"<b>{name}</b>", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Experience section
            exp_title = Paragraph("<b>Experience</b>", styles['Heading2'])
            story.append(exp_title)
            exp_content = Paragraph(experience, styles['Normal'])
            story.append(exp_content)
            story.append(Spacer(1, 12))
            
            # Skills section
            skills_title = Paragraph("<b>Skills</b>", styles['Heading2'])
            story.append(skills_title)
            skills_content = Paragraph(skills, styles['Normal'])
            story.append(skills_content)
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            logging.error(f"Resume generation error: {str(e)}")
            return None
    
    @staticmethod
    def generate_business_names(industry, keywords):
        """Generate business name suggestions"""
        try:
            # Simple business name generation logic
            prefixes = ['Smart', 'Pro', 'Digital', 'Tech', 'Quick', 'Elite', 'Prime']
            suffixes = ['Solutions', 'Systems', 'Works', 'Hub', 'Lab', 'Studio', 'Group']
            
            business_names = []
            
            # Generate combinations
            for prefix in prefixes[:3]:
                for suffix in suffixes[:3]:
                    name = f"{prefix} {industry} {suffix}"
                    business_names.append(name)
            
            # Add keyword-based names if provided
            if keywords:
                keyword_list = keywords.split(',')
                for keyword in keyword_list[:2]:
                    keyword = keyword.strip()
                    business_names.append(f"{keyword} {industry} Solutions")
                    business_names.append(f"{industry} {keyword} Hub")
            
            return business_names[:10]  # Return top 10
            
        except Exception as e:
            logging.error(f"Business name generation error: {str(e)}")
            return ["TechCorp Solutions", "Digital Innovations", "Smart Systems Hub"]
    
    @staticmethod
    def generate_blog_titles(topic, keywords=""):
        """Generate blog title suggestions"""
        try:
            titles = [
                f"The Ultimate Guide to {topic}",
                f"10 Essential Tips for {topic}",
                f"How to Master {topic} in 2025",
                f"Everything You Need to Know About {topic}",
                f"The Future of {topic}: Trends and Insights",
                f"Common Mistakes in {topic} and How to Avoid Them",
                f"Best Practices for {topic} Success",
                f"Transform Your Business with {topic}"
            ]
            
            if keywords:
                keyword_list = keywords.split(',')
                for keyword in keyword_list[:3]:
                    keyword = keyword.strip()
                    titles.append(f"{keyword} and {topic}: A Complete Guide")
                    titles.append(f"Why {keyword} Matters in {topic}")
            
            return titles[:10]
            
        except Exception as e:
            logging.error(f"Blog title generation error: {str(e)}")
            return ["How to Succeed in Business", "Digital Marketing Tips", "Technology Trends"]
    
    @staticmethod 
    def generate_product_description(product_name, features="", target_audience=""):
        """Generate product description"""
        try:
            default_features = "• Advanced functionality\n• User-friendly interface\n• Reliable performance"
            feature_text = features or default_features
            audience_text = target_audience or 'modern professionals'
            
            description = f"""Introducing {product_name} - the revolutionary solution designed for {audience_text}.

Key Features:
{feature_text}

This innovative product combines cutting-edge technology with practical design to deliver exceptional results. Whether you're looking to streamline your workflow or enhance productivity, {product_name} provides the tools you need to succeed.

Perfect for businesses and individuals who demand quality and efficiency. Experience the difference that {product_name} can make in your daily operations."""
            
            return description.strip()
            
        except Exception as e:
            logging.error(f"Product description generation error: {str(e)}")
            return f"Professional {product_name} designed for optimal performance and user satisfaction."