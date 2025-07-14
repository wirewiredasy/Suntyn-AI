import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def merge_pdfs(pdf_paths, output_path):
    """Merge multiple PDF files into one"""
    try:
        writer = PdfWriter()
        
        for pdf_path in pdf_paths:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False

def split_pdf(pdf_path, output_dir, pages_per_file=1):
    """Split PDF into multiple files"""
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        files_created = []
        
        for i in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            
            for page_num in range(i, min(i + pages_per_file, total_pages)):
                writer.add_page(reader.pages[page_num])
            
            output_filename = f"split_page_{i+1}-{min(i+pages_per_file, total_pages)}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            files_created.append(output_path)
        
        return files_created
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return []

def compress_pdf(input_path, output_path, quality=0.4):
    """Compress PDF file"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return False

def add_watermark(input_path, output_path, watermark_text):
    """Add watermark to PDF"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Create watermark
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.setFont("Helvetica", 50)
        c.drawString(100, 400, watermark_text)
        c.save()
        
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error adding watermark: {e}")
        return False

def rotate_pdf(input_path, output_path, rotation_angle=90):
    """Rotate PDF pages"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(rotation_angle)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error rotating PDF: {e}")
        return False

def extract_pages(input_path, output_path, page_numbers):
    """Extract specific pages from PDF"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page_num in page_numbers:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error extracting pages: {e}")
        return False
