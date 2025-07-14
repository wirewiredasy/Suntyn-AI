import os
import subprocess
import tempfile
from werkzeug.utils import secure_filename

def get_video_info(input_path):
    """Get video information using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', input_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None

def trim_video(input_path, output_path, start_time, end_time):
    """Trim video to specified time range"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error trimming video: {e}")
        return False

def extract_audio(input_path, output_path, audio_format='mp3'):
    """Extract audio from video"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vn', '-acodec', 'libmp3lame' if audio_format == 'mp3' else 'copy',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False

def remove_audio(input_path, output_path):
    """Remove audio track from video"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-an', '-c:v', 'copy',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error removing audio: {e}")
        return False

def compress_video(input_path, output_path, quality='medium'):
    """Compress video file"""
    try:
        # Quality settings
        quality_settings = {
            'low': ['-crf', '35'],
            'medium': ['-crf', '28'],
            'high': ['-crf', '23']
        }
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium'
        ] + quality_settings.get(quality, quality_settings['medium']) + [
            '-c:a', 'aac', '-b:a', '128k',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error compressing video: {e}")
        return False

def convert_video(input_path, output_path, output_format='mp4'):
    """Convert video to different format"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error converting video: {e}")
        return False

def crop_video_vertical(input_path, output_path, aspect_ratio='9:16'):
    """Crop video for vertical format (shorts/stories)"""
    try:
        # Get video info to calculate crop dimensions
        info = get_video_info(input_path)
        if not info:
            return False
        
        video_stream = next(s for s in info['streams'] if s['codec_type'] == 'video')
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        
        # Calculate crop dimensions for 9:16 aspect ratio
        if aspect_ratio == '9:16':
            target_width = height * 9 // 16
            target_height = height
            crop_x = (width - target_width) // 2
            crop_y = 0
        else:
            target_width = width
            target_height = width * 16 // 9
            crop_x = 0
            crop_y = (height - target_height) // 2
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f'crop={target_width}:{target_height}:{crop_x}:{crop_y}',
            '-c:a', 'copy',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error cropping video: {e}")
        return False

def add_subtitles(input_path, subtitle_path, output_path):
    """Add subtitles to video"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f'subtitles={subtitle_path}',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error adding subtitles: {e}")
        return False

class VideoProcessor:
    @staticmethod
    def trim_video(file, start_time, end_time):
        """Trim video file"""
        # Note: This is a placeholder - you'll need moviepy or ffmpeg for actual video processing
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"trimmed_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)

        # Save the original file for now (placeholder)
        file.save(output_path)
        return output_path

    @staticmethod
    def extract_audio(file, format='mp3'):
        """Extract audio from video"""
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"audio_{name}.{format}"
        output_path = os.path.join('uploads', output_filename)

        # Placeholder - you'll need moviepy or ffmpeg
        with open(output_path, 'wb') as f:
            f.write(b'placeholder audio file')

        return output_path

    @staticmethod
    def compress_video(file, quality='medium'):
        """Compress video file"""
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"compressed_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)

        # Placeholder
        file.save(output_path)
        return output_path

    @staticmethod
    def convert_video(file, format='mp4'):
        """Convert video format"""
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"converted_{name}.{format}"
        output_path = os.path.join('uploads', output_filename)

        # Placeholder
        file.save(output_path)
        return output_path

    @staticmethod
    def crop_vertical(file, aspect_ratio='9:16'):
        """Crop video to vertical format"""
        os.makedirs('uploads', exist_ok=True)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"vertical_{name}{ext}"
        output_path = os.path.join('uploads', output_filename)

        # Placeholder
        file.save(output_path)
        return output_path