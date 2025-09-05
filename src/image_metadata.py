from PIL import Image
from datetime import datetime
import logging

# HEIC files are handled without external libraries
logger = logging.getLogger('ZenSort')

# ExifRead fallback for when PIL fails
import exifread


class ImageMetadata:
    def __init__(self, config=None):
        self.datetime_formats = config.get('datetime_formats', ['%Y:%m:%d %H:%M:%S', '%Y-%m-%d %H:%M:%S']) if config else ['%Y:%m:%d %H:%M:%S', '%Y-%m-%d %H:%M:%S']
        self.editing_software = config.get('editing_software', [
            'photoshop', 'adobe', 'lightroom', 'gimp', 'paint.net', 'canva', 
            'pixlr', 'windows photo', 'picasa'
        ]) if config else ['photoshop', 'adobe', 'lightroom', 'gimp', 'paint.net', 'canva', 'pixlr', 'windows photo', 'picasa']
    
    def process_image(self, image_path):
        """Process image and return metadata with loaded image."""
        try:
            # Initialize metadata
            metadata = {
                'datetime': None,
                'make': None,
                'model': None,
                'software': '',
                'is_edited': False,
                'year': '0000'
            }
            
            # HEIC files cannot be opened by PIL without external libraries
            if str(image_path).lower().endswith(('.heic', '.heif')):
                heic_metadata = self._extract_metadata_with_exifread(image_path)
                if heic_metadata:
                    metadata.update(heic_metadata)
                return metadata, None, None
            
            img = Image.open(image_path)
            exif = img.getexif() or {}
            
            if exif and len(exif) > 0:
                # Get datetime with comprehensive fallback (DateTimeOriginal, DateTimeDigitized, DateTime)
                dt_str = exif.get(36867) or exif.get(36868) or exif.get(306)
                if dt_str:
                    dt = self._parse_datetime(str(dt_str).strip())
                    if dt:
                        metadata['datetime'] = dt
                        metadata['year'] = dt.strftime('%Y')
                
                # Get camera info
                if 271 in exif:  # Make
                    metadata['make'] = str(exif[271]).strip()
                if 272 in exif:  # Model
                    metadata['model'] = str(exif[272]).strip()
                if 305 in exif:  # Software
                    software = str(exif[305]).strip().lower()
                    metadata['software'] = software
                    metadata['is_edited'] = any(editor in software for editor in self.editing_software)
                
                # Normalize EXIF datetime tags for export consistency
                if metadata['datetime']:
                    standard_dt = metadata['datetime'].strftime('%Y:%m:%d %H:%M:%S')
                    exif[306] = standard_dt  # DateTime
                    exif[36867] = standard_dt  # DateTimeOriginal
                    exif[36868] = standard_dt  # DateTimeDigitized
            
            # ExifRead fallback if PIL failed to extract datetime
            if not metadata['datetime']:
                self._set_datetime_from_exifread(image_path, metadata)
            
            return metadata, img, exif
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return {}, None, None
    
    def _parse_datetime(self, dt_str):
        """Parse datetime string with multiple format support."""
        if not dt_str or dt_str.strip() == '':
            return None
            
        # Clean the datetime string
        dt_str = dt_str.strip()
        
        for fmt in self.datetime_formats:
            try:
                dt = datetime.strptime(dt_str, fmt)
                # Validate reasonable date range (1970-2040)
                if 1970 <= dt.year <= 2040:
                    return dt
            except (ValueError, TypeError):
                continue
        return None
    
    def save_with_exif(self, image, output_path, exif_data=None, quality=85):
        """Save image preserving EXIF data."""
        try:
            if exif_data:
                image.save(output_path, 'JPEG', exif=exif_data, quality=quality, optimize=True)
            else:
                image.save(output_path, 'JPEG', quality=quality, optimize=True)
            return True
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle RGBA/P mode conversion
            if "cannot write mode" in error_msg and ("rgba" in error_msg or "p" in error_msg):
                try:
                    logger.warning(f"Converting {image.mode} to RGB for {output_path}")
                    if image.mode in ('RGBA', 'P'):
                        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                        rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                        image = rgb_image
                    
                    if exif_data:
                        image.save(output_path, 'JPEG', exif=exif_data, quality=quality, optimize=True)
                    else:
                        image.save(output_path, 'JPEG', quality=quality, optimize=True)
                    return True
                except Exception as retry_e:
                    logger.error(f"Failed to convert image mode for {output_path}: {retry_e}")
            
            # Handle EXIF too long
            if "too long" in error_msg and exif_data:
                try:
                    logger.warning(f"EXIF data too long, saving without EXIF for {output_path}")
                    image.save(output_path, 'JPEG', quality=quality, optimize=True)
                    return True
                except Exception as retry_e:
                    logger.error(f"Failed to save without EXIF for {output_path}: {retry_e}")
            
            logger.error(f"Error saving image {output_path}: {e}")
            return False
    
    def _set_datetime_from_exifread(self, image_path, metadata):
        """Extract and set datetime using ExifRead."""
        dt_str = self._extract_datetime_with_exifread(image_path)
        if dt_str:
            dt = self._parse_datetime(dt_str)
            if dt:
                metadata['datetime'] = dt
                metadata['year'] = dt.strftime('%Y')
    
    def _extract_datetime_with_exifread(self, image_path):
        """Extract datetime using ExifRead as fallback."""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
                
                # Try DateTimeOriginal, DateTimeDigitized, DateTime
                for tag_name in ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime']:
                    if tag_name in tags:
                        return str(tags[tag_name]).strip()
                        
        except Exception as e:
            logger.error(f"ExifRead fallback failed for {image_path}: {e}")
        
        return None
    
    def _extract_metadata_with_exifread(self, image_path):
        """Extract full metadata using ExifRead for HEIC files."""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                
                metadata = {
                    'datetime': None,
                    'make': None,
                    'model': None,
                    'software': '',
                    'is_edited': False,
                    'year': '0000'
                }
                
                # Extract datetime
                for tag_name in ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime']:
                    if tag_name in tags:
                        dt = self._parse_datetime(str(tags[tag_name]).strip())
                        if dt:
                            metadata['datetime'] = dt
                            metadata['year'] = dt.strftime('%Y')
                            break
                
                # Extract Make/Model/Software
                if 'Image Make' in tags:
                    metadata['make'] = str(tags['Image Make']).strip()
                if 'Image Model' in tags:
                    metadata['model'] = str(tags['Image Model']).strip()
                if 'Image Software' in tags:
                    software = str(tags['Image Software']).strip().lower()
                    metadata['software'] = software
                    metadata['is_edited'] = any(editor in software for editor in self.editing_software)
                
                return metadata
                
        except Exception as e:
            logger.error(f"ExifRead metadata extraction failed for {image_path}: {e}")
            return None