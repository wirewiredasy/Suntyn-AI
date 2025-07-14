#!/usr/bin/env python3
"""
Script to create individual tool templates for all 85 tools in Toolora AI
This will ensure every tool has its own dedicated HTML template
"""

import os
from config import Config

def get_tool_specific_config(tool_name, category_data):
    """Get tool-specific configuration and descriptions"""
    
    tool_configs = {
        # PDF Tools
        'pdf-merge': {
            'title': 'PDF Merge',
            'description': 'Combine multiple PDF files into one document seamlessly',
            'features': ['Unlimited files', 'Preserve quality', 'Fast processing'],
            'accept_files': '.pdf',
            'instructions': 'Select multiple PDF files to merge them into a single document.'
        },
        'pdf-split': {
            'title': 'PDF Split',
            'description': 'Split PDF into multiple files or individual pages',
            'features': ['Split by pages', 'Custom ranges', 'Batch processing'],
            'accept_files': '.pdf',
            'instructions': 'Upload a PDF file and choose how to split it.'
        },
        'pdf-compress': {
            'title': 'PDF Compress',
            'description': 'Reduce PDF file size without quality loss using advanced compression',
            'features': ['Smart compression', 'Quality preserved', 'Significant reduction'],
            'accept_files': '.pdf',
            'instructions': 'Upload a PDF file to compress and reduce its size.'
        },
        'pdf-to-word': {
            'title': 'PDF to Word',
            'description': 'Convert PDF files to editable Word documents',
            'features': ['Maintain formatting', 'Editable output', 'High accuracy'],
            'accept_files': '.pdf',
            'instructions': 'Upload a PDF file to convert to Word format.'
        },
        'word-to-pdf': {
            'title': 'Word to PDF',
            'description': 'Convert Word documents to professional PDF files',
            'features': ['Professional output', 'Layout preserved', 'Universal compatibility'],
            'accept_files': '.doc,.docx',
            'instructions': 'Upload a Word document to convert to PDF format.'
        },
        
        # Image Tools
        'image-compress': {
            'title': 'Image Compress',
            'description': 'Reduce image file size while maintaining quality',
            'features': ['Smart compression', 'Quality control', 'Batch processing'],
            'accept_files': '.jpg,.jpeg,.png,.webp',
            'instructions': 'Upload images to compress and reduce file size.'
        },
        'image-resize': {
            'title': 'Image Resize',
            'description': 'Resize images to specific dimensions perfectly',
            'features': ['Custom dimensions', 'Aspect ratio', 'Batch resize'],
            'accept_files': '.jpg,.jpeg,.png,.webp,.gif',
            'instructions': 'Upload images and specify new dimensions.'
        },
        'background-remover': {
            'title': 'Background Remover',
            'description': 'Remove backgrounds from images automatically using AI',
            'features': ['AI-powered', 'Automatic detection', 'Clean results'],
            'accept_files': '.jpg,.jpeg,.png',
            'instructions': 'Upload an image to automatically remove its background.'
        },
        
        # Video Tools
        'video-trimmer': {
            'title': 'Video Trimmer',
            'description': 'Trim and cut video clips with precision',
            'features': ['Frame accuracy', 'Multiple formats', 'Quality preserved'],
            'accept_files': '.mp4,.avi,.mov,.mkv',
            'instructions': 'Upload a video and set start/end times for trimming.'
        },
        'video-to-mp3': {
            'title': 'Video to MP3',
            'description': 'Extract audio from video files as MP3',
            'features': ['High quality', 'Multiple formats', 'Fast extraction'],
            'accept_files': '.mp4,.avi,.mov,.mkv,.webm',
            'instructions': 'Upload a video file to extract audio as MP3.'
        },
        
        # AI Tools
        'resume-generator': {
            'title': 'Resume Generator',
            'description': 'Create professional resumes with AI assistance',
            'features': ['AI-powered', 'Professional templates', 'ATS-friendly'],
            'accept_files': 'text',
            'instructions': 'Enter your details to generate a professional resume.'
        },
        'business-name-generator': {
            'title': 'Business Name Generator',
            'description': 'Generate unique business names using AI',
            'features': ['Creative suggestions', 'Industry-specific', 'Available domains'],
            'accept_files': 'text',
            'instructions': 'Enter keywords and industry to generate business names.'
        }
    }
    
    # Default configuration for tools not specifically configured
    default_config = {
        'title': tool_name.replace('-', ' ').title(),
        'description': f'Professional {tool_name.replace("-", " ")} tool for your needs',
        'features': ['Fast processing', 'High quality', 'Secure'],
        'accept_files': '*/*',
        'instructions': f'Upload files to use the {tool_name.replace("-", " ")} tool.'
    }
    
    return tool_configs.get(tool_name, default_config)

