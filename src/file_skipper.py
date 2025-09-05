import re
from pathlib import Path


class FileSkipper:
    def __init__(self, config):
        # Cache all skip patterns to avoid repeated dict lookups
        skip_config = config.get('skip_patterns', {})
        
        # Pre-compile patterns for speed
        self.skip_hidden = skip_config.get('hidden_files', True)
        self.system_files = set(skip_config.get('system_files', []))
        self.temp_extensions = set(skip_config.get('temp_extensions', []))
        self.ignore_dirs = set(skip_config.get('ignore_directories', []))
        self.min_size = skip_config.get('min_file_size_bytes', 0)
        self.max_size = skip_config.get('max_file_size_gb', 50) * 1024 * 1024 * 1024
        
        # Thumbnail patterns
        self.thumb_pattern = re.compile(r'\.thumb\d*$', re.IGNORECASE)
        
        # Compile filename skip patterns
        filename_patterns = skip_config.get('skip_filename_patterns', [])
        self.filename_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in filename_patterns]
    
    def should_skip_file(self, file_path, file_size=None):
        """Check if file should be skipped. Returns True to skip."""
        path = Path(file_path)
        
        # Check filename patterns
        if self._skip_by_name(path.name):
            return True
        
        # Check extension patterns
        if self._skip_by_extension(path.suffix.lower()):
            return True
        
        # Check file size if provided
        if file_size is not None and self._skip_by_size(file_size):
            return True
        
        return False
    
    def should_skip_directory(self, dir_path):
        """Check if directory should be skipped."""
        dir_name = Path(dir_path).name
        return dir_name in self.ignore_dirs or (self.skip_hidden and dir_name.startswith('.'))
    
    def _skip_by_name(self, filename):
        """Check filename patterns."""
        if self.skip_hidden and filename.startswith('.'):
            return True
        if filename in self.system_files:
            return True
        if self.thumb_pattern.search(filename):
            return True
        if any(pattern.search(filename) for pattern in self.filename_patterns):
            return True
        return False
    
    def _skip_by_extension(self, extension):
        """Check extension patterns."""
        return extension in self.temp_extensions
    
    def _skip_by_size(self, file_size):
        """Check file size limits."""
        return file_size < self.min_size or file_size > self.max_size