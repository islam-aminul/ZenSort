import hashlib
import os
from pathlib import Path
import logging

logger = logging.getLogger('ZenSort')
try:
    from .file_detector import FileDetector
    from .file_skipper import FileSkipper
    from .image_organizer import ImageOrganizer
    from .video_organizer import VideoOrganizer
    from .audio_organizer import AudioOrganizer
    from .document_organizer import DocumentOrganizer
    from .file_copy import FileCopy
except ImportError:
    from file_detector import FileDetector
    from file_skipper import FileSkipper
    from image_organizer import ImageOrganizer
    from video_organizer import VideoOrganizer
    from audio_organizer import AudioOrganizer
    from document_organizer import DocumentOrganizer
    from file_copy import FileCopy


class FileOrganizer:
    def __init__(self, config, database, audio_handler, music_enhancer=None):
        self.database = database
        self.detector = FileDetector()
        self.skipper = FileSkipper(config)
        
        # Cache directory names
        directories = config.get('directories', {})
        self.archives_dir = directories.get('archives', 'Archives')
        self.executables_dir = directories.get('executables', 'Executables')
        self.others_dir = directories.get('others', 'Others')
        
        # Initialize organizers
        self.image_organizer = ImageOrganizer(config)
        self.video_organizer = VideoOrganizer(config)
        self.audio_organizer = AudioOrganizer(config, audio_handler, music_enhancer)
        self.document_organizer = DocumentOrganizer(config)
    
    def process_file(self, file_path, base_dir):
        """Process a single file through the complete workflow."""
        try:
            # Get file info
            file_size = os.path.getsize(file_path)
            
            # Check if file should be skipped
            if self.skipper.should_skip_file(file_path, file_size):
                return {'status': 'skipped', 'reason': 'skip_pattern'}
            
            # Generate file hash
            file_hash = self._generate_hash(file_path)
            if not file_hash:
                return {'status': 'error', 'reason': 'hash_generation_failed'}
            
            # Check for duplicates
            duplicate_path = self.database.check_duplicate(file_hash)
            if duplicate_path:
                return {'status': 'duplicate', 'original': duplicate_path}
            
            # Detect file type
            file_type = self.detector.detect_file_type(file_path)
            
            # Route to appropriate organizer
            result_path = self._route_file(file_path, file_type, base_dir)
            
            if result_path:
                # Add to database
                self.database.add_hash(result_path, file_hash, file_size)
                return {'status': 'processed', 'type': file_type, 'destination': result_path}
            else:
                return {'status': 'error', 'reason': 'organization_failed'}
                
        except Exception as e:
            return {'status': 'error', 'reason': str(e)}
    
    def _generate_hash(self, file_path):
        """Generate SHA-256 hash of file."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error generating hash for {file_path}: {e}")
            return None
    
    def _route_file(self, file_path, file_type, base_dir):
        """Route file to appropriate organizer."""
        if file_type == 'image':
            return self.image_organizer.organize_image(file_path, base_dir)
        elif file_type == 'video':
            return self.video_organizer.organize_video(file_path, base_dir)
        elif file_type == 'audio':
            return self.audio_organizer.organize_audio(file_path, base_dir)
        elif file_type == 'document':
            return self.document_organizer.organize_document(file_path, base_dir)
        elif file_type in ['archive', 'executable']:
            # Handle other types with simple directory structure
            return self._organize_other(file_path, file_type, base_dir)
        else:
            return self._organize_other(file_path, 'unknown', base_dir)
    
    def _organize_other(self, file_path, file_type, base_dir):
        """Organize other file types into simple directories."""
        
        type_map = {
            'archive': self.archives_dir,
            'executable': self.executables_dir,
            'unknown': self.others_dir
        }
        
        dest_dir = Path(base_dir) / type_map.get(file_type, self.others_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        
        return FileCopy.copy_with_conflict_resolution(file_path, dest_path)