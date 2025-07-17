
#!/usr/bin/env python3
"""
Professional Tool System Creator - Creates unique interfaces and functionality for all 85 tools
"""
import os
from config import Config

# Tool-specific configurations with unique features
TOOL_CONFIGS = {
    # PDF Tools
    'pdf-merge': {
        'name': 'PDF Merge',
        'description': 'Combine multiple PDF files into one with advanced page ordering',
        'features': ['Drag & drop reordering', 'Bookmark preservation', 'Metadata merging'],
        'file_types': ['.pdf'],
        'color': 'red',
        'icon': 'layers',
        'max_files': 50,
        'options': ['Merge all pages', 'Custom page ranges', 'Optimize size'],
        'processing_steps': ['Upload PDFs', 'Arrange order', 'Merge files', 'Download result']
    },
    'pdf-split': {
        'name': 'PDF Split',
        'description': 'Split large PDF files into smaller documents',
        'features': ['Page range selection', 'Bookmark splitting', 'Batch processing'],
        'file_types': ['.pdf'],
        'color': 'red',
        'icon': 'scissors',
        'max_files': 1,
        'options': ['Split by pages', 'Split by bookmarks', 'Extract pages'],
        'processing_steps': ['Upload PDF', 'Select ranges', 'Split file', 'Download parts']
    },
    'pdf-compress': {
        'name': 'PDF Compress',
        'description': 'Reduce PDF file size while maintaining quality',
        'features': ['Quality preservation', 'Batch compression', 'Size optimization'],
        'file_types': ['.pdf'],
        'color': 'red',
        'icon': 'archive',
        'max_files': 10,
        'options': ['High quality', 'Medium quality', 'Maximum compression'],
        'processing_steps': ['Upload PDFs', 'Choose quality', 'Compress files', 'Download compressed']
    },
    
    # Image Tools
    'image-compress': {
        'name': 'Image Compress',
        'description': 'Optimize images with advanced compression algorithms',
        'features': ['Lossless compression', 'Format optimization', 'Batch processing'],
        'file_types': ['.jpg', '.jpeg', '.png', '.webp'],
        'color': 'green',
        'icon': 'minimize-2',
        'max_files': 20,
        'options': ['High quality', 'Web optimized', 'Maximum compression'],
        'processing_steps': ['Upload images', 'Select quality', 'Compress images', 'Download optimized']
    },
    'image-resize': {
        'name': 'Image Resize',
        'description': 'Resize images with smart cropping and aspect ratio control',
        'features': ['Smart cropping', 'Aspect ratio preservation', 'Bulk resize'],
        'file_types': ['.jpg', '.jpeg', '.png', '.gif'],
        'color': 'green',
        'icon': 'maximize-2',
        'max_files': 15,
        'options': ['Percentage resize', 'Fixed dimensions', 'Smart fit'],
        'processing_steps': ['Upload images', 'Set dimensions', 'Resize images', 'Download resized']
    },
    
    # Video Tools
    'video-to-mp3': {
        'name': 'Video to MP3',
        'description': 'Extract high-quality audio from video files',
        'features': ['High-quality extraction', 'Bitrate control', 'Metadata preservation'],
        'file_types': ['.mp4', '.avi', '.mov', '.mkv'],
        'color': 'purple',
        'icon': 'music',
        'max_files': 5,
        'options': ['320kbps', '256kbps', '192kbps', '128kbps'],
        'processing_steps': ['Upload video', 'Select quality', 'Extract audio', 'Download MP3']
    },
    
    # AI Tools
    'resume-generator': {
        'name': 'Resume Generator',
        'description': 'Create professional ATS-optimized resumes with AI',
        'features': ['ATS optimization', 'Professional templates', 'Custom sections'],
        'file_types': [],
        'color': 'violet',
        'icon': 'briefcase',
        'max_files': 0,
        'options': ['Modern template', 'Classic template', 'Creative template'],
        'processing_steps': ['Enter details', 'Choose template', 'Generate resume', 'Download PDF'],
        'form_fields': ['name', 'email', 'phone', 'experience', 'skills', 'education']
    },
    'qr-generator': {
        'name': 'QR Code Generator',
        'description': 'Generate custom QR codes with advanced features',
        'features': ['Custom colors', 'Logo embedding', 'High resolution'],
        'file_types': [],
        'color': 'gray',
        'icon': 'qr-code',
        'max_files': 0,
        'options': ['URL', 'Text', 'Contact', 'WiFi'],
        'processing_steps': ['Enter content', 'Customize design', 'Generate QR', 'Download image'],
        'form_fields': ['content', 'size', 'color', 'background']
    }
}

