import os
import subprocess
import tempfile

def trim_video(input_file, output_path, start_time, end_time):
    """Trim video to specified time range"""
    try:
        # Use ffmpeg to trim video
        cmd = [
            'ffmpeg', '-i', input_file,
            '-ss', str(start_time),
            '-t', str(end_time - start_time),
            '-c', 'copy',
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error trimming video: {e}")
        return False

def extract_audio(input_file, output_path):
    """Extract audio from video file"""
    try:
        # Use ffmpeg to extract audio
        cmd = [
            'ffmpeg', '-i', input_file,
            '-vn',  # No video
            '-acodec', 'mp3',
            '-ab', '192k',  # Audio bitrate
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False

def compress_video(input_file, output_path, quality='medium'):
    """Compress video file"""
    try:
        # Quality settings
        quality_settings = {
            'low': '28',
            'medium': '23',
            'high': '18'
        }
        
        crf = quality_settings.get(quality, '23')
        
        # Use ffmpeg to compress video
        cmd = [
            'ffmpeg', '-i', input_file,
            '-c:v', 'libx264',
            '-crf', crf,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error compressing video: {e}")
        return False

def convert_video_format(input_file, output_path, output_format):
    """Convert video to different format"""
    try:
        # Use ffmpeg to convert video format
        cmd = [
            'ffmpeg', '-i', input_file,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error converting video format: {e}")
        return False