import mimetypes
from pathlib import Path


class FileDetector:
    def __init__(self):
        self.extensions = {
            'image': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico', '.raw', '.heic', '.heif'},
            'video': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'},
            'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus', '.m4b'},
            'document': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'},
            'archive': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', '.tar.bz2'},
            'executable': {'.exe', '.msi', '.deb', '.rpm', '.dmg', '.app', '.apk', '.jar'}
        }
    
    def detect_file_type(self, file_path):
        """Detect file type based on extension and MIME type."""
        path = Path(file_path)
        
        if self.is_hidden(path):
            return 'hidden'
        
        # Check by extension first
        ext = path.suffix.lower()
        for category, extensions in self.extensions.items():
            if ext in extensions:
                return category
        
        # Fallback to MIME type
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type:
            main_type = mime_type.split('/')[0]
            if main_type in ['image', 'video', 'audio']:
                return main_type
            elif main_type == 'application':
                if 'pdf' in mime_type or 'document' in mime_type or 'text' in mime_type:
                    return 'document'
                elif 'zip' in mime_type or 'compressed' in mime_type:
                    return 'archive'
                elif 'executable' in mime_type:
                    return 'executable'
        
        return 'unknown'
    
    def is_hidden(self, path):
        """Check if file is hidden."""
        return path.name.startswith('.') or path.name.startswith('~')