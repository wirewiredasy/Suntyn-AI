import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz  # PyMuPDF for compression

def merge_pdfs(input_files, output_path):
    """Merge multiple PDF files into one"""
    try:
        merger = PdfMerger()
        
        for pdf_file in input_files:
            if os.path.exists(pdf_file):
                merger.append(pdf_file)
        
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)
        
        merger.close()
        return True
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False

def split_pdf(input_file, output_path, page_range):
    """Split PDF and extract specific pages"""
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        # Parse page range (e.g., "1-3", "1,3,5", "1-3,5")
        pages = []
        for part in page_range.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start-1, end))  # Convert to 0-based
            else:
                pages.append(int(part)-1)  # Convert to 0-based
        
        # Add selected pages
        for page_num in pages:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return False

def compress_pdf(input_file, output_path, compression_level='medium'):
    """Compress PDF file"""
    try:
        doc = fitz.open(input_file)
        
        # Compression settings
        compression_settings = {
            'low': (90, 150),
            'medium': (70, 100),
            'high': (50, 72)
        }
        
        quality, dpi = compression_settings.get(compression_level, (70, 100))
        
        # Get original size
        original_size = os.path.getsize(input_file)
        
        # Save with compression
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        
        # Get compressed size
        compressed_size = os.path.getsize(output_path)
        
        return True, original_size, compressed_size
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return False, 0, 0