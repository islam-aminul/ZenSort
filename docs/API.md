# ZenSort API Documentation

This document describes how to use ZenSort programmatically as a Python module.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.files_organizer import FilesOrganizer

# Basic usage
organizer = FilesOrganizer("/path/to/source", "/path/to/destination")
success = organizer.organize()
print(f"Organization {'completed' if success else 'failed'}")
```

## Core Classes

### FilesOrganizer

Main controller class for organizing multiple files.

```python
class FilesOrganizer:
    def __init__(self, source_dir, dest_dir, config_path=None)
    def organize(self, progress_callback=None)
    def pause()
    def resume() 
    def stop()
    def get_stats()
```

**Parameters:**
- `source_dir`: Path to source directory
- `dest_dir`: Path to destination directory  
- `config_path`: Optional custom config directory

**Methods:**

#### organize(progress_callback=None)
Start the organization process.

```python
def progress_callback(current, total, stats):
    percentage = (current / total) * 100
    print(f"Progress: {percentage:.1f}% - {stats}")

success = organizer.organize(progress_callback=progress_callback)
```

#### pause() / resume() / stop()
Control the organization process.

```python
organizer.pause()   # Pause processing
organizer.resume()  # Resume processing
organizer.stop()    # Stop processing
```

#### get_stats()
Get current processing statistics.

```python
stats = organizer.get_stats()
# Returns: {'processed': 150, 'skipped': 10, 'duplicates': 5, 'errors': 2, 'total': 167}
```

### FileOrganizer

Single file processor class.

```python
class FileOrganizer:
    def __init__(self, config, database, audio_handler, music_enhancer=None)
    def process_file(self, file_path, base_dir)
```

**Methods:**

#### process_file(file_path, base_dir)
Process a single file.

```python
result = processor.process_file("/path/to/file.jpg", "/path/to/destination")
# Returns: {'status': 'processed', 'type': 'image', 'destination': '/path/to/organized/file.jpg'}
```

**Return values:**
- `{'status': 'processed', 'type': 'image', 'destination': 'path'}`
- `{'status': 'skipped', 'reason': 'skip_pattern'}`
- `{'status': 'duplicate', 'original': 'path'}`
- `{'status': 'error', 'reason': 'error_message'}`

### ConfigManager

Configuration management class.

```python
class ConfigManager:
    def __init__(self, config_dir)
    def load_config()
    def save_config(config)
    def reset_to_defaults()
```

**Usage:**
```python
from src.config_manager import ConfigManager

config_manager = ConfigManager("/path/to/config")
config = config_manager.load_config()

# Modify config
config['image_export']['enabled'] = False

# Save changes
config_manager.save_config(config)
```

### Database Classes

#### FileHashDB

Database for duplicate detection.

```python
class FileHashDB:
    def __init__(self, db_path)
    def connect()
    def add_hash(file_path, file_hash, file_size)
    def check_duplicate(file_hash)
    def get_stats()
    def close()
```

**Usage:**
```python
from src.database import FileHashDB

db = FileHashDB("/path/to/database.db")
db.connect()

# Check for duplicate
duplicate_path = db.check_duplicate("sha256_hash")
if duplicate_path:
    print(f"Duplicate found: {duplicate_path}")

# Add new file
db.add_hash("/path/to/file.jpg", "sha256_hash", 1024000)

db.close()
```

### Organizer Classes

#### ImageOrganizer

Organizes image files.

```python
class ImageOrganizer:
    def __init__(self, config)
    def organize_image(self, file_path, base_dir)
```

#### VideoOrganizer

Organizes video files.

```python
class VideoOrganizer:
    def __init__(self, config)
    def organize_video(self, file_path, base_dir)
```

#### AudioOrganizer

Organizes audio files.

```python
class AudioOrganizer:
    def __init__(self, config, audio_handler, music_enhancer=None)
    def organize_audio(self, file_path, base_dir)
```

#### DocumentOrganizer

Organizes document files.

```python
class DocumentOrganizer:
    def __init__(self, config)
    def organize_document(self, file_path, base_dir)
```

### Handler Classes

#### ImageMetadata

Handles image metadata extraction.

```python
class ImageMetadata:
    def __init__(self, config=None)
    def process_image(self, image_path)
    def save_with_exif(self, image, output_path, exif_data=None, quality=85)
```

**Usage:**
```python
from src.image_metadata import ImageMetadata

handler = ImageMetadata(config)
metadata, img, exif = handler.process_image("/path/to/image.jpg")

print(f"Camera: {metadata['make']} {metadata['model']}")
print(f"Date: {metadata['datetime']}")
print(f"Edited: {metadata['is_edited']}")

img.close()  # Don't forget to close the image
```

#### AudioHandler

Handles audio file categorization.

```python
class AudioHandler:
    def __init__(self, config)
    def categorize_audio(self, file_path)
    def extract_metadata(self, file_path)
```

**Usage:**
```python
from src.audio_handler import AudioHandler

handler = AudioHandler(config)
category = handler.categorize_audio("/path/to/audio.mp3")
# Returns: 'music', 'call_recording', 'voice_recording', or 'other_audio'

