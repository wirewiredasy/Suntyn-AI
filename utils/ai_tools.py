import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import random

def generate_resume(name, email, phone, experience, education, skills, output_path):
    """Generate a professional resume PDF"""
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Header
        story.append(Paragraph(f"<b>{name}</b>", styles['Title']))
        story.append(Paragraph(f"{email} | {phone}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Experience
        if experience:
            story.append(Paragraph("<b>Experience</b>", styles['Heading2']))
            for exp in experience:
                story.append(Paragraph(f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}", styles['Normal']))
                story.append(Paragraph(f"{exp.get('duration', '')}", styles['Normal']))
                story.append(Paragraph(exp.get('description', ''), styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Education
        if education:
            story.append(Paragraph("<b>Education</b>", styles['Heading2']))
            for edu in education:
                story.append(Paragraph(f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}", styles['Normal']))
                story.append(Paragraph(f"{edu.get('year', '')}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Skills
        if skills:
            story.append(Paragraph("<b>Skills</b>", styles['Heading2']))
            story.append(Paragraph(", ".join(skills), styles['Normal']))
        
        doc.build(story)
        return True
    except Exception as e:
        print(f"Error generating resume: {e}")
        return False

def generate_business_names(industry, keywords, count=10):
    """Generate business name suggestions"""
    try:
        # Simple business name generator
        prefixes = ['Pro', 'Elite', 'Smart', 'Quick', 'Prime', 'Digital', 'Modern', 'Creative', 'Global', 'Innovative']
        suffixes = ['Solutions', 'Services', 'Systems', 'Technologies', 'Consulting', 'Group', 'Labs', 'Studio', 'Works', 'Hub']
        
        names = []
        
        # Generate names using keywords
        for keyword in keywords:
            for prefix in prefixes[:3]:
                names.append(f"{prefix} {keyword}")
            for suffix in suffixes[:3]:
                names.append(f"{keyword} {suffix}")
        
        # Add some random combinations
        for i in range(count - len(names)):
            if len(names) >= count:
                break
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            names.append(f"{prefix} {suffix}")
        
        return names[:count]
    except Exception as e:
        print(f"Error generating business names: {e}")
        return []

def generate_blog_titles(topic, count=10):
    """Generate blog title suggestions"""
    try:
        title_templates = [
            "The Ultimate Guide to {topic}",
            "10 Essential Tips for {topic}",
            "How to Master {topic} in 2024",
            "The Complete {topic} Handbook",
            "5 Common {topic} Mistakes to Avoid",
            "Why {topic} is Important for Your Business",
            "The Future of {topic}",
            "Best Practices for {topic}",
            "Advanced {topic} Strategies",
            "Getting Started with {topic}"
        ]
        
        titles = []
        for template in title_templates:
            titles.append(template.format(topic=topic))
        
        return titles[:count]
    except Exception as e:
        print(f"Error generating blog titles: {e}")
        return []

def generate_product_description(product_name, features, benefits, target_audience="general"):
    """Generate product description"""
    try:
        # Simple product description generator
        intro_templates = [
            f"Introducing {product_name}, the revolutionary solution that transforms your experience.",
            f"Discover the power of {product_name} and unlock new possibilities.",
            f"Meet {product_name}, designed specifically for {target_audience}."
        ]
        
        description = random.choice(intro_templates) + "\n\n"
        
        if features:
            description += "Key Features:\n"
            for feature in features:
                description += f"• {feature}\n"
            description += "\n"
        
        if benefits:
            description += "Benefits:\n"
            for benefit in benefits:
                description += f"• {benefit}\n"
            description += "\n"
        
        description += f"Experience the difference with {product_name} today!"
        
        return description
    except Exception as e:
        print(f"Error generating product description: {e}")
        return ""

def generate_social_bio(name, profession, interests, platform="general"):
    """Generate social media bio"""
    try:
        bio_templates = {
            "general": [
                f"{profession} | {' & '.join(interests[:2])} enthusiast",
                f"✨ {profession} ✨ Passionate about {interests[0] if interests else 'innovation'}",
                f"{profession} sharing insights about {' & '.join(interests[:2])}"
            ],
            "instagram": [
                f"📸 {profession}\n✨ {' • '.join(interests[:3])}\n🌟 Living my best life",
                f"🎯 {profession}\n💡 {interests[0] if interests else 'Creating'} enthusiast\n📩 DM for collabs"
            ],
            "twitter": [
                f"{profession} | Tweeting about {' & '.join(interests[:2])}",
                f"💡 {profession} • {interests[0] if interests else 'Innovation'} advocate • Coffee lover ☕"
            ],
            "linkedin": [
                f"{profession} with expertise in {' and '.join(interests[:2])}",
                f"Experienced {profession} | {interests[0] if interests else 'Industry'} thought leader"
            ]
        }
        
        templates = bio_templates.get(platform, bio_templates["general"])
        return random.choice(templates)
    except Exception as e:
        print(f"Error generating social bio: {e}")
        return ""

def generate_ad_copy(product, target_audience, call_to_action="Learn More"):
    """Generate ad copy"""
    try:
        headlines = [
            f"Transform Your {target_audience} Experience with {product}",
            f"The {product} That {target_audience} Are Raving About",
            f"Why {target_audience} Choose {product} Over Everything Else"
        ]
        
        descriptions = [
            f"Join thousands of satisfied {target_audience} who have discovered the power of {product}. Don't miss out on this game-changing solution.",
            f"Experience the difference that {product} makes. Perfect for {target_audience} who demand excellence.",
            f"Ready to elevate your game? {product} is here to help {target_audience} achieve their goals faster and more efficiently."
        ]
        
        return {
            "headline": random.choice(headlines),
            "description": random.choice(descriptions),
            "call_to_action": call_to_action
        }
    except Exception as e:
        print(f"Error generating ad copy: {e}")
        return {"headline": "", "description": "", "call_to_action": call_to_action}
