"""
PDF processing utilities for Toolora AI
Handles PDF merge, split, compress, and other operations
"""

import os
import uuid
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import logging

class PDFProcessor:
    """PDF processing utilities"""
    
    @staticmethod
    def merge_pdfs(input_files):
        """Merge multiple PDF files into one"""
        try:
            writer = PdfWriter()
            
            for file_path in input_files:
                if os.path.exists(file_path):
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        writer.add_page(page)
            
            # Generate output filename
            output_filename = f"merged_{uuid.uuid4()}.pdf"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Cleanup input files
            for file_path in input_files:
                try:
                    os.remove(file_path)
                except:
                    pass
            
            return output_path
            
        except Exception as e:
            logging.error(f"PDF merge error: {str(e)}")
            return None
    
    @staticmethod
    def split_pdf(input_file, pages_per_file=1):
        """Split PDF into multiple files"""
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            output_files = []
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            for i in range(0, total_pages, pages_per_file):
                writer = PdfWriter()
                
                # Add pages to current split
                for j in range(i, min(i + pages_per_file, total_pages)):
                    writer.add_page(reader.pages[j])
                
                # Generate output filename
                output_filename = f"split_{uuid.uuid4()}_part_{i//pages_per_file + 1}.pdf"
                output_path = os.path.join('uploads', output_filename)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append(output_path)
            
            # Cleanup input file
            try:
                os.remove(input_file)
            except:
                pass
            
            return output_files
            
        except Exception as e:
            logging.error(f"PDF split error: {str(e)}")
            return None
    
    @staticmethod
    def compress_pdf(input_file, quality=0.7):
        """Compress PDF file"""
        try:
            reader = PdfReader(input_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            # Generate output filename
            output_filename = f"compressed_{uuid.uuid4()}.pdf"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Cleanup input file
            try:
                os.remove(input_file)
            except:
                pass
            
            return output_path
            
        except Exception as e:
            logging.error(f"PDF compress error: {str(e)}")
            return None
    
    @staticmethod
    def add_watermark(input_file, watermark_text):
        """Add watermark to PDF"""
        try:
            # Create watermark PDF
            watermark_path = f"watermark_{uuid.uuid4()}.pdf"
            c = canvas.Canvas(watermark_path, pagesize=letter)
            c.setFont("Helvetica", 50)
            c.setFillAlpha(0.3)
            c.rotate(45)
            c.drawString(200, 200, watermark_text)
            c.save()
            
            reader = PdfReader(input_file)
            watermark_reader = PdfReader(watermark_path)
            writer = PdfWriter()
            
            watermark_page = watermark_reader.pages[0]
            
            for page in reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            # Generate output filename
            output_filename = f"watermarked_{uuid.uuid4()}.pdf"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Cleanup
            try:
                os.remove(input_file)
                os.remove(watermark_path)
            except:
                pass
            
            return output_path
            
        except Exception as e:
            logging.error(f"PDF watermark error: {str(e)}")
            return None