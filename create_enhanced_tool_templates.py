#!/usr/bin/env python3
"""
Enhanced Tool Template Generator for Toolora AI
Creates unique, professional, mobile-responsive templates for all 85 tools
"""

import os
from config import Config

def get_tool_details(tool_name, category_id):
    """Get detailed information for each tool"""
    
    # Tool-specific configurations with unique features and descriptions
    tool_configs = {
        # PDF Tools
        'pdf-merge': {
            'title': 'PDF Merge',
            'description': 'Combine multiple PDF files into one seamless document',
            'features': ['Drag & drop file upload', 'Reorder files via drag', 'Progress tracking', 'Batch processing'],
            'instructions': 'Upload multiple PDF files and arrange them in your desired order. Click merge to create a single PDF.',
            'file_types': ['.pdf'],
            'handler': 'pdfMerger()'
        },
        'pdf-split': {
            'title': 'PDF Split',
            'description': 'Extract specific pages or ranges from a PDF',
            'features': ['Page range selector', 'Real-time preview', 'Multiple output options', 'Batch processing'],
            'instructions': 'Upload a PDF and specify which pages to extract (e.g., 1-3, 5, 7-10).',
            'file_types': ['.pdf'],
            'handler': 'genericToolHandler("pdf-split")'
        },
        'pdf-compress': {
            'title': 'PDF Compress',
            'description': 'Reduce PDF file size without losing quality',
            'features': ['Compression level control', 'Quality preview', 'Size comparison', 'Privacy-safe'],
            'instructions': 'Upload a PDF file and choose compression level. Preview the result before downloading.',
            'file_types': ['.pdf'],
            'handler': 'genericToolHandler("pdf-compress")'
        },
        
        # Image Tools
        'image-compress': {
            'title': 'Image Compress',
            'description': 'Reduce image file size while preserving quality',
            'features': ['Quality slider', 'Before/after preview', 'Multiple formats', 'Batch processing'],
            'instructions': 'Upload images and adjust quality settings. Preview the compression results.',
            'file_types': ['.jpg', '.jpeg', '.png', '.webp'],
            'handler': 'imageCompressor()'
        },
        'image-resize': {
            'title': 'Image Resize',
            'description': 'Resize images by dimensions or percentage',
            'features': ['Aspect ratio lock', 'Percentage scaling', 'Multiple units', 'Batch processing'],
            'instructions': 'Upload images and set new dimensions. Choose to maintain aspect ratio or custom sizing.',
            'file_types': ['.jpg', '.jpeg', '.png', '.webp'],
            'handler': 'genericToolHandler("image-resize")'
        },
        'background-remover': {
            'title': 'Background Remover',
            'description': 'Remove image backgrounds with AI precision',
            'features': ['AI detection', 'Transparent PNG output', 'Edge refinement', 'Batch processing'],
            'instructions': 'Upload an image and let AI automatically remove the background. Download as PNG.',
            'file_types': ['.jpg', '.jpeg', '.png'],
            'handler': 'genericToolHandler("background-remover")'
        },
        
        # Video Tools
        'video-trimmer': {
            'title': 'Video Trimmer',
            'description': 'Cut specific sections from video files',
            'features': ['Timeline preview', 'Precision cutting', 'Multiple formats', 'Quality preservation'],
            'instructions': 'Upload a video and set start/end times. Preview the trimmed section before processing.',
            'file_types': ['.mp4', '.mov', '.avi', '.mkv'],
            'handler': 'videoTrimmer()'
        },
        'video-to-mp3': {
            'title': 'Video to MP3',
            'description': 'Extract audio from video files',
            'features': ['High-quality audio', 'Multiple formats', 'Batch processing', 'Quality options'],
            'instructions': 'Upload video files to extract audio tracks. Choose quality and format.',
            'file_types': ['.mp4', '.mov', '.avi', '.mkv'],
            'handler': 'genericToolHandler("video-to-mp3")'
        },
        
        # AI Tools
        'resume-generator': {
            'title': 'Resume Generator',
            'description': 'Create professional resumes with AI assistance',
            'features': ['Multiple templates', 'AI suggestions', 'PDF export', 'Real-time preview'],
            'instructions': 'Fill in your details step by step. AI will help format and suggest improvements.',
            'file_types': [],
            'handler': 'resumeGenerator()'
        },
        'business-name-generator': {
            'title': 'Business Name Generator',
            'description': 'Generate creative business names with AI',
            'features': ['Industry-specific', 'Domain availability', 'Multiple suggestions', 'Trademark check'],
            'instructions': 'Enter keywords and industry. AI will generate unique business name suggestions.',
            'file_types': [],
            'handler': 'genericToolHandler("business-name-generator")'
        },
        
        # Utility Tools
        'qr-generator': {
            'title': 'QR Code Generator',
            'description': 'Create customizable QR codes for any content',
            'features': ['Custom colors', 'Multiple sizes', 'Logo embedding', 'Batch generation'],
            'instructions': 'Enter text, URL, or other content. Customize appearance and download QR code.',
            'file_types': [],
            'handler': 'qrGenerator()'
        },
        'password-generator': {
            'title': 'Password Generator',
            'description': 'Generate secure, random passwords',
            'features': ['Length control', 'Character options', 'Strength indicator', 'Bulk generation'],
            'instructions': 'Set password length and character types. Generate secure passwords instantly.',
            'file_types': [],
            'handler': 'genericToolHandler("password-generator")'
        }
    }
    
    # Get tool config or create generic one
    config = tool_configs.get(tool_name, {
        'title': tool_name.replace('-', ' ').title(),
        'description': f'Professional {tool_name.replace("-", " ")} tool',
        'features': ['Easy to use', 'Fast processing', 'Secure', 'No registration required'],
        'instructions': 'Upload your files and process them with our professional tool.',
        'file_types': ['.*'],
        'handler': f'genericToolHandler("{tool_name}")'
    })
    
    return config