def create_tool_template(tool_name, category_id, category_data):
    """Create a complete tool template"""
    
    config = get_tool_specific_config(tool_name, category_data)
    
    # Generate feature badges HTML
    feature_badges_html = ""
    for feature in config['features']:
        feature_badges_html += f'''
                <div class="flex items-center space-x-2 bg-white dark:bg-gray-800 px-4 py-2 rounded-full shadow-md">
                    <i data-lucide="check-circle" class="w-4 h-4 text-green-500"></i>
                    <span>{feature}</span>
                </div>'''
    
    template_content = f'''{{%% extends "base.html" %%}}

{{%% block title %%}}{config['title']} - Toolora AI{{%% endblock %%}}

{{%% block content %%}}
<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 pt-20">
    <div class="container mx-auto px-4 py-8">
        <!-- Breadcrumb -->
        <nav class="flex mb-8 animate__animated animate__fadeInDown" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 md:space-x-3">
                <li class="inline-flex items-center">
                    <a href="{{{{ url_for('main.index') }}}}" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-blue-600 dark:text-gray-400 dark:hover:text-white nav-link">
                        <i data-lucide="home" class="w-4 h-4 mr-2"></i>
                        Home
                    </a>
                </li>
                <li>
                    <div class="flex items-center">
                        <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        <a href="{{{{ url_for('tools.index') }}}}" class="ml-1 text-sm font-medium text-gray-700 hover:text-blue-600 md:ml-2 dark:text-gray-400 dark:hover:text-white nav-link">Tools</a>
                    </div>
                </li>
                <li>
                    <div class="flex items-center">
                        <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        <a href="{{{{ url_for('tools.index', category='{category_id}') }}}}" class="ml-1 text-sm font-medium text-gray-700 hover:text-blue-600 md:ml-2 dark:text-gray-400 dark:hover:text-white nav-link">
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

        <!-- Tool Header -->
        <div class="text-center mb-12 animate__animated animate__fadeInUp">
            <div class="inline-flex items-center justify-center w-24 h-24 rounded-3xl bg-gradient-to-br from-{category_data['color']}-100 to-{category_data['color']}-200 dark:from-{category_data['color']}-900 dark:to-{category_data['color']}-800 mb-6 shadow-lg floating">
                <i data-lucide="{category_data['icon']}" class="w-12 h-12 text-{category_data['color']}-600 dark:text-{category_data['color']}-400"></i>
            </div>
            <h1 class="text-5xl md:text-6xl font-bold text-gray-800 dark:text-white mb-4">
                {config['title']}
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8 leading-relaxed">
                {config['description']}
            </p>
            <div class="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500 dark:text-gray-400">{feature_badges_html}
            </div>
        </div>

        <!-- Tool Interface -->
        <div class="max-w-5xl mx-auto">
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl border border-gray-200 dark:border-gray-700 animate__animated animate__fadeInUp animate__delay-1s card-enhanced">
                <div class="p-8 md:p-12">
                    <!-- Instructions -->
                    <div class="mb-8 p-6 bg-{category_data['color']}-50 dark:bg-{category_data['color']}-900/20 rounded-2xl border border-{category_data['color']}-200 dark:border-{category_data['color']}-700">
                        <div class="flex items-start space-x-3">
                            <i data-lucide="info" class="w-6 h-6 text-{category_data['color']}-600 dark:text-{category_data['color']}-400 mt-1 flex-shrink-0"></i>
                            <div>
                                <h3 class="font-semibold text-{category_data['color']}-800 dark:text-{category_data['color']}-200 mb-2">How to use</h3>
                                <p class="text-{category_data['color']}-700 dark:text-{category_data['color']}-300">{config['instructions']}</p>
                            </div>
                        </div>
                    </div>

                    <!-- File Upload Area -->
                    <div id="upload-area" class="upload-area border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-2xl p-12 text-center hover:border-{category_data['color']}-400 dark:hover:border-{category_data['color']}-500 transition-all duration-500 cursor-pointer group" 
                         ondrop="handleDrop(event)" ondragover="handleDragOver(event)" ondragenter="handleDragEnter(event)" ondragleave="handleDragLeave(event)">
                        <div class="space-y-6">
                            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-{category_data['color']}-100 to-{category_data['color']}-200 dark:from-{category_data['color']}-900 dark:to-{category_data['color']}-800 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                <i data-lucide="upload-cloud" class="w-10 h-10 text-{category_data['color']}-600 dark:text-{category_data['color']}-400"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                                    Drop your files here or click to browse
                                </h3>
                                <p class="text-gray-500 dark:text-gray-400 text-lg">
                                    Supports: {config['accept_files']} • Maximum file size: 16MB
                                </p>
                            </div>
                            <input type="file" id="file-input" class="hidden" multiple accept="{config['accept_files']}" onchange="handleFileSelect(event)">
                            <button onclick="document.getElementById('file-input').click()" 
                                    class="btn-gradient btn-lg px-10 py-4 text-lg font-semibold rounded-2xl shadow-lg transform hover:scale-105 transition-all duration-300">
                                <i data-lucide="folder-open" class="w-6 h-6 mr-3"></i>
                                Select Files
                            </button>
                        </div>
                    </div>

                    <!-- File List -->
                    <div id="file-list" class="hidden mt-8">
                        <h4 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Selected Files</h4>
                        <div id="files-container" class="space-y-4"></div>
                    </div>

                    <!-- Tool Options -->
                    <div id="options-section" class="hidden mt-8">
                        <h4 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Processing Options</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Tool-specific options will be added here via JavaScript -->
                        </div>
                    </div>

                    <!-- Process Button -->
                    <div id="process-section" class="hidden mt-8 text-center">
                        <button id="process-btn" onclick="processFiles()" 
                                class="btn-gradient btn-lg px-16 py-5 text-xl font-bold rounded-2xl shadow-xl transform hover:scale-105 transition-all duration-300 pulse-cta">
                            <i data-lucide="play" class="w-6 h-6 mr-3"></i>
                            Process Files
                        </button>
                    </div>

                    <!-- Progress -->
                    <div id="progress-section" class="hidden mt-8">
                        <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-4 mb-6 overflow-hidden">
                            <div id="progress-bar" class="progress-bar bg-gradient-to-r from-{category_data['color']}-500 to-{category_data['color']}-600 h-4 rounded-full transition-all duration-500" style="width: 0%"></div>
                        </div>
                        <p id="progress-text" class="text-center text-lg text-gray-600 dark:text-gray-300 font-medium">Processing files...</p>
                    </div>

                    <!-- Results -->
                    <div id="results-section" class="hidden mt-8">
                        <h4 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Processed Files</h4>
                        <div id="results-container" class="space-y-4"></div>
                    </div>
                </div>
            </div>

            <!-- Feature Cards -->
            <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 animate__animated animate__fadeInUp animate__delay-2s">
                <div class="card-enhanced bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900 dark:to-blue-800 rounded-2xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="shield" class="w-8 h-8 text-blue-600 dark:text-blue-400"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">100% Secure</h3>
                    <p class="text-gray-600 dark:text-gray-300 leading-relaxed">All files are processed locally and automatically deleted after processing for maximum security.</p>
                </div>
                
                <div class="card-enhanced bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
                    <div class="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900 dark:to-green-800 rounded-2xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="zap" class="w-8 h-8 text-green-600 dark:text-green-400"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Lightning Fast</h3>
                    <p class="text-gray-600 dark:text-gray-300 leading-relaxed">Optimized algorithms ensure quick processing without compromising on quality or accuracy.</p>
                </div>
                
                <div class="card-enhanced bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
                    <div class="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900 dark:to-purple-800 rounded-2xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="heart" class="w-8 h-8 text-purple-600 dark:text-purple-400"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Always Free</h3>
                    <p class="text-gray-600 dark:text-gray-300 leading-relaxed">No registration required. All tools are completely free to use with unlimited access.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Enhanced file handling functionality with animations
let selectedFiles = [];
const toolName = '{tool_name}';
const category = '{category_id}';

function handleDragOver(e) {{
    e.preventDefault();
    e.stopPropagation();
}}

function handleDragEnter(e) {{
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = e.target.closest('#upload-area');
    uploadArea.classList.add('drag-over', 'border-{category_data['color']}-400', 'bg-{category_data['color']}-50', 'dark:bg-{category_data['color']}-900', 'scale-105');
}}

function handleDragLeave(e) {{
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = e.target.closest('#upload-area');
    uploadArea.classList.remove('drag-over', 'border-{category_data['color']}-400', 'bg-{category_data['color']}-50', 'dark:bg-{category_data['color']}-900', 'scale-105');
}}

function handleDrop(e) {{
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = e.target.closest('#upload-area');
    uploadArea.classList.remove('drag-over', 'border-{category_data['color']}-400', 'bg-{category_data['color']}-50', 'dark:bg-{category_data['color']}-900', 'scale-105');
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}}

function handleFileSelect(e) {{
    const files = Array.from(e.target.files);
    addFiles(files);
}}

function addFiles(files) {{
    selectedFiles = [...selectedFiles, ...files];
    displayFiles();
    showSection('file-list');
    showSection('process-section');
    
    // Add tool-specific options if needed
    if (toolName.includes('resize') || toolName.includes('compress')) {{
        showSection('options-section');
        addToolOptions();
    }}
}}

function displayFiles() {{
    const container = document.getElementById('files-container');
    container.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {{
        const fileElement = document.createElement('div');
        fileElement.className = 'flex items-center justify-between p-6 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-xl border border-gray-200 dark:border-gray-600 animate__animated animate__fadeInUp interactive-element';
        fileElement.style.animationDelay = `${{index * 0.1}}s`;
        
        fileElement.innerHTML = `
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-{category_data['color']}-100 dark:bg-{category_data['color']}-900 rounded-xl flex items-center justify-center">
                    <i data-lucide="file" class="w-6 h-6 text-{category_data['color']}-600 dark:text-{category_data['color']}-400"></i>
                </div>
                <div>
                    <div class="font-semibold text-gray-900 dark:text-white text-lg">${{file.name}}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">${{formatFileSize(file.size)}}</div>
                </div>
            </div>
            <button onclick="removeFile(${{index}})" class="p-3 text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900 rounded-xl transition-all duration-200 interactive-element">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
        `;
        container.appendChild(fileElement);
    }});
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {{
        lucide.createIcons();
    }}
}}

function removeFile(index) {{
    selectedFiles.splice(index, 1);
    displayFiles();
    
    if (selectedFiles.length === 0) {{
        hideSection('file-list');
        hideSection('process-section');
        hideSection('options-section');
    }}
}}

function showSection(sectionId) {{
    const section = document.getElementById(sectionId);
    if (section) {{
        section.classList.remove('hidden');
        section.classList.add('animate__animated', 'animate__fadeInUp');
    }}
}}

function hideSection(sectionId) {{
    const section = document.getElementById(sectionId);
    if (section) {{
        section.classList.add('hidden');
    }}
}}

function addToolOptions() {{
    const optionsContainer = document.querySelector('#options-section .grid');
    if (!optionsContainer) return;
    
    // Add tool-specific options based on tool type
    if (toolName.includes('resize')) {{
        optionsContainer.innerHTML = `
            <div class="bg-white dark:bg-gray-700 p-6 rounded-xl border border-gray-200 dark:border-gray-600">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Width (px)</label>
                <input type="number" id="width" class="form-input w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg" placeholder="800">
            </div>
            <div class="bg-white dark:bg-gray-700 p-6 rounded-xl border border-gray-200 dark:border-gray-600">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Height (px)</label>
                <input type="number" id="height" class="form-input w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg" placeholder="600">
            </div>
        `;
    }} else if (toolName.includes('compress')) {{
        optionsContainer.innerHTML = `
            <div class="bg-white dark:bg-gray-700 p-6 rounded-xl border border-gray-200 dark:border-gray-600 col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Quality Level</label>
                <input type="range" id="quality" min="10" max="100" value="85" class="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700">
                <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400 mt-2">
                    <span>Lower Size</span>
                    <span id="quality-value">85%</span>
                    <span>Higher Quality</span>
                </div>
            </div>
        `;
        
        // Add quality slider listener
        const qualitySlider = document.getElementById('quality');
        const qualityValue = document.getElementById('quality-value');
        if (qualitySlider && qualityValue) {{
            qualitySlider.addEventListener('input', function() {{
                qualityValue.textContent = this.value + '%';
            }});
        }}
    }}
}}

function processFiles() {{
    if (selectedFiles.length === 0) return;
    
    showSection('progress-section');
    document.getElementById('process-btn').disabled = true;
    document.getElementById('process-btn').innerHTML = '<i data-lucide="loader" class="w-6 h-6 mr-3 animate-spin"></i>Processing...';
    
    // Simulate processing with realistic progress
    simulateProcessing();
}}

function simulateProcessing() {{
    let progress = 0;
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    
    const interval = setInterval(() => {{
        progress += Math.random() * 15 + 5;
        if (progress >= 100) {{
            progress = 100;
            clearInterval(interval);
            setTimeout(showResults, 500);
        }}
        
        progressBar.style.width = progress + '%';
        progressText.textContent = `Processing files... ${{Math.round(progress)}}%`;
    }}, 300);
}}

function showResults() {{
    showSection('results-section');
    document.getElementById('progress-text').textContent = 'Processing complete!';
    
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {{
        const resultElement = document.createElement('div');
        resultElement.className = 'flex items-center justify-between p-6 bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 rounded-xl border border-green-200 dark:border-green-700 animate__animated animate__fadeInUp';
        resultElement.style.animationDelay = `${{index * 0.1}}s`;
        
        resultElement.innerHTML = `
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-xl flex items-center justify-center">
                    <i data-lucide="check-circle" class="w-6 h-6 text-green-600 dark:text-green-400"></i>
                </div>
                <div>
                    <div class="font-semibold text-gray-900 dark:text-white text-lg">processed_${{file.name}}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">Ready for download</div>
                </div>
            </div>
            <button onclick="downloadFile('processed_${{file.name}}')" class="btn bg-green-600 hover:bg-green-700 text-white border-none px-6 py-3 rounded-xl transform hover:scale-105 transition-all duration-200">
                <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                Download
            </button>
        `;
        container.appendChild(resultElement);
    }});
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {{
        lucide.createIcons();
    }}
}}

function downloadFile(filename) {{
    // In a real implementation, this would trigger actual file download
    console.log('Downloading:', filename);
    showNotification('Download started!', 'success');
}}

function formatFileSize(bytes) {{
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}}

function showNotification(message, type = 'info') {{
    // Simple notification system
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 z-50 p-4 rounded-xl shadow-lg ${{
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    setTimeout(() => {{
        notification.remove();
    }}, 3000);
}}

// Initialize upload area click handler
document.addEventListener('DOMContentLoaded', function() {{
    const uploadArea = document.getElementById('upload-area');
    if (uploadArea) {{
        uploadArea.addEventListener('click', (e) => {{
            if (e.target.tagName !== 'BUTTON') {{
                document.getElementById('file-input').click();
            }}
        }});
    }}
}});
</script>
{{%% endblock %%}}'''
    
    return template_content

def main():
    """Generate all tool templates"""
    
    # Create templates/tools directory if it doesn't exist
    os.makedirs('templates/tools', exist_ok=True)
    
    total_created = 0
    
    for category_id, category_data in Config.TOOL_CATEGORIES.items():
        print(f"Creating templates for {category_data['name']} ({len(category_data['tools'])} tools)...")
        
        for tool_name in category_data['tools']:
            template_path = f"templates/tools/{tool_name}.html"
            
            # Check if template already exists
            if os.path.exists(template_path):
                print(f"  ✓ {tool_name}.html (already exists)")
                continue
            
            # Create the template
            template_content = create_tool_template(tool_name, category_id, category_data)
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            total_created += 1
            print(f"  ✓ Created {tool_name}.html")
    
    print(f"\n🎉 Successfully created {total_created} new tool templates!")
    print(f"📊 Total tools now have templates: {len(os.listdir('templates/tools')) - 1}")  # -1 for index.html

if __name__ == "__main__":
    main()