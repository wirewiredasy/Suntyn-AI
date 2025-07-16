"""
Video processing utilities for Toolora AI
Handles video trimming, audio extraction, and other operations
"""

import os
import uuid
import subprocess
import tempfile
import logging

class VideoProcessor:
    """Video processing utilities using FFmpeg"""
    
    @staticmethod
    def extract_audio(input_file, output_format='mp3'):
        """Extract audio from video file"""
        try:
            # Generate output filename
            output_filename = f"audio_{uuid.uuid4()}.{output_format}"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            # FFmpeg command to extract audio
            cmd = [
                'ffmpeg', '-i', input_file,
                '-vn',  # No video
                '-acodec', 'libmp3lame' if output_format == 'mp3' else 'aac',
                '-ab', '192k',  # Audio bitrate
                '-ar', '44100',  # Sample rate
                '-f', output_format,
                '-y',  # Overwrite output
                output_path
            ]
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                return output_path
            else:
                logging.error(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            logging.error(f"Video audio extraction error: {str(e)}")
            return None
    
    @staticmethod
    def trim_video(input_file, start_time=0, duration=None):
        """Trim video file"""
        try:
            # Generate output filename
            file_ext = os.path.splitext(input_file)[1].lower()
            output_filename = f"trimmed_{uuid.uuid4()}{file_ext}"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            # Build FFmpeg command
            cmd = ['ffmpeg', '-i', input_file, '-ss', str(start_time)]
            
            if duration:
                cmd.extend(['-t', str(duration)])
            
            cmd.extend(['-c', 'copy', '-y', output_path])
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                return output_path
            else:
                logging.error(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            logging.error(f"Video trim error: {str(e)}")
            return None
    
    @staticmethod
    def compress_video(input_file, crf=23):
        """Compress video file"""
        try:
            # Generate output filename
            file_ext = os.path.splitext(input_file)[1].lower()
            output_filename = f"compressed_{uuid.uuid4()}{file_ext}"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            # FFmpeg command for compression
            cmd = [
                'ffmpeg', '-i', input_file,
                '-c:v', 'libx264',  # Video codec
                '-crf', str(crf),   # Quality (lower = better quality)
                '-c:a', 'aac',      # Audio codec
                '-b:a', '128k',     # Audio bitrate
                '-y',               # Overwrite output
                output_path
            ]
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                return output_path
            else:
                logging.error(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            logging.error(f"Video compress error: {str(e)}")
            return None
    
    @staticmethod
    def remove_audio(input_file):
        """Remove audio from video file"""
        try:
            # Generate output filename
            file_ext = os.path.splitext(input_file)[1].lower()
            output_filename = f"no_audio_{uuid.uuid4()}{file_ext}"
            output_path = os.path.join('uploads', output_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            
            # FFmpeg command to remove audio
            cmd = [
                'ffmpeg', '-i', input_file,
                '-c:v', 'copy',  # Copy video stream
                '-an',           # No audio
                '-y',            # Overwrite output
                output_path
            ]
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Cleanup input file
                try:
                    os.remove(input_file)
                except:
                    pass
                return output_path
            else:
                logging.error(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            logging.error(f"Video audio removal error: {str(e)}")
            return None