metadata = handler.extract_metadata("/path/to/audio.mp3")
# Returns: {'title': 'Song Title', 'artist': 'Artist Name', ...}
```

## Advanced Usage Examples

### Custom Progress Tracking

```python
import time
from src.files_organizer import FilesOrganizer

class ProgressTracker:
    def __init__(self):
        self.start_time = time.time()
        self.last_update = 0
    
    def callback(self, current, total, stats):
        # Update every 10 files or at completion
        if current - self.last_update >= 10 or current == total:
            elapsed = time.time() - self.start_time
            rate = current / elapsed if elapsed > 0 else 0
            eta = (total - current) / rate if rate > 0 else 0
            
            print(f"Progress: {current}/{total} ({current/total*100:.1f}%)")
            print(f"Rate: {rate:.1f} files/sec, ETA: {eta:.0f}s")
            print(f"Stats: {stats}")
            
            self.last_update = current

tracker = ProgressTracker()
organizer = FilesOrganizer("/source", "/dest")
organizer.organize(progress_callback=tracker.callback)
```

### Custom Configuration

```python
from src.files_organizer import FilesOrganizer
from src.config_manager import ConfigManager

# Load and modify config
config_manager = ConfigManager("/path/to/config")
config = config_manager.load_config()

# Customize settings
config['image_export']['max_width'] = 4096
config['image_export']['quality'] = 95
config['musicbrainz']['enabled'] = False

# Save custom config
config_manager.save_config(config)

# Use with organizer
organizer = FilesOrganizer("/source", "/dest", "/path/to/config")
organizer.organize()
```

### Batch Processing

```python
import os
from pathlib import Path
from src.files_organizer import FilesOrganizer

def organize_multiple_directories(source_dirs, base_dest):
    """Organize multiple source directories."""
    for i, source_dir in enumerate(source_dirs):
        dest_dir = Path(base_dest) / f"organized_{i+1}"
        
        print(f"Processing {source_dir} -> {dest_dir}")
        
        organizer = FilesOrganizer(source_dir, dest_dir)
        success = organizer.organize()
        
        stats = organizer.get_stats()
        print(f"Completed: {stats}")
        
        if not success:
            print(f"Failed to process {source_dir}")

# Usage
sources = ["/photos/2020", "/photos/2021", "/photos/2022"]
organize_multiple_directories(sources, "/organized_photos")
```

### Error Handling

```python
from src.files_organizer import FilesOrganizer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_organize(source, dest):
    """Organize with comprehensive error handling."""
    try:
        organizer = FilesOrganizer(source, dest)
        
        # Validate paths
        if not Path(source).exists():
            raise ValueError(f"Source directory does not exist: {source}")
        
        # Start organization
        success = organizer.organize()
        
        # Check results
        stats = organizer.get_stats()
        if stats['errors'] > 0:
            logger.warning(f"Completed with {stats['errors']} errors")
        
        return success, stats
        
    except Exception as e:
        logger.error(f"Organization failed: {e}")
        return False, {}

# Usage
success, stats = safe_organize("/source", "/dest")
if success:
    print(f"Success! Processed {stats['processed']} files")
else:
    print("Organization failed")
```

### Integration with Other Tools

```python
import json
from pathlib import Path
from src.files_organizer import FilesOrganizer

def organize_with_report(source, dest, report_file):
    """Organize files and generate detailed report."""
    
    def progress_callback(current, total, stats):
        # Save progress to file
        progress_data = {
            'current': current,
            'total': total,
            'stats': stats,
            'percentage': (current / total) * 100
        }
        
        with open(f"{report_file}.progress", 'w') as f:
            json.dump(progress_data, f, indent=2)
    
    organizer = FilesOrganizer(source, dest)
    success = organizer.organize(progress_callback=progress_callback)
    
    # Generate final report
    final_stats = organizer.get_stats()
    report = {
        'source': str(source),
        'destination': str(dest),
        'success': success,
        'statistics': final_stats,
        'organization_structure': {
            'images': 'Images/Originals/Make - Model/Year/',
            'videos': 'Videos/Year/',
            'audio': 'Audios/Songs/',
            'documents': 'Documents/Type/'
        }
    }
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return success, final_stats

# Usage
success, stats = organize_with_report("/photos", "/organized", "report.json")
```

## Error Handling

All methods may raise exceptions. Common exceptions:

- `FileNotFoundError`: Source file/directory not found
- `PermissionError`: Insufficient permissions
- `OSError`: System-level errors
- `ValueError`: Invalid parameters
- `json.JSONDecodeError`: Invalid configuration

Always use try-catch blocks for robust error handling:

```python
try:
    organizer = FilesOrganizer(source, dest)
    success = organizer.organize()
except FileNotFoundError as e:
    print(f"File not found: {e}")
except PermissionError as e:
    print(f"Permission denied: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Thread Safety

ZenSort is not thread-safe. Use separate instances for concurrent processing:

```python
import threading
from src.files_organizer import FilesOrganizer

def organize_directory(source, dest):
    organizer = FilesOrganizer(source, dest)
    return organizer.organize()

# Process multiple directories concurrently
threads = []
for source, dest in directory_pairs:
    thread = threading.Thread(target=organize_directory, args=(source, dest))
    threads.append(thread)
    thread.start()

# Wait for completion
for thread in threads:
    thread.join()
```