def create_enhanced_template(tool_name, category_id, category_data):
    """Create enhanced template with unique design and functionality"""
    
    config = get_tool_details(tool_name, category_id)
    color = category_data['color']
    
    # Generate feature list HTML
    features_html = ""
    for feature in config['features']:
        features_html += f'''
            <div class="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                <div class="w-2 h-2 bg-{color}-500 rounded-full"></div>
                <span class="text-gray-700 dark:text-gray-300">{feature}</span>
            </div>'''
    
    # Generate file types HTML
    file_types_html = ""
    if config['file_types']:
        file_types_html = f"Supported formats: {', '.join(config['file_types'])}"
    
    template_content = f'''{% extends "base.html" %}

{% block title %}{config['title']} - Toolora AI{% endblock %}

{% block head %}
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/tool-specific-styles.css') }}}}">
<script src="{{{{ url_for('static', filename='js/tool-specific-handlers.js') }}}}"></script>
{{%% endblock %%}}

{{%% block content %%}}
<div class="min-h-screen {category_id}-gradient dark:from-gray-900 dark:to-gray-800 pt-20">
    <div class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- Enhanced Breadcrumb -->
            <nav class="flex mb-8 animate-fade-in" aria-label="Breadcrumb">
                <ol class="inline-flex items-center space-x-1 md:space-x-3">
                    <li class="inline-flex items-center">
                        <a href="{{{{ url_for('main.index') }}}}" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-{color}-600 dark:text-gray-400 dark:hover:text-white transition-colors">
                            <i data-lucide="home" class="w-4 h-4 mr-2"></i>
                            Home
                        </a>
                    </li>
                    <li>
                        <div class="flex items-center">
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                            <a href="{{{{ url_for('tools.index') }}}}" class="ml-1 text-sm font-medium text-gray-700 hover:text-{color}-600 md:ml-2 dark:text-gray-400 dark:hover:text-white transition-colors">Tools</a>
                        </div>
                    </li>
                    <li>
                        <div class="flex items-center">
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                            <a href="{{{{ url_for('tools.index', category='{category_id}') }}}}" class="ml-1 text-sm font-medium text-gray-700 hover:text-{color}-600 md:ml-2 dark:text-gray-400 dark:hover:text-white transition-colors">
                                {category_data['name']}
                            </a>
                        </div>
                    </li>
                    <li aria-current="page">
                        <div class="flex items-center">
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                            <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2 dark:text-gray-400">{config['title']}</span>
                        </div>
                    </li>
                </ol>
            </nav>

            <!-- Enhanced Tool Header -->
            <div class="text-center mb-12 animate-fade-in">
                <div class="w-24 h-24 mx-auto mb-6 rounded-3xl bg-{color}-100 dark:bg-{color}-900 flex items-center justify-center shadow-lg">
                    <i data-lucide="{category_data['icon']}" class="w-12 h-12 text-{color}-600 dark:text-{color}-400"></i>
                </div>
                <h1 class="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">{config['title']}</h1>
                <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">{config['description']}</p>
                <div class="mt-6 flex flex-wrap justify-center gap-2">
                    <span class="px-4 py-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm font-medium">Free</span>
                    <span class="px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">No Registration</span>
                    <span class="px-4 py-2 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full text-sm font-medium">Secure</span>
                    <span class="px-4 py-2 bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200 rounded-full text-sm font-medium">Fast Processing</span>
                </div>
            </div>

            <!-- Enhanced Tool Interface -->
            <div class="{category_id}-card rounded-3xl shadow-2xl p-8 mb-8 animate-slide-in">
                <div x-data="{config['handler']}" class="space-y-8">
                    <!-- Instructions -->
                    <div class="bg-{color}-50 dark:bg-{color}-900/20 border border-{color}-200 dark:border-{color}-700 rounded-2xl p-6">
                        <div class="flex items-start space-x-3">
                            <i data-lucide="info" class="w-6 h-6 text-{color}-600 dark:text-{color}-400 mt-1 flex-shrink-0"></i>
                            <div>
                                <h3 class="text-lg font-semibold text-{color}-900 dark:text-{color}-100 mb-2">How to Use</h3>
                                <p class="text-{color}-800 dark:text-{color}-200">{config['instructions']}</p>
                                {f'<p class="text-sm text-{color}-600 dark:text-{color}-400 mt-2">{file_types_html}</p>' if file_types_html else ''}
                            </div>
                        </div>
                    </div>

                    <!-- Enhanced Upload Area -->
                    <div class="{category_id}-upload-zone border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300"
                         @dragover.prevent="dragover = true"
                         @dragleave.prevent="dragover = false"
                         @drop.prevent="handleDrop && handleDrop($event)"
                         :class="{{ 'border-{color}-400 bg-{color}-50 dark:bg-{color}-900/20': dragover }}">
                        
                        <div class="space-y-6">
                            <div class="w-20 h-20 mx-auto rounded-full bg-{color}-100 dark:bg-{color}-700 flex items-center justify-center">
                                <i data-lucide="upload" class="w-10 h-10 text-{color}-600 dark:text-{color}-400"></i>
                            </div>
                            
                            <div>
                                <h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-3">Upload Files</h3>
                                <p class="text-gray-600 dark:text-gray-300 mb-6">
                                    Drag and drop your files here, or click to browse
                                </p>
                                
                                <input type="file" id="file-input" multiple class="hidden" 
                                       @change="handleFiles && handleFiles($event.target.files)"
                                       accept="{','.join(config['file_types']) if config['file_types'] else '*'}">
                                <button @click="$refs.fileInput.click()" class="btn-{category_id} inline-flex items-center px-8 py-4 text-lg font-medium rounded-xl transition-all duration-300 transform hover:scale-105">
                                    <i data-lucide="folder" class="w-5 h-5 mr-3"></i>
                                    Choose Files
                                </button>
                                <input type="file" x-ref="fileInput" multiple class="hidden" 
                                       @change="handleFiles && handleFiles($event.target.files)"
                                       accept="{','.join(config['file_types']) if config['file_types'] else '*'}">
                            </div>
                            
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                Maximum file size: 16MB per file
                            </p>
                        </div>
                    </div>

                    <!-- File List -->
                    <div x-show="files && files.length > 0" class="space-y-4">
                        <h4 class="text-lg font-semibold text-gray-900 dark:text-white">Selected Files</h4>
                        <div class="space-y-2">
                            <template x-for="(file, index) in files" :key="index">
                                <div class="file-preview">
                                    <div class="file-preview-icon">
                                        <i data-lucide="file" class="w-5 h-5 text-{color}-600"></i>
                                    </div>
                                    <div class="file-preview-info">
                                        <div class="file-preview-name" x-text="file.name || (file.file && file.file.name)"></div>
                                        <div class="file-preview-size" x-text="formatFileSize && formatFileSize(file.size || (file.file && file.file.size))"></div>
                                    </div>
                                    <button @click="removeFile && removeFile(index)" class="file-preview-remove">
                                        <i data-lucide="x" class="w-4 h-4"></i>
                                    </button>
                                </div>
                            </template>
                        </div>
                    </div>

                    <!-- Processing Button -->
                    <div class="text-center">
                        <button @click="processFiles && processFiles()" 
                                :disabled="processing || (files && files.length === 0)"
                                class="btn-{category_id} px-12 py-4 text-lg font-semibold rounded-xl transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                            <span x-show="!processing" class="flex items-center">
                                <i data-lucide="play" class="w-5 h-5 mr-3"></i>
                                Process Files
                            </span>
                            <span x-show="processing" class="flex items-center">
                                <i data-lucide="loader" class="w-5 h-5 mr-3 animate-spin"></i>
                                Processing...
                            </span>
                        </button>
                    </div>

                    <!-- Progress Bar -->
                    <div x-show="processing" class="space-y-4">
                        <div class="progress-bar {category_id}" :style="`--progress-width: ${{progress}}%`"></div>
                        <p class="text-center text-sm text-gray-600 dark:text-gray-400" x-text="`Processing: ${{progress}}%`"></p>
                    </div>
                </div>
            </div>

            <!-- Enhanced Features Section -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="space-y-4">
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Key Features</h3>
                    <div class="space-y-3">
                        {features_html}
                    </div>
                </div>
                <div class="space-y-4">
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Why Choose Our Tool?</h3>
                    <div class="space-y-3">
                        <div class="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span class="text-gray-700 dark:text-gray-300">100% Privacy & Security</span>
                        </div>
                        <div class="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                            <span class="text-gray-700 dark:text-gray-300">No Registration Required</span>
                        </div>
                        <div class="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                            <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                            <span class="text-gray-700 dark:text-gray-300">Lightning Fast Processing</span>
                        </div>
                        <div class="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                            <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                            <span class="text-gray-700 dark:text-gray-300">Mobile Responsive</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Tool-specific scripts -->
<script>
    // Initialize Lucide icons
    lucide.createIcons();
    
    // Initialize tool-specific enhancements
    document.addEventListener('DOMContentLoaded', function() {{
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // Add enhanced animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('animate-fade-in');
                }}
            }});
        }});
        
        document.querySelectorAll('.animate-on-scroll').forEach(el => {{
            observer.observe(el);
        }});
    }});
</script>
{{%% endblock %%}}'''

    return template_content

