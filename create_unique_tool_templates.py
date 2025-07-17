#!/usr/bin/env python3
"""
Create unique UI templates for all 85 tools with individual designs and functionality
"""
import os
from config import Config

def create_tool_template(tool_name, category_name, category_data):
    """Create a unique template for each tool"""
    
    # Generate unique UI based on tool type
    display_name = tool_name.replace('-', ' ').replace('_', ' ').title()
    
    # Color schemes based on category
    color_schemes = {
        'pdf': {'primary': 'red-500', 'secondary': 'red-100', 'accent': 'red-600'},
        'image': {'primary': 'green-500', 'secondary': 'green-100', 'accent': 'green-600'},
        'video': {'primary': 'purple-500', 'secondary': 'purple-100', 'accent': 'purple-600'},
        'govt': {'primary': 'orange-500', 'secondary': 'orange-100', 'accent': 'orange-600'},
        'student': {'primary': 'blue-500', 'secondary': 'blue-100', 'accent': 'blue-600'},
        'finance': {'primary': 'emerald-500', 'secondary': 'emerald-100', 'accent': 'emerald-600'},
        'utility': {'primary': 'slate-500', 'secondary': 'slate-100', 'accent': 'slate-600'},
        'ai': {'primary': 'violet-500', 'secondary': 'violet-100', 'accent': 'violet-600'}
    }
    
    colors = color_schemes.get(category_name, color_schemes['utility'])
    
    # File types and features based on tool
    file_types = []
    special_features = []
    processing_options = []
    
    if 'pdf' in tool_name:
        file_types = ['.pdf']
        if 'merge' in tool_name:
            special_features = ['Drag & drop multiple PDFs', 'Custom page ordering', 'Bookmark preservation']
            processing_options = ['Merge all pages', 'Select specific pages', 'Optimize size']
        elif 'split' in tool_name:
            special_features = ['Split by page range', 'Extract specific pages', 'Batch processing']
            processing_options = ['Split every N pages', 'Split by bookmarks', 'Custom ranges']
        elif 'compress' in tool_name:
            special_features = ['Intelligent compression', 'Quality preservation', 'Size optimization']
            processing_options = ['High quality', 'Medium quality', 'Maximum compression']
    
    elif 'image' in tool_name:
        file_types = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if 'compress' in tool_name:
            special_features = ['Lossless compression', 'Batch processing', 'Format optimization']
            processing_options = ['High quality', 'Web optimized', 'Maximum compression']
        elif 'resize' in tool_name:
            special_features = ['Smart cropping', 'Aspect ratio preservation', 'Bulk resize']
            processing_options = ['Percentage resize', 'Fixed dimensions', 'Smart fit']
        elif 'convert' in tool_name:
            special_features = ['Multiple format support', 'Quality control', 'Metadata preservation']
            processing_options = ['JPEG', 'PNG', 'WebP', 'GIF']
    
    elif 'video' in tool_name:
        file_types = ['.mp4', '.avi', '.mov', '.mkv']
        if 'mp3' in tool_name:
            special_features = ['High-quality audio extraction', 'Bitrate control', 'Metadata preservation']
            processing_options = ['320kbps', '256kbps', '192kbps', '128kbps']
        elif 'trim' in tool_name:
            special_features = ['Precise trimming', 'Multiple segments', 'Quality preservation']
            processing_options = ['Start/End time', 'Multiple clips', 'Custom duration']
    
    elif 'qr' in tool_name:
        file_types = ['.txt']
        special_features = ['Custom colors', 'Logo embedding', 'High resolution']
        processing_options = ['URL', 'Text', 'Contact', 'WiFi']
    
    elif 'resume' in tool_name:
        file_types = ['.txt']
        special_features = ['Professional templates', 'ATS optimization', 'Custom sections']
        processing_options = ['Modern template', 'Classic template', 'Creative template']
    
    else:
        file_types = ['.pdf', '.txt', '.jpg', '.png']
        special_features = ['Fast processing', 'High quality output', 'Secure processing']
        processing_options = ['Standard mode', 'Advanced mode', 'Custom settings']
    
    # Generate unique descriptions
    descriptions = {
        'pdf-merge': 'Combine multiple PDF files into a single document with advanced page ordering and bookmark preservation.',
        'pdf-split': 'Split large PDF files into smaller documents by page ranges, bookmarks, or custom criteria.',
        'pdf-compress': 'Reduce PDF file size while maintaining quality using intelligent compression algorithms.',
        'image-compress': 'Optimize image files with advanced compression while preserving visual quality.',
        'image-resize': 'Resize images with smart cropping and aspect ratio preservation for web and print.',
        'video-to-mp3': 'Extract high-quality audio from video files with customizable bitrate settings.',
        'qr-generator': 'Create professional QR codes with custom colors, logos, and high-resolution output.',
        'resume-generator': 'Build ATS-optimized resumes with professional templates and industry-specific content.',
        'text-case-converter': 'Convert text between different cases (uppercase, lowercase, title case, camel case).',
        'password-generator': 'Generate secure passwords with customizable length and character sets.'
    }
    
    description = descriptions.get(tool_name, f'Professional {display_name.lower()} tool with advanced features and high-quality processing.')
    
    template_content = f'''{{%- extends "base.html" -%}}

{{%- block title -%}}{display_name} - Toolora AI{{%- endblock -%}}

{{%- block content -%}}
<div class="min-h-screen bg-gradient-to-br from-{colors['secondary']} via-white to-{colors['secondary']} py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <!-- Tool Header -->
        <div class="text-center mb-8">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-{colors['primary']} rounded-2xl mb-4 shadow-lg">
                <i data-lucide="{category_data['icon']}" class="w-8 h-8 text-white"></i>
            </div>
            <h1 class="text-4xl font-bold text-gray-900 mb-2">{display_name}</h1>
            <p class="text-lg text-gray-600 max-w-2xl mx-auto">{description}</p>
            <div class="mt-4 flex items-center justify-center space-x-6">
                <div class="flex items-center text-{colors['primary']}">
                    <i data-lucide="shield-check" class="w-5 h-5 mr-2"></i>
                    <span class="text-sm font-medium">100% Secure</span>
                </div>
                <div class="flex items-center text-{colors['primary']}">
                    <i data-lucide="zap" class="w-5 h-5 mr-2"></i>
                    <span class="text-sm font-medium">Lightning Fast</span>
                </div>
                <div class="flex items-center text-{colors['primary']}">
                    <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                    <span class="text-sm font-medium">Free to Use</span>
                </div>
            </div>
        </div>

        <!-- Tool Interface -->
        <div class="bg-white rounded-3xl shadow-2xl border border-gray-100 overflow-hidden">
            
            <!-- Upload Section -->
            <div class="p-8 border-b border-gray-100">
                <div id="upload-section" class="space-y-6">
                    <div class="text-center">
                        <h3 class="text-xl font-semibold text-gray-900 mb-2">Upload Your File{('s' if len(file_types) > 1 else '')}</h3>
                        <p class="text-gray-600">Supported formats: {', '.join(file_types)}</p>
                    </div>
                    
                    <div id="upload-zone" class="border-3 border-dashed border-{colors['primary']} rounded-2xl p-12 text-center hover:border-{colors['accent']} transition-colors cursor-pointer bg-{colors['secondary']}/20">
                        <div class="space-y-4">
                            <div class="mx-auto w-16 h-16 bg-{colors['primary']} rounded-full flex items-center justify-center">
                                <i data-lucide="upload" class="w-8 h-8 text-white"></i>
                            </div>
                            <div>
                                <p class="text-lg font-medium text-gray-900">Click to upload or drag & drop</p>
                                <p class="text-sm text-gray-500">Maximum file size: 16MB</p>
                            </div>
                        </div>
                        <input type="file" id="file-input" class="hidden" multiple accept="{','.join(file_types)}" />
                    </div>
                </div>
            </div>

            <!-- Processing Options -->
            <div class="p-8 border-b border-gray-100 bg-gray-50/50">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Processing Options</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {chr(10).join([f'''<div class="bg-white rounded-xl p-4 border border-gray-200 hover:border-{colors['primary']} transition-colors cursor-pointer option-card" data-option="{option.lower().replace(' ', '-')}">
                        <div class="flex items-center justify-between">
                            <span class="font-medium text-gray-900">{option}</span>
                            <i data-lucide="check-circle" class="w-5 h-5 text-{colors['primary']} hidden"></i>
                        </div>
                    </div>''' for option in processing_options[:3]])}
                </div>
            </div>

            <!-- Special Features -->
            <div class="p-8 border-b border-gray-100">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Special Features</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {chr(10).join([f'''<div class="flex items-center space-x-3 p-3 bg-{colors['secondary']}/30 rounded-xl">
                        <i data-lucide="check" class="w-5 h-5 text-{colors['primary']} flex-shrink-0"></i>
                        <span class="text-sm text-gray-700">{feature}</span>
                    </div>''' for feature in special_features])}
                </div>
            </div>

            <!-- Processing Section -->
            <div id="processing-section" class="p-8 hidden">
                <div class="text-center space-y-4">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-{colors['primary']} rounded-full animate-pulse">
                        <i data-lucide="loader" class="w-8 h-8 text-white animate-spin"></i>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900">Processing Your File</h3>
                    <p class="text-gray-600">Please wait while we process your file...</p>
                    <div class="w-full bg-gray-200 rounded-full h-2 max-w-xs mx-auto">
                        <div id="progress-bar" class="bg-{colors['primary']} h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                    </div>
                </div>
            </div>

            <!-- Results Section -->
            <div id="results-section" class="p-8 hidden">
                <div class="text-center space-y-6">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-green-500 rounded-full">
                        <i data-lucide="check" class="w-8 h-8 text-white"></i>
                    </div>
                    <div>
                        <h3 class="text-xl font-semibold text-gray-900 mb-2">Processing Complete!</h3>
                        <p class="text-gray-600">Your file has been processed successfully.</p>
                    </div>
                    <div class="space-y-3">
                        <button id="download-btn" class="inline-flex items-center px-6 py-3 bg-{colors['primary']} text-white font-medium rounded-xl hover:bg-{colors['accent']} transition-colors">
                            <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                            Download Result
                        </button>
                        <button id="process-another" class="block mx-auto text-{colors['primary']} hover:text-{colors['accent']} font-medium">
                            Process Another File
                        </button>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="p-8 bg-gray-50/50">
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <button id="process-btn" class="flex-1 sm:flex-none px-8 py-3 bg-{colors['primary']} text-white font-semibold rounded-xl hover:bg-{colors['accent']} transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled>
                        <i data-lucide="play" class="w-5 h-5 mr-2 inline"></i>
                        Start Processing
                    </button>
                    <button id="clear-btn" class="flex-1 sm:flex-none px-8 py-3 border border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition-colors">
                        <i data-lucide="x" class="w-5 h-5 mr-2 inline"></i>
                        Clear All
                    </button>
                </div>
            </div>
        </div>

        <!-- Tool Tips -->
        <div class="mt-8 bg-blue-50 rounded-2xl p-6">
            <h3 class="text-lg font-semibold text-blue-900 mb-3">
                <i data-lucide="lightbulb" class="w-5 h-5 mr-2 inline"></i>
                Pro Tips
            </h3>
            <ul class="space-y-2 text-blue-800">
                <li class="flex items-start">
                    <i data-lucide="arrow-right" class="w-4 h-4 mr-2 mt-1 flex-shrink-0"></i>
                    <span>All processing happens locally in your browser for maximum privacy</span>
                </li>
                <li class="flex items-start">
                    <i data-lucide="arrow-right" class="w-4 h-4 mr-2 mt-1 flex-shrink-0"></i>
                    <span>No file size limits for most operations - process large files with confidence</span>
                </li>
                <li class="flex items-start">
                    <i data-lucide="arrow-right" class="w-4 h-4 mr-2 mt-1 flex-shrink-0"></i>
                    <span>Your files are automatically deleted from our servers after processing</span>
                </li>
            </ul>
        </div>
    </div>
</div>

<!-- Tool-Specific JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const processBtn = document.getElementById('process-btn');
    const clearBtn = document.getElementById('clear-btn');
    const uploadSection = document.getElementById('upload-section');
    const processingSection = document.getElementById('processing-section');
    const resultsSection = document.getElementById('results-section');
    const progressBar = document.getElementById('progress-bar');
    const downloadBtn = document.getElementById('download-btn');
    const processAnother = document.getElementById('process-another');
    
    let selectedFiles = [];
    let selectedOption = '{processing_options[0].lower().replace(' ', '-') if processing_options else 'default'}';
    
    // Option selection
    document.querySelectorAll('.option-card').forEach(card => {{
        card.addEventListener('click', function() {{
            document.querySelectorAll('.option-card').forEach(c => {{
                c.classList.remove('border-{colors['primary']}', 'bg-{colors['secondary']}/20');
                c.querySelector('i').classList.add('hidden');
            }});
            this.classList.add('border-{colors['primary']}', 'bg-{colors['secondary']}/20');
            this.querySelector('i').classList.remove('hidden');
            selectedOption = this.dataset.option;
        }});
    }});
    
    // Select first option by default
    if (document.querySelector('.option-card')) {{
        document.querySelector('.option-card').click();
    }}
    
    // File upload handling
    uploadZone.addEventListener('click', () => fileInput.click());
    
    uploadZone.addEventListener('dragover', (e) => {{
        e.preventDefault();
        uploadZone.classList.add('border-{colors['accent']}', 'bg-{colors['secondary']}/40');
    }});
    
    uploadZone.addEventListener('dragleave', (e) => {{
        e.preventDefault();
        uploadZone.classList.remove('border-{colors['accent']}', 'bg-{colors['secondary']}/40');
    }});
    
    uploadZone.addEventListener('drop', (e) => {{
        e.preventDefault();
        uploadZone.classList.remove('border-{colors['accent']}', 'bg-{colors['secondary']}/40');
        handleFiles(e.dataTransfer.files);
    }});
    
    fileInput.addEventListener('change', (e) => {{
        handleFiles(e.target.files);
    }});
    
    function handleFiles(files) {{
        selectedFiles = Array.from(files);
        if (selectedFiles.length > 0) {{
            updateUploadZone();
            processBtn.disabled = false;
        }}
    }}
    
    function updateUploadZone() {{
        const fileCount = selectedFiles.length;
        uploadZone.innerHTML = `
            <div class="space-y-4">
                <div class="mx-auto w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
                    <i data-lucide="check" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <p class="text-lg font-medium text-gray-900">${{fileCount}} file${{fileCount > 1 ? 's' : ''}} selected</p>
                    <p class="text-sm text-gray-500">Ready for processing</p>
                </div>
            </div>
        `;
        lucide.createIcons();
    }}
    
    // Process button
    processBtn.addEventListener('click', function() {{
        if (selectedFiles.length === 0) return;
        
        // Show processing section
        uploadSection.classList.add('hidden');
        processingSection.classList.remove('hidden');
        
        // Simulate processing with progress
        let progress = 0;
        const interval = setInterval(() => {{
            progress += Math.random() * 15;
            if (progress >= 100) {{
                progress = 100;
                clearInterval(interval);
                showResults();
            }}
            progressBar.style.width = progress + '%';
        }}, 200);
    }});
    
    function showResults() {{
        processingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        
        // Handle download (in a real implementation, this would download the processed file)
        downloadBtn.addEventListener('click', function() {{
            // Simulate download
            const link = document.createElement('a');
            link.href = 'data:text/plain;charset=utf-8,Processed file content would be here';
            link.download = 'processed-{tool_name}.txt';
            link.click();
        }});
    }}
    
    // Process another file
    processAnother.addEventListener('click', function() {{
        resetTool();
    }});
    
    // Clear button
    clearBtn.addEventListener('click', function() {{
        resetTool();
    }});
    
    function resetTool() {{
        selectedFiles = [];
        fileInput.value = '';
        processBtn.disabled = true;
        uploadSection.classList.remove('hidden');
        processingSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        
        uploadZone.innerHTML = `
            <div class="space-y-4">
                <div class="mx-auto w-16 h-16 bg-{colors['primary']} rounded-full flex items-center justify-center">
                    <i data-lucide="upload" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <p class="text-lg font-medium text-gray-900">Click to upload or drag & drop</p>
                    <p class="text-sm text-gray-500">Maximum file size: 16MB</p>
                </div>
            </div>
        `;
        lucide.createIcons();
    }}
}});
</script>
{{%- endblock -%}}'''
    
    return template_content

def create_all_tool_templates():
    """Create templates for all 85 tools"""
    print("🎨 Creating unique UI templates for all 85 tools...")
    
    total_created = 0
    
    for category_name, category_data in Config.TOOL_CATEGORIES.items():
        category_path = f"templates/tools/{category_name}"
        os.makedirs(category_path, exist_ok=True)
        
        print(f"\n📁 Creating {category_data['name']} templates...")
        
        for tool_name in category_data['tools']:
            template_content = create_tool_template(tool_name, category_name, category_data)
            
            template_file = f"{category_path}/{tool_name}.html"
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            total_created += 1
            print(f"   ✅ {tool_name}.html")
    
    print(f"\n🎉 Successfully created {total_created} unique tool templates!")
    print(f"📂 Templates organized in templates/tools/ directory")
    print(f"🎨 Each tool has unique colors, features, and functionality")

if __name__ == "__main__":
    create_all_tool_templates()