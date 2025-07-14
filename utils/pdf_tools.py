
import os
import tempfile
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PDFProcessor:
    @staticmethod
    def merge_pdfs(file_paths):
        """Merge multiple PDF files into one"""
        writer = PdfWriter()
        
        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
        
        # Save to uploads directory
        os.makedirs('uploads', exist_ok=True)
        output_filename = f"merged_{secure_filename('document')}.pdf"
        output_path = os.path.join('uploads', output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def split_pdf(file_path, pages_per_file=1):
        """Split PDF into separate files"""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            output_files = []
            
            os.makedirs('uploads', exist_ok=True)
            
            for i in range(0, total_pages, pages_per_file):
                writer = PdfWriter()
                
                # Add pages to writer
                for j in range(i, min(i + pages_per_file, total_pages)):
                    writer.add_page(reader.pages[j])
                
                # Save split file
                output_filename = f"split_part_{i//pages_per_file + 1}.pdf"
                output_path = os.path.join('uploads', output_filename)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append(output_path)
            
            return output_files
    
    @staticmethod
    def compress_pdf(file_path, quality=0.7):
        """Compress PDF file"""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            os.makedirs('uploads', exist_ok=True)
            output_filename = f"compressed_{secure_filename(os.path.basename(file_path))}"
            output_path = os.path.join('uploads', output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
    
    @staticmethod
    def add_watermark(file, watermark_text, position='center', opacity=0.5):
        """Add watermark to PDF"""
        reader = PdfReader(file)
        writer = PdfWriter()
        
        # Create watermark
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillAlpha(opacity)
        can.drawString(100, 100, watermark_text)
        can.save()
        
        packet.seek(0)
        watermark = PdfReader(packet)
        
        for page in reader.pages:
            page.merge_page(watermark.pages[0])
            writer.add_page(page)
        
        os.makedirs('uploads', exist_ok=True)
        output_filename = f"watermarked_{secure_filename(file.filename)}"
        output_path = os.path.join('uploads', output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def rotate_pdf(file, rotation=90):
        """Rotate PDF pages"""
        reader = PdfReader(file)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)
        
        os.makedirs('uploads', exist_ok=True)
        output_filename = f"rotated_{secure_filename(file.filename)}"
        output_path = os.path.join('uploads', output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def extract_pages(file, page_numbers):
        """Extract specific pages from PDF"""
        reader = PdfReader(file)
        writer = PdfWriter()
        
        for page_num in page_numbers:
            if 0 <= page_num - 1 < len(reader.pages):
                writer.add_page(reader.pages[page_num - 1])
        
        os.makedirs('uploads', exist_ok=True)
        output_filename = f"extracted_{secure_filename(file.filename)}"
        output_path = os.path.join('uploads', output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
