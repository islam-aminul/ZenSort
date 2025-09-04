import re
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger('ZenSort')
try:
    from .image_metadata import ImageMetadata
    from .file_copy import FileCopy
except ImportError:
    from image_metadata import ImageMetadata
    from file_copy import FileCopy


class ImageOrganizer:
    def __init__(self, config):
        self.metadata_handler = ImageMetadata(config)
        
        # Cache directory names
        directories = config.get('directories', {})
        self.images_dir = directories.get('images', 'Images')
        
        # Cache subdirectory names
        subdirs = config.get('subdirectories', {}).get('images', {})
        self.originals_dir = subdirs.get('originals', 'Originals')
        self.collections_dir = subdirs.get('collections', 'Collections')
        self.screenshots_dir = subdirs.get('screenshots', 'Screenshots')
        self.edited_dir = subdirs.get('edited', 'Edited')
        self.hidden_dir = subdirs.get('hidden', 'Hidden')
        self.exports_dir = subdirs.get('exports', 'Exports')
        self.social_media_dir = subdirs.get('social_media', 'Social Media')
        
        # Cache compiled social media patterns
        social_rules = config.get('social_media_image_rules', [])
        self.social_media_rules = [(re.compile(rule['pattern'], re.IGNORECASE), rule['extension']) for rule in social_rules]
        
        # Cache export settings to avoid repeated dict lookups
        image_config = config.get('image_export', {})
        self.export_enabled = image_config.get('enabled', True)
        self.max_width = image_config.get('max_width', 3840)
        self.max_height = image_config.get('max_height', 2160)
        self.quality = image_config.get('quality', 85)
        
        # Cache compiled screenshot patterns
        screenshot_patterns = config.get('screenshot_patterns', ['screenshot', 'screen.*shot', 'capture'])
        self.screenshot_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in screenshot_patterns]
    
    def organize_image(self, file_path, base_dir):
        """Organize image into appropriate directory structure."""
        path = Path(file_path)
        filename = path.name
        
        # Check if hidden
        if filename.startswith('.'):
            return self._move_to_hidden(file_path, base_dir)
        
        # Check if screenshot
        if self._is_screenshot(filename):
            return self._move_to_screenshots(file_path, base_dir)
        
        # Check if social media image
        if self._is_social_media_image(filename):
            return self._move_to_social_media(file_path, base_dir)
        
        # Process image and get metadata
        metadata, img, exif = self.metadata_handler.process_image(file_path)
        
        try:
            # Check if edited photo
            if metadata.get('is_edited'):
                return self._move_to_edited(file_path, base_dir)
            
            # Route based on EXIF data
            if metadata.get('datetime') and (metadata.get('make') or metadata.get('model')):
                return self._move_to_originals(file_path, base_dir, metadata, img, exif)
            else:
                return self._move_to_collections(file_path, base_dir, img, exif)
        
        finally:
            if img:
                img.close()
    
    def _is_screenshot(self, filename):
        """Check if image is a screenshot."""
        return any(pattern.search(filename) for pattern in self.screenshot_patterns)
    
    def _is_social_media_image(self, filename):
        """Check if image is from social media."""
        extension = Path(filename).suffix.lower().lstrip('.')
        for pattern, rule_ext in self.social_media_rules:
            if rule_ext == extension and pattern.search(filename):
                return True
        return False
    
    def _move_to_originals(self, file_path, base_dir, metadata, img=None, exif=None):
        """Move to Originals with camera/year structure."""
        make = metadata.get('make')
        model = metadata.get('model')
        year = metadata.get('year', '0000')
        
        # Build path based on available metadata
        path_parts = ['Images', 'Originals']
        
        if make and model:
            path_parts.append(f'{make} - {model}')
        elif make:
            path_parts.append(make)
        elif model:
            path_parts.append(model)
        else:
            path_parts.append('Generic')
        
        path_parts.append(year)
        
        dest_dir = Path(base_dir) / self.images_dir / self.originals_dir
        for part in path_parts[2:]:
            dest_dir = dest_dir / part
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        
        result = FileCopy.copy_with_conflict_resolution(file_path, dest_path)
        
        # Create export for originals only
        if result and self.export_enabled and img and exif is not None:
            self._create_export(file_path, base_dir, metadata, img, exif)
        
        return result
    
    def _move_to_collections(self, file_path, base_dir, img=None, exif=None):
        """Move to Collections directory."""
        dest_dir = Path(base_dir) / self.images_dir / self.collections_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        
        result = FileCopy.copy_with_conflict_resolution(file_path, dest_path)
        
        # Create export for collections only if metadata is available
        if result and self.export_enabled and img and exif is not None:
            metadata = {'year': None, 'make': None, 'model': None, 'datetime': None}
            self._create_export(file_path, base_dir, metadata, img, exif)
        
        return result
    
    def _move_to_screenshots(self, file_path, base_dir):
        """Move to Screenshots directory."""
        dest_dir = Path(base_dir) / self.images_dir / self.screenshots_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        return FileCopy.copy_with_conflict_resolution(file_path, dest_path)
    
    def _move_to_edited(self, file_path, base_dir):
        """Move to Edited directory."""
        dest_dir = Path(base_dir) / self.images_dir / self.edited_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        return FileCopy.copy_with_conflict_resolution(file_path, dest_path)
    
    def _move_to_hidden(self, file_path, base_dir):
        """Move to Hidden directory."""
        dest_dir = Path(base_dir) / self.images_dir / self.hidden_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        return FileCopy.copy_with_conflict_resolution(file_path, dest_path)
    
    def _move_to_social_media(self, file_path, base_dir):
        """Move to Social Media directory."""
        dest_dir = Path(base_dir) / self.images_dir / self.social_media_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / Path(file_path).name
        return FileCopy.copy_with_conflict_resolution(file_path, dest_path)
    
    def _create_export(self, file_path, base_dir, metadata, img, exif):
        """Create resized export with specific naming."""
        try:
            # Generate export filename
            dt = metadata.get('datetime')
            make = metadata.get('make')
            model = metadata.get('model')
            original_name = Path(file_path).stem
            
            # Build filename parts
            filename_parts = []
            
            if dt:
                year = dt.strftime('%Y')
                date_time = dt.strftime('%Y-%m-%d - %H-%M-%S')
                filename_parts.append(date_time)
            else:
                year = 'NoDate'
            
            if make and model:
                filename_parts.append(f'{make} - {model}')
            
            filename_parts.append(original_name)
            
            export_filename = ' -- '.join(filename_parts) + '.jpg'
            export_dir = Path(base_dir) / self.images_dir / self.exports_dir / year
            export_dir.mkdir(parents=True, exist_ok=True)
            export_path = export_dir / export_filename
            
            # Create export image
            export_img = img.copy()
            
            # Resize if needed (preserve aspect ratio)
            if export_img.width > self.max_width or export_img.height > self.max_height:
                export_img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)
            
            # Save with EXIF preservation
            success = self.metadata_handler.save_with_exif(export_img, export_path, exif, self.quality)
            export_img.close()
            
            return str(export_path) if success else None
            
        except Exception as e:
            logger.error(f"Error creating export: {e}")
            return None