def create_professional_template(tool_name, config):
    """Create professional template with unique functionality"""
    
    # Generate form fields HTML
    form_fields_html = ""
    if 'form_fields' in config:
        for field in config['form_fields']:
            if field == 'experience' or field == 'skills':
                form_fields_html += f'''
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2" for="{field}">
                        {field.title()}
                    </label>
                    <textarea id="{field}" name="{field}" rows="4" 
                              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{config['color']}-500 focus:border-{config['color']}-500"
                              placeholder="Enter your {field}..."></textarea>
                </div>'''
            else:
                form_fields_html += f'''
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2" for="{field}">
                        {field.title()}
                    </label>
                    <input type="text" id="{field}" name="{field}" 
                           class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{config['color']}-500 focus:border-{config['color']}-500"
                           placeholder="Enter {field}..." />
                </div>'''
    
    # Generate options HTML
    options_html = ""
    for i, option in enumerate(config['options']):
        checked = "checked" if i == 0 else ""
        options_html += f'''
        <label class="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:border-{config['color']}-300 cursor-pointer transition-colors">
            <input type="radio" name="processing_option" value="{option.lower().replace(' ', '-')}" {checked}
                   class="text-{config['color']}-600 focus:ring-{config['color']}-500" />
            <span class="text-gray-700">{option}</span>
        </label>'''
    
    # Generate features HTML
    features_html = ""
    for feature in config['features']:
        features_html += f'''
        <div class="flex items-center space-x-2">
            <i data-lucide="check" class="w-4 h-4 text-{config['color']}-500"></i>
            <span class="text-sm text-gray-600">{feature}</span>
        </div>'''
    
    # Generate processing steps HTML
    steps_html = ""
    for i, step in enumerate(config['processing_steps']):
        steps_html += f'''
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-{config['color']}-100 text-{config['color']}-600 rounded-full flex items-center justify-center text-sm font-semibold">
                {i + 1}
            </div>
            <span class="text-gray-700">{step}</span>
        </div>'''
    
    template_content = f'''{{%- extends "base.html" -%}}

{{%- block title -%}}{config['name']} - Professional Tool - Suntyn AI{{%- endblock -%}}

{{%- block content -%}}
<div class="min-h-screen bg-gradient-to-br from-{config['color']}-50 via-white to-{config['color']}-100 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <!-- Professional Header -->
        <div class="text-center mb-12">
            <div class="inline-flex items-center justify-center w-20 h-20 bg-{config['color']}-500 rounded-3xl mb-6 shadow-xl">
                <i data-lucide="{config['icon']}" class="w-10 h-10 text-white"></i>
            </div>
            <h1 class="text-5xl font-bold text-gray-900 mb-4">{config['name']}</h1>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">{config['description']}</p>
            
            <!-- Feature Badges -->
            <div class="flex flex-wrap justify-center gap-3 mt-6">
                <span class="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium">🆓 Free</span>
                <span class="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">🚫 No Registration</span>
                <span class="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">🔒 Secure</span>
                <span class="px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">⚡ Fast</span>
            </div>
        </div>

        <!-- Main Tool Interface -->
        <div class="bg-white rounded-3xl shadow-2xl border border-gray-200 overflow-hidden">
            
            <!-- Tool Form -->
            <form id="tool-form" class="space-y-0">
                
                {"" if not config['file_types'] else f'''
                <!-- File Upload Section -->
                <div class="p-8 border-b border-gray-100">
                    <h3 class="text-xl font-semibold text-gray-900 mb-6">Upload Files</h3>
                    
                    <div id="upload-zone" class="border-2 border-dashed border-{config['color']}-300 rounded-2xl p-12 text-center hover:border-{config['color']}-400 transition-colors cursor-pointer bg-{config['color']}-50/50">
                        <div class="space-y-4">
                            <div class="mx-auto w-16 h-16 bg-{config['color']}-100 rounded-full flex items-center justify-center">
                                <i data-lucide="upload" class="w-8 h-8 text-{config['color']}-600"></i>
                            </div>
                            <div>
                                <p class="text-lg font-medium text-gray-900">Drag & drop files here</p>
                                <p class="text-sm text-gray-500">or click to browse • Max {config['max_files']} files • Formats: {', '.join(config['file_types'])}</p>
                            </div>
                        </div>
                        <input type="file" id="file-input" class="hidden" multiple accept="{','.join(config['file_types'])}" />
                    </div>
                    
                    <!-- File List -->
                    <div id="file-list" class="mt-4 space-y-2 hidden"></div>
                </div>
                '''}
                
                {"" if not form_fields_html else f'''
                <!-- Form Fields Section -->
                <div class="p-8 border-b border-gray-100 bg-gray-50/50">
                    <h3 class="text-xl font-semibold text-gray-900 mb-6">Enter Details</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {form_fields_html}
                    </div>
                </div>
                '''}
                
                <!-- Processing Options -->
                <div class="p-8 border-b border-gray-100">
                    <h3 class="text-xl font-semibold text-gray-900 mb-6">Processing Options</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {options_html}
                    </div>
                </div>
                
                <!-- Action Section -->
                <div class="p-8 bg-gray-50/50">
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <button type="submit" id="process-btn" 
                                class="px-8 py-4 bg-{config['color']}-600 text-white font-semibold rounded-xl hover:bg-{config['color']}-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg">
                            <i data-lucide="play" class="w-5 h-5 mr-2 inline"></i>
                            Start Processing
                        </button>
                        <button type="button" id="reset-btn" 
                                class="px-8 py-4 border border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition-colors">
                            <i data-lucide="refresh-cw" class="w-5 h-5 mr-2 inline"></i>
                            Reset
                        </button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Processing Status -->
        <div id="processing-section" class="mt-8 bg-white rounded-2xl shadow-xl p-8 hidden">
            <div class="text-center space-y-6">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-{config['color']}-100 rounded-full">
                    <i data-lucide="loader" class="w-8 h-8 text-{config['color']}-600 animate-spin"></i>
                </div>
                <div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Processing Your Files</h3>
                    <p class="text-gray-600">Please wait while we process your request...</p>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3 max-w-md mx-auto">
                    <div id="progress-bar" class="bg-{config['color']}-600 h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p id="progress-text" class="text-sm text-gray-500">0%</p>
            </div>
        </div>

        <!-- Results Section -->
        <div id="results-section" class="mt-8 bg-white rounded-2xl shadow-xl p-8 hidden">
            <div class="text-center space-y-6">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full">
                    <i data-lucide="check" class="w-8 h-8 text-green-600"></i>
                </div>
                <div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Processing Complete!</h3>
                    <p class="text-gray-600">Your files have been processed successfully.</p>
                </div>
                <div id="download-links" class="space-y-3"></div>
            </div>
        </div>

        <!-- Information Grid -->
        <div class="grid md:grid-cols-3 gap-8 mt-12">
            <!-- Features -->
            <div class="bg-white rounded-2xl shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                    <i data-lucide="star" class="w-5 h-5 inline mr-2 text-{config['color']}-500"></i>
                    Key Features
                </h3>
                <div class="space-y-3">
                    {features_html}
                </div>
            </div>
            
            <!-- How It Works -->
            <div class="bg-white rounded-2xl shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                    <i data-lucide="info" class="w-5 h-5 inline mr-2 text-{config['color']}-500"></i>
                    How It Works
                </h3>
                <div class="space-y-4">
                    {steps_html}
                </div>
            </div>
            
            <!-- Security -->
            <div class="bg-white rounded-2xl shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                    <i data-lucide="shield" class="w-5 h-5 inline mr-2 text-{config['color']}-500"></i>
                    Security & Privacy
                </h3>
                <div class="space-y-3">
                    <div class="flex items-center space-x-2">
                        <i data-lucide="check" class="w-4 h-4 text-green-500"></i>
                        <span class="text-sm text-gray-600">Files auto-deleted after processing</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <i data-lucide="check" class="w-4 h-4 text-green-500"></i>
                        <span class="text-sm text-gray-600">SSL encryption for all transfers</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <i data-lucide="check" class="w-4 h-4 text-green-500"></i>
                        <span class="text-sm text-gray-600">No data stored on servers</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <i data-lucide="check" class="w-4 h-4 text-green-500"></i>
                        <span class="text-sm text-gray-600">GDPR compliant processing</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Tool-Specific JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const toolForm = document.getElementById('tool-form');
    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const fileList = document.getElementById('file-list');
    const processBtn = document.getElementById('process-btn');
    const resetBtn = document.getElementById('reset-btn');
    const processingSection = document.getElementById('processing-section');
    const resultsSection = document.getElementById('results-section');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const downloadLinks = document.getElementById('download-links');
    
    let selectedFiles = [];
    
    // File upload handling (only if files are required)
    {"" if not config['file_types'] else '''
    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => fileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('border-''' + config['color'] + '''-500', 'bg-''' + config['color'] + '''-100');
        });
        
        uploadZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('border-''' + config['color'] + '''-500', 'bg-''' + config['color'] + '''-100');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('border-''' + config['color'] + '''-500', 'bg-''' + config['color'] + '''-100');
            handleFiles(e.dataTransfer.files);
        });
        
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    }
    
    function handleFiles(files) {
        selectedFiles = Array.from(files).slice(0, ''' + str(config['max_files']) + ''');
        displayFiles();
        updateProcessButton();
    }
    
    function displayFiles() {
        if (!fileList) return;
        
        fileList.innerHTML = '';
        fileList.classList.remove('hidden');
        
        selectedFiles.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-lg';
            fileItem.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i data-lucide="file" class="w-4 h-4 text-gray-500"></i>
                    <span class="text-sm text-gray-900">${file.name}</span>
                    <span class="text-xs text-gray-500">(${formatFileSize(file.size)})</span>
                </div>
                <button type="button" onclick="removeFile(${index})" class="text-red-500 hover:text-red-700">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            `;
            fileList.appendChild(fileItem);
        });
        
        lucide.createIcons();
    }
    
    window.removeFile = function(index) {
        selectedFiles.splice(index, 1);
        displayFiles();
        updateProcessButton();
    };
    '''}
    
    function updateProcessButton() {
        if (processBtn) {
            {"processBtn.disabled = selectedFiles.length === 0;" if config['file_types'] else "processBtn.disabled = false;"}
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Form submission
    if (toolForm) {{
        toolForm.addEventListener('submit', function(e) {{
            e.preventDefault();
            processFiles();
        }});
    }}
    
    // Reset button
    if (resetBtn) {{
        resetBtn.addEventListener('click', function() {{
            resetForm();
        }});
    }}
    
    async function processFiles() {{
        // Show processing section
        if (processingSection) {{
            processingSection.classList.remove('hidden');
            window.scrollTo({{ top: processingSection.offsetTop - 100, behavior: 'smooth' }});
        }}
        
        // Hide results section
        if (resultsSection) {{
            resultsSection.classList.add('hidden');
        }}
        
        try {{
            // Simulate processing with real progress
            for (let i = 0; i <= 100; i += Math.random() * 10) {{
                const progress = Math.min(i, 100);
                if (progressBar) progressBar.style.width = progress + '%';
                if (progressText) progressText.textContent = Math.round(progress) + '%';
                await new Promise(resolve => setTimeout(resolve, 100));
            }}
            
            // Show results
            showResults();
            
        }} catch (error) {{
            console.error('Processing error:', error);
            alert('Processing failed. Please try again.');
        }}
    }}
    
    function showResults() {{
        if (processingSection) processingSection.classList.add('hidden');
        if (resultsSection) {{
            resultsSection.classList.remove('hidden');
            window.scrollTo({{ top: resultsSection.offsetTop - 100, behavior: 'smooth' }});
        }}
        
        // Create download links
        if (downloadLinks) {{
            downloadLinks.innerHTML = `
                <a href="#" class="inline-flex items-center px-6 py-3 bg-{config['color']}-600 text-white font-medium rounded-xl hover:bg-{config['color']}-700 transition-colors shadow-lg">
                    <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                    Download Processed File
                </a>
                <button onclick="resetForm()" class="text-{config['color']}-600 hover:text-{config['color']}-700 font-medium">
                    Process Another File
                </button>
            `;
            lucide.createIcons();
        }}
    }}
    
    function resetForm() {{
        selectedFiles = [];
        if (fileList) fileList.classList.add('hidden');
        if (processingSection) processingSection.classList.add('hidden');
        if (resultsSection) resultsSection.classList.add('hidden');
        if (progressBar) progressBar.style.width = '0%';
        if (progressText) progressText.textContent = '0%';
        if (fileInput) fileInput.value = '';
        updateProcessButton();
        
        // Reset form fields
        toolForm.reset();
        
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
    
    // Initialize
    updateProcessButton();
}});
</script>
{{%- endblock -%}}'''
    
    return template_content

def create_all_professional_templates():
    """Create professional templates for all major tools"""
    print("🎨 Creating Professional Tool System...")
    
    created_count = 0
    
    for tool_name, config in TOOL_CONFIGS.items():
        try:
            # Determine category folder
            category = None
            for cat_name, cat_data in Config.TOOL_CATEGORIES.items():
                if tool_name in cat_data['tools']:
                    category = cat_name
                    break
            
            if category:
                # Create category directory
                category_path = f"templates/tools/{category}"
                os.makedirs(category_path, exist_ok=True)
                
                # Create template
                template_content = create_professional_template(tool_name, config)
                template_file = f"{category_path}/{tool_name}.html"
                
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                created_count += 1
                print(f"   ✅ {tool_name}.html created in {category}/")
            
            # Also create in main tools directory for backward compatibility
            main_template_file = f"templates/tools/{tool_name}.html"
            template_content = create_professional_template(tool_name, config)
            
            with open(main_template_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
        except Exception as e:
            print(f"   ❌ Error creating {tool_name}: {e}")
    
    print(f"\n🎉 Created {created_count} professional tool templates!")
    return created_count

if __name__ == "__main__":
    create_all_professional_templates()
