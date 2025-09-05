import logging
import av
from datetime import datetime

logger = logging.getLogger('ZenSort')


class FFmpegHandler:
    def __init__(self):
        self.available = self._check_availability()
        if self.available:
            logger.info("PyAV (FFmpeg) libraries available")
        else:
            logger.warning("PyAV (FFmpeg) libraries not available")
    
    def convert_heic_to_jpeg(self, heic_path, jpeg_path, quality=85):
        """Convert HEIC file to JPEG using PyAV."""
        if not self.available:
            return False
            
        try:
            with av.open(heic_path) as container:
                stream = container.streams.video[0]
                for frame in container.decode(stream):
                    # Convert to PIL Image and save as JPEG
                    pil_image = frame.to_image()
                    pil_image.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                    break  # Only need first frame
            return True
            
        except Exception as e:
            logger.error(f"HEIC to JPEG conversion failed for {heic_path}: {e}")
            return False
    
    def extract_video_metadata(self, video_path):
        """Extract video metadata using PyAV."""
        if not self.available:
            return {}
            
        try:
            with av.open(video_path) as container:
                metadata = {
                    'duration': None,
                    'width': None,
                    'height': None,
                    'codec': None,
                    'creation_time': None
                }
                
                # Get container duration
                if container.duration:
                    metadata['duration'] = float(container.duration) / av.time_base
                
                # Get creation time from container metadata
                if container.metadata:
                    for key in ['creation_time', 'date', 'DATE']:
                        if key in container.metadata:
                            metadata['creation_time'] = container.metadata[key]
                            break
                
                # Get video stream info
                video_stream = None
                for stream in container.streams:
                    if stream.type == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    metadata['width'] = video_stream.width
                    metadata['height'] = video_stream.height
                    metadata['codec'] = video_stream.codec.name
                    
                    # Get creation time from stream metadata
                    if not metadata['creation_time'] and video_stream.metadata:
                        for key in ['creation_time', 'date', 'DATE']:
                            if key in video_stream.metadata:
                                metadata['creation_time'] = video_stream.metadata[key]
                                break
                
                return metadata
                
        except Exception as e:
            logger.error(f"Video metadata extraction failed for {video_path}: {e}")
            return {}
    
    def _check_availability(self):
        """Check if PyAV is available and working."""
        try:
            # Try to create a simple container to test PyAV
            av.open
            return True
        except Exception:
            return False
    
    def is_available(self):
        """Check if PyAV is available."""
        return self.available