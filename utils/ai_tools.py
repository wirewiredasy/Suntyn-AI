import os
import json
import uuid
from werkzeug.utils import secure_filename

class AIProcessor:
    @staticmethod
    def generate_resume(data):
        """Generate a resume using AI (placeholder)"""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        
        # Create resume PDF
        os.makedirs('uploads', exist_ok=True)
        output_filename = f"resume_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join('uploads', output_filename)
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"<b>{data.get('name', 'John Doe')}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Contact Information
        email = data.get('email', 'john@example.com')
        phone = data.get('phone', '+1-555-0123')
        contact = Paragraph(f"Email: {email} | Phone: {phone}", styles['Normal'])
        story.append(contact)
        story.append(Spacer(1, 12))
        
        # Professional Summary
        summary = data.get('summary', 'Experienced professional with expertise in multiple domains.')
        summary_title = Paragraph("<b>Professional Summary</b>", styles['Heading2'])
        summary_text = Paragraph(summary, styles['Normal'])
        story.append(summary_title)
        story.append(summary_text)
        story.append(Spacer(1, 12))
        
        # Experience
        experience_title = Paragraph("<b>Experience</b>", styles['Heading2'])
        story.append(experience_title)
        
        experience = data.get('experience', [])
        if not experience:
            experience = [
                {
                    'title': 'Software Engineer',
                    'company': 'Tech Company',
                    'duration': '2020-Present',
                    'description': 'Developed and maintained web applications using modern technologies.'
                }
            ]
        
        for exp in experience:
            exp_title = Paragraph(f"<b>{exp.get('title', 'Position')}</b> - {exp.get('company', 'Company')}", styles['Heading3'])
            exp_duration = Paragraph(f"<i>{exp.get('duration', '2020-Present')}</i>", styles['Normal'])
            exp_desc = Paragraph(exp.get('description', 'Job description'), styles['Normal'])
            story.append(exp_title)
            story.append(exp_duration)
            story.append(exp_desc)
            story.append(Spacer(1, 6))
        
        # Education
        education_title = Paragraph("<b>Education</b>", styles['Heading2'])
        story.append(education_title)
        
        education = data.get('education', [])
        if not education:
            education = [
                {
                    'degree': 'Bachelor of Computer Science',
                    'school': 'University Name',
                    'year': '2020'
                }
            ]
        
        for edu in education:
            edu_text = Paragraph(f"{edu.get('degree', 'Degree')} - {edu.get('school', 'School')} ({edu.get('year', '2020')})", styles['Normal'])
            story.append(edu_text)
            story.append(Spacer(1, 6))
        
        # Skills
        skills = data.get('skills', ['Python', 'JavaScript', 'React', 'Node.js'])
        skills_title = Paragraph("<b>Skills</b>", styles['Heading2'])
        skills_text = Paragraph(', '.join(skills), styles['Normal'])
        story.append(skills_title)
        story.append(skills_text)
        
        doc.build(story)
        return output_path
    
    @staticmethod
    def generate_business_names(industry, keywords, count=10):
        """Generate business name suggestions"""
        import random
        
        # Common business name patterns
        prefixes = ['Prime', 'Elite', 'Global', 'Digital', 'Smart', 'Pro', 'Next', 'Future', 'Advanced', 'Premium']
        suffixes = ['Solutions', 'Systems', 'Services', 'Group', 'Corp', 'Inc', 'Labs', 'Works', 'Hub', 'Studio']
        
        business_names = []
        
        # Generate names based on keywords
        for keyword in keywords:
            keyword = keyword.strip().title()
            
            # Pattern 1: Keyword + Suffix
            for suffix in random.sample(suffixes, min(3, len(suffixes))):
                business_names.append(f"{keyword} {suffix}")
            
            # Pattern 2: Prefix + Keyword
            for prefix in random.sample(prefixes, min(3, len(prefixes))):
                business_names.append(f"{prefix} {keyword}")
            
            # Pattern 3: Industry-specific combinations
            if industry:
                industry_words = industry.split()
                for word in industry_words:
                    if word.lower() not in ['the', 'and', 'or', 'of', 'in', 'to', 'for']:
                        business_names.append(f"{keyword} {word.title()}")
        
        # Add some creative combinations
        creative_names = [
            f"{random.choice(prefixes)}{random.choice(keywords).title()}",
            f"{random.choice(keywords).title()}{random.choice(['Pro', 'Max', 'Plus', 'X', 'Tech'])}",
            f"{random.choice(keywords).title()}{random.choice(['ify', 'ly', 'wise', 'hub', 'labs'])}"
        ]
        
        business_names.extend(creative_names)
        
        # Remove duplicates and limit to requested count
        unique_names = list(set(business_names))
        return unique_names[:count]
    
    @staticmethod
    def generate_blog_titles(topic, keywords, count=10):
        """Generate blog title suggestions"""
        import random
        
        # Common blog title patterns
        patterns = [
            "How to {action} {topic}",
            "The Ultimate Guide to {topic}",
            "{number} Ways to {action} {topic}",
            "Why {topic} is Important for {audience}",
            "The Complete {topic} Tutorial",
            "{topic}: Everything You Need to Know",
            "Mastering {topic} in {timeframe}",
            "The Future of {topic}",
            "{topic} Best Practices",
            "Common {topic} Mistakes to Avoid"
        ]
        
        actions = ['improve', 'master', 'understand', 'optimize', 'learn', 'implement', 'build', 'create']
        numbers = ['5', '10', '15', '20', '25']
        timeframes = ['2024', '30 days', '1 week', '3 months']
        audiences = ['beginners', 'professionals', 'businesses', 'developers', 'marketers']
        
        titles = []
        
        for pattern in patterns:
            for keyword in keywords:
                title = pattern.format(
                    action=random.choice(actions),
                    topic=keyword.title(),
                    number=random.choice(numbers),
                    timeframe=random.choice(timeframes),
                    audience=random.choice(audiences)
                )
                titles.append(title)
        
        # Add topic-specific titles
        topic_titles = [
            f"Getting Started with {topic}",
            f"{topic} Tips and Tricks",
            f"Advanced {topic} Techniques",
            f"{topic} Case Studies",
            f"The Benefits of {topic}"
        ]
        
        titles.extend(topic_titles)
        
        # Remove duplicates and limit to requested count
        unique_titles = list(set(titles))
        return unique_titles[:count]
    
    @staticmethod
    def generate_product_description(product_name, features, benefits, target_audience):
        """Generate product description"""
        description = f"""
        <h2>{product_name}</h2>
        
        <h3>Product Overview</h3>
        <p>Discover the power of {product_name}, designed specifically for {target_audience}. 
        Our innovative solution combines cutting-edge technology with user-friendly design.</p>
        
        <h3>Key Features</h3>
        <ul>
        """
        
        for feature in features:
            description += f"<li>{feature}</li>\n"
        
        description += """
        </ul>
        
        <h3>Benefits</h3>
        <ul>
        """
        
        for benefit in benefits:
            description += f"<li>{benefit}</li>\n"
        
        description += f"""
        </ul>
        
        <h3>Perfect For</h3>
        <p>{product_name} is ideal for {target_audience} who want to enhance their productivity 
        and achieve better results. Whether you're a beginner or an expert, our solution 
        adapts to your needs.</p>
        
        <h3>Why Choose {product_name}?</h3>
        <p>With its intuitive interface and powerful capabilities, {product_name} stands out 
        from the competition. Join thousands of satisfied customers who have already 
        transformed their workflow with our solution.</p>
        """
        
        return description.strip()
    
    @staticmethod
    def generate_ad_copy(product, target_audience, tone='professional', length='short'):
        """Generate advertisement copy"""
        
        # Tone variations
        tones = {
            'professional': {
                'adjectives': ['innovative', 'professional', 'reliable', 'efficient', 'premium'],
                'verbs': ['enhance', 'optimize', 'streamline', 'elevate', 'transform'],
                'closings': ['Contact us today', 'Learn more', 'Get started now']
            },
            'casual': {
                'adjectives': ['awesome', 'cool', 'amazing', 'fantastic', 'incredible'],
                'verbs': ['boost', 'improve', 'upgrade', 'supercharge', 'revolutionize'],
                'closings': ['Check it out', 'Try it now', 'Get yours today']
            },
            'urgent': {
                'adjectives': ['limited-time', 'exclusive', 'urgent', 'immediate', 'instant'],
                'verbs': ['act now', 'don\'t wait', 'hurry', 'grab', 'secure'],
                'closings': ['Act now!', 'Limited time offer!', 'Don\'t miss out!']
            }
        }
        
        tone_data = tones.get(tone, tones['professional'])
        
        if length == 'short':
            copy = f"""
            🎯 {random.choice(tone_data['adjectives']).title()} {product} for {target_audience}
            
            {random.choice(tone_data['verbs']).title()} your results with our cutting-edge solution.
            
            ✅ Easy to use
            ✅ Fast results
            ✅ Proven effectiveness
            
            {random.choice(tone_data['closings'])}!
            """
        else:
            copy = f"""
            Introducing {product} - The {random.choice(tone_data['adjectives'])} Solution for {target_audience}
            
            Are you tired of struggling with outdated methods? {product} is here to 
            {random.choice(tone_data['verbs'])} your entire approach.
            
            What makes {product} different:
            • Industry-leading technology
            • User-friendly interface
            • Proven track record
            • Exceptional customer support
            
            Perfect for {target_audience} who demand excellence. Join thousands of 
            satisfied customers who have already transformed their workflow.
            
            Special launch offer: Get started today and experience the difference!
            
            {random.choice(tone_data['closings'])}
            """
        
        return copy.strip()
    
    @staticmethod
    def generate_faq(topic, questions_count=10):
        """Generate FAQ for a topic"""
        import random
        
        # Common FAQ patterns
        question_patterns = [
            f"What is {topic}?",
            f"How does {topic} work?",
            f"Is {topic} safe to use?",
            f"How much does {topic} cost?",
            f"Can I use {topic} for free?",
            f"What are the benefits of {topic}?",
            f"How do I get started with {topic}?",
            f"Is {topic} suitable for beginners?",
            f"What support is available for {topic}?",
            f"How long does it take to see results with {topic}?"
        ]
        
        # Generic answers
        answers = [
            f"{topic} is a comprehensive solution designed to help users achieve their goals efficiently.",
            f"{topic} works by utilizing advanced algorithms and user-friendly interfaces to deliver optimal results.",
            f"Yes, {topic} is completely safe and follows industry best practices for security and privacy.",
            f"We offer various pricing plans for {topic} to suit different needs and budgets.",
            f"Yes, we provide a free tier of {topic} with basic features to get you started.",
            f"The main benefits of {topic} include improved efficiency, better results, and user-friendly experience.",
            f"Getting started with {topic} is easy - simply sign up and follow our guided setup process.",
            f"Absolutely! {topic} is designed to be accessible for users of all skill levels.",
            f"We provide comprehensive support including documentation, tutorials, and customer service.",
            f"Most users see immediate results with {topic}, with significant improvements within the first week."
        ]
        
        faq_list = []
        for i, question in enumerate(question_patterns[:questions_count]):
            faq_list.append({
                'question': question,
                'answer': answers[i % len(answers)]
            })
        
        return faq_list