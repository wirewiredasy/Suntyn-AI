import os
import json
import random
import string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime

def generate_resume(form_data, output_path):
    """Generate PDF resume from form data"""
    try:
        # Create PDF canvas
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, form_data.get('name', 'Unknown'))
        
        # Contact info
        c.setFont("Helvetica", 12)
        y_position = height - 80
        
        contact_info = [
            form_data.get('email', ''),
            form_data.get('phone', ''),
            form_data.get('address', '')
        ]
        
        for info in contact_info:
            if info:
                c.drawString(50, y_position, info)
                y_position -= 20
        
        # Objective
        if form_data.get('objective'):
            y_position -= 20
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, "Objective")
            y_position -= 20
            c.setFont("Helvetica", 12)
            c.drawString(50, y_position, form_data['objective'])
            y_position -= 30
        
        # Experience
        if form_data.get('experience'):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, "Experience")
            y_position -= 20
            
            for exp in form_data['experience']:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y_position, f"{exp.get('position', '')} - {exp.get('company', '')}")
                y_position -= 15
                c.setFont("Helvetica", 10)
                c.drawString(50, y_position, exp.get('duration', ''))
                y_position -= 15
                c.setFont("Helvetica", 12)
                c.drawString(50, y_position, exp.get('description', ''))
                y_position -= 25
        
        # Education
        if form_data.get('education'):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, "Education")
            y_position -= 20
            
            for edu in form_data['education']:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y_position, f"{edu.get('degree', '')} - {edu.get('institution', '')}")
                y_position -= 15
                c.setFont("Helvetica", 10)
                c.drawString(50, y_position, f"{edu.get('year', '')} - {edu.get('grade', '')}")
                y_position -= 25
        
        # Skills
        if form_data.get('skills'):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, "Skills")
            y_position -= 20
            c.setFont("Helvetica", 12)
            skills_text = ', '.join(form_data['skills'])
            c.drawString(50, y_position, skills_text)
        
        c.save()
        return True
    except Exception as e:
        print(f"Error generating resume: {e}")
        return False

def generate_business_names(keywords, industry, count=10):
    """Generate business names based on keywords and industry"""
    try:
        # Simple name generation algorithm
        # In production, you'd use AI services like OpenAI
        
        prefixes = ['Pro', 'Smart', 'Digital', 'Tech', 'Expert', 'Prime', 'Elite', 'Ultra']
        suffixes = ['Solutions', 'Services', 'Pro', 'Hub', 'Lab', 'Studio', 'Works', 'Co']
        
        # Industry-specific terms
        industry_terms = {
            'technology': ['Tech', 'Digital', 'Cyber', 'Data', 'Cloud', 'AI'],
            'healthcare': ['Health', 'Care', 'Medical', 'Wellness', 'Life'],
            'finance': ['Finance', 'Capital', 'Money', 'Wealth', 'Investment'],
            'education': ['Learn', 'Edu', 'Academic', 'Study', 'Knowledge'],
            'general': ['Pro', 'Smart', 'Expert', 'Prime', 'Elite']
        }
        
        terms = industry_terms.get(industry, industry_terms['general'])
        keyword_list = [k.strip().capitalize() for k in keywords.split(',')]
        
        names = []
        for _ in range(count):
            # Generate different types of names
            name_type = random.choice(['prefix_keyword', 'keyword_suffix', 'industry_keyword', 'compound'])
            
            if name_type == 'prefix_keyword':
                name = f"{random.choice(prefixes)} {random.choice(keyword_list)}"
            elif name_type == 'keyword_suffix':
                name = f"{random.choice(keyword_list)} {random.choice(suffixes)}"
            elif name_type == 'industry_keyword':
                name = f"{random.choice(terms)} {random.choice(keyword_list)}"
            else:  # compound
                name = f"{random.choice(keyword_list)} {random.choice(terms)} {random.choice(suffixes)}"
            
            if name not in names:
                names.append(name)
        
        return names[:count]
    except Exception as e:
        print(f"Error generating business names: {e}")
        return []

def generate_blog_titles(keywords, tone='professional', count=5):
    """Generate blog titles based on keywords"""
    try:
        # Simple title generation
        # In production, you'd use AI services
        
        templates = {
            'professional': [
                "Complete Guide to {keyword}",
                "Best Practices for {keyword}",
                "How to Master {keyword} in 2024",
                "Top 10 {keyword} Tips",
                "Understanding {keyword}: A Comprehensive Overview"
            ],
            'casual': [
                "Everything You Need to Know About {keyword}",
                "Why {keyword} Matters More Than You Think",
                "The Ultimate {keyword} Hack",
                "Simple {keyword} Tips That Actually Work",
                "What I Learned About {keyword}"
            ]
        }
        
        template_list = templates.get(tone, templates['professional'])
        keyword_list = [k.strip() for k in keywords.split(',')]
        
        titles = []
        for _ in range(count):
            template = random.choice(template_list)
            keyword = random.choice(keyword_list)
            title = template.format(keyword=keyword)
            if title not in titles:
                titles.append(title)
        
        return titles[:count]
    except Exception as e:
        print(f"Error generating blog titles: {e}")
        return []