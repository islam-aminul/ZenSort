from PIL import Image
from datetime import datetime


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
            img = Image.open(image_path)
            exif = img.getexif()
            
            # Extract metadata
            metadata = {
                'datetime': None,
                'make': None,
                'model': None,
                'software': '',
                'is_edited': False,
                'year': '0000'
            }
            
            if exif:
                # Get datetime with fallback
                dt_str = exif.get(36867) or exif.get(306)  # DateTimeOriginal or DateTime
                if dt_str:
                    dt = self._parse_datetime(str(dt_str))
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
                
                # Fix DateTime if empty but DateTimeOriginal exists
                if exif.get(36867) and not exif.get(306):
                    exif[306] = exif[36867]
            
            return metadata, img, exif
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return {}, None, None
    
    def _parse_datetime(self, dt_str):
        """Parse datetime string with multiple format support."""
        for fmt in self.datetime_formats:
            try:
                dt = datetime.strptime(dt_str, fmt)
                # Add system timezone if missing
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
                return dt
            except ValueError:
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
            print(f"Error saving image: {e}")
            return False