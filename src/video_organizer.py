import re
from pathlib import Path
from datetime import datetime
import os
try:
    from .file_copy import FileCopy
    from .ffmpeg_handler import FFmpegHandler
except ImportError:
    from file_copy import FileCopy
    from ffmpeg_handler import FFmpegHandler


class VideoOrganizer:
    def __init__(self, config):
        # Cache directory names
        directories = config.get('directories', {})
        self.videos_dir = directories.get('videos', 'Videos')
        
        # Initialize FFmpeg handler for metadata extraction
        self.ffmpeg_handler = FFmpegHandler()
        
        # Cache subdirectory names
        subdirs = config.get('subdirectories', {}).get('videos', {})
        self.motion_photos_dir = subdirs.get('motion_photos', 'Motion Photos')
        self.short_videos_dir = subdirs.get('short_videos', 'Short Videos')
        
        # Cache video threshold to avoid repeated dict lookups
        video_config = config.get('video_thresholds', {})
        self.short_video_threshold = video_config.get('short_video_threshold', 60)
        
        # Cache compiled motion photo patterns
        motion_patterns = config.get('motion_photo_patterns', [
            r'IMG_\d+\.MOV',  # iPhone Live Photos
            r'MVIMG_\d+',     # Samsung Motion Photos
            r'.*_MOTION',     # Generic motion pattern
            r'LIVE_\d+'       # Live photo pattern
        ])
        self.motion_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in motion_patterns]
    
    def organize_video(self, file_path, base_dir):
        """Organize video into appropriate directory structure."""
        path = Path(file_path)
        filename = path.name
        
        # Get creation year
        year = self._get_video_year(file_path)
        
        # Check motion photo patterns first
        if self._is_motion_photo(filename):
            return self._move_to_motion_photos(file_path, base_dir, year)
        
        # Check video duration for short videos
        duration = self._get_video_duration(file_path)
        if duration and duration <= self.short_video_threshold:
            return self._move_to_short_videos(file_path, base_dir, year)
        
        # Regular videos
        return self._move_to_regular_videos(file_path, base_dir, year)
    
    def _is_motion_photo(self, filename):
        """Check if video is a motion photo."""
        return any(pattern.search(filename) for pattern in self.motion_patterns)
    
    def _get_video_year(self, file_path):
        """Get video creation year from metadata or file stats."""
        try:
            # Try to get from file modification time as fallback
            stat = os.stat(file_path)
            return datetime.fromtimestamp(stat.st_mtime).strftime('%Y')
        except Exception:
            return '0000'
    
    def _get_video_duration(self, file_path):
        """Get video duration in seconds."""
        try:
            # Basic duration check using file size as approximation
            # In a real implementation, you'd use ffprobe or similar
            stat = os.stat(file_path)
            # Rough estimate: assume 1MB per minute for standard video
            estimated_duration = stat.st_size / (1024 * 1024) * 60
            return estimated_duration
        except Exception:
            return None
    
    def _move_to_motion_photos(self, file_path, base_dir, year):
        """Move to Motion Photos directory."""
        dest_dir = Path(base_dir) / self.videos_dir / self.motion_photos_dir / year
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract metadata and generate filename
        metadata = self.ffmpeg_handler.extract_video_metadata(file_path)
        new_filename = self._generate_video_filename(file_path, metadata)
        dest_path = dest_dir / new_filename
        return self._copy_file(file_path, dest_path)
    
    def _move_to_short_videos(self, file_path, base_dir, year):
        """Move to Short Videos directory."""
        dest_dir = Path(base_dir) / self.videos_dir / self.short_videos_dir / year
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract metadata and generate filename
        metadata = self.ffmpeg_handler.extract_video_metadata(file_path)
        new_filename = self._generate_video_filename(file_path, metadata)
        dest_path = dest_dir / new_filename
        return self._copy_file(file_path, dest_path)
    
    def _move_to_regular_videos(self, file_path, base_dir, year):
        """Move to regular Videos directory."""
        dest_dir = Path(base_dir) / self.videos_dir / year
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract metadata and generate filename
        metadata = self.ffmpeg_handler.extract_video_metadata(file_path)
        new_filename = self._generate_video_filename(file_path, metadata)
        dest_path = dest_dir / new_filename
        return self._copy_file(file_path, dest_path)
    
    def _generate_video_filename(self, file_path, metadata):
        """Generate video filename with datetime, make, model format."""
        original_name = Path(file_path).stem
        extension = Path(file_path).suffix
        
        filename_parts = []
        
        # Add datetime if available
        creation_time = metadata.get('creation_time')
        if creation_time:
            try:
                # Parse creation time (usually ISO format)
                if 'T' in creation_time:
                    dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                else:
                    dt = datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
                
                date_time = dt.strftime('%Y-%m-%d %H-%M-%S')
                filename_parts.append(date_time)
            except (ValueError, TypeError):
                pass
        
        # Add make and model if available (from EXIF or metadata)
        make = metadata.get('make')
        model = metadata.get('model')
        if make and model:
            filename_parts.append(f'{make} - {model}')
        
        # Add original filename
        filename_parts.append(original_name)
        
        # Join parts with separator
        if len(filename_parts) > 1:
            new_filename = ' -- '.join(filename_parts) + extension
        else:
            new_filename = original_name + extension
        
        return new_filename
    
    def _copy_file(self, src, dest):
        """Copy file to destination with conflict resolution."""
        return FileCopy.copy_with_conflict_resolution(src, dest)