def generate_all_enhanced_templates():
    """Generate enhanced templates for all 85 tools"""
    
    # Create templates/tools directory if it doesn't exist
    os.makedirs('templates/tools', exist_ok=True)
    
    total_created = 0
    total_updated = 0
    
    print("🚀 Generating Enhanced Tool Templates")
    print("=" * 50)
    
    for category_id, category_data in Config.TOOL_CATEGORIES.items():
        print(f"\n📁 {category_data['name']} ({len(category_data['tools'])} tools)")
        
        for tool_name in category_data['tools']:
            template_path = f"templates/tools/{tool_name}.html"
            
            # Create enhanced template
            template_content = create_enhanced_template(tool_name, category_id, category_data)
            
            # Check if template exists
            if os.path.exists(template_path):
                # Update existing template
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                print(f"  ✅ Updated {tool_name}.html")
                total_updated += 1
            else:
                # Create new template
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                print(f"  ✨ Created {tool_name}.html")
                total_created += 1
    
    print(f"\n🎉 Template Generation Complete!")
    print(f"📊 Created: {total_created} templates")
    print(f"📊 Updated: {total_updated} templates")
    print(f"📊 Total: {total_created + total_updated} templates")
    
    return total_created + total_updated

if __name__ == "__main__":
    generate_all_enhanced_templates()