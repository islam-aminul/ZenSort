# ZenSort - Intelligent File Organizer

ZenSort automatically organizes your files into a clean, structured directory system based on file types, metadata, and intelligent detection patterns.

## Features

- **Smart Image Organization** - Sorts by camera make/model, date, and detects screenshots/edited photos
- **Video Categorization** - Separates regular videos, motion photos, and short clips
- **Audio Classification** - Organizes music, call recordings, voice memos with MusicBrainz enhancement
- **Document Sorting** - Groups by type (Word, PDF, Excel, etc.)
- **Duplicate Detection** - Uses SHA-256 hashing to prevent duplicates
- **EXIF Preservation** - Maintains metadata in image exports
- **Configurable Rules** - Customize all organization patterns and settings
- **GUI & CLI Interfaces** - Choose your preferred interaction method

## Quick Start

### Download Pre-built Executables
1. Download the latest release for your platform
2. Run `ZenSort` (GUI) or `ZenSort-CLI` (command line)
3. Select source and destination folders
4. Click Start!

### From Source
```bash
# Clone repository
git clone https://github.com/yourusername/ZenSort.git
cd ZenSort

# Setup environment
./scripts/setup_env.sh  # Linux/macOS
# or
scripts\setup_env.bat   # Windows

# Run GUI
python src/gui.py

# Run CLI
python src/cli.py /path/to/source /path/to/destination
```

## Organization Structure

ZenSort creates the following directory structure:

```
Destination/
├── Images/
│   ├── Originals/
│   │   ├── Camera Make - Camera Model/
│   │   │   └── Year/
│   │   └── Collections/          # Images without EXIF
│   ├── Exports/
│   │   └── Year/                 # Resized exports with metadata naming
│   ├── Screenshots/
│   ├── Edited/                   # Photos edited with software
│   └── Hidden/                   # Hidden image files
├── Videos/
│   ├── Year/                     # Regular videos
│   ├── Motion Photos/
│   │   └── Year/                 # iPhone Live Photos, Samsung Motion
│   └── Short Videos/
│       └── Year/                 # Videos under threshold duration
├── Audios/
│   ├── Songs/                    # Music files (enhanced with MusicBrainz)
│   ├── Call Recordings/          # Phone call recordings
│   ├── Voice Recordings/         # Voice memos, notes
│   └── Other/                    # Other audio files
├── Documents/
│   ├── Word/                     # .doc, .docx, .rtf, .odt
│   ├── PDF/                      # .pdf files
│   ├── Excel/                    # .xls, .xlsx, .csv, .ods
│   ├── Powerpoint/               # .ppt, .pptx, .odp
│   ├── Text/                     # .txt, .md, .log
│   ├── Ebook/                    # .epub, .mobi, .azw
│   └── Other/                    # Unrecognized documents
├── Archives/                     # .zip, .rar, .7z, etc.
├── Executables/                  # .exe, .msi, .deb, .rpm, etc.
└── Others/                       # Unrecognized file types
```

## Organization Rules

### Images
- **Originals**: Images with EXIF data → `Images/Originals/Make - Model/Year/`
- **Collections**: Images without EXIF → `Images/Originals/Collections/`
- **Screenshots**: Filename contains "screenshot", "capture" → `Images/Screenshots/`
- **Edited**: Software field contains editing programs → `Images/Edited/`
- **Hidden**: Filenames starting with "." → `Images/Hidden/`
- **Exports**: Resized copies (max 3840x2160) → `Images/Exports/Year/YYYY-MM-DD - HH-MM-SS -- Make - Model -- filename.jpg`

### Videos
1. **Motion Photos**: Patterns like `IMG_*.MOV`, `MVIMG_*` → `Videos/Motion Photos/Year/`
2. **Short Videos**: Duration ≤ threshold → `Videos/Short Videos/Year/`
3. **Regular Videos**: All others → `Videos/Year/`

### Audio
1. **Call Recordings**: Pattern + extension pairs (e.g., "call recording" + .3gp) → `Audios/Call Recordings/`
2. **Voice Recordings**: Pattern + extension pairs (e.g., "voice memo" + .wav) → `Audios/Voice Recordings/`
3. **Music**: Music extensions (.mp3, .flac, etc.) → `Audios/Songs/`
4. **Other Audio**: Everything else → `Audios/Other/`

### Documents
Sorted by extension into appropriate folders (Word, PDF, Excel, PowerPoint, Text, Ebook, Other).

## Configuration

ZenSort creates a `zensort_config.json` file in the destination directory. Key settings:

### Image Export Settings
```json
{
  "image_export": {
    "enabled": true,
    "max_width": 3840,
    "max_height": 2160,
    "quality": 85
  }
}
```

### Screenshot Detection
```json
{
  "screenshot_patterns": [
    "screenshot",
    "screen.*shot", 
    "capture"
  ]
}
```

### Video Settings
```json
{
  "video_thresholds": {
    "short_video_threshold": 60
  },
  "motion_photo_patterns": [
    "IMG_\\d+\\.MOV",
    "MVIMG_\\d+",
    ".*_MOTION"
  ]
}
```

### Audio Classification
```json
{
  "call_recording_rules": [
    {"pattern": "call.*recording", "extension": "3gp"},
    {"pattern": "phone.*call", "extension": "amr"}
  ],
  "voice_recording_rules": [
    {"pattern": "voice", "extension": "wav"},
    {"pattern": "memo", "extension": "mp3"}
  ]
}
```

### MusicBrainz Enhancement
```json
{
  "musicbrainz": {
    "enabled": true,
    "rate_limit": 1.0,
    "use_acoustid": true,
    "acoustid_api_key": ""
  }
}
```

### Skip Patterns
```json
{
  "skip_patterns": {
    "hidden_files": true,
    "system_files": [".DS_Store", "Thumbs.db"],
    "temp_extensions": [".tmp", ".cache"],
    "ignore_directories": [".git", "__pycache__"],
    "max_file_size_gb": 50
  }
}
```

## Usage Examples

### GUI Interface
1. Launch `ZenSort`
2. Browse and select source directory
3. Browse and select destination directory
4. Click "Settings" to customize organization rules
5. Click "Start" to begin organization
6. Use "Pause/Resume" and "Stop" as needed
7. Monitor progress and logs in real-time

### Command Line Interface
```bash
# Basic usage
ZenSort-CLI /path/to/photos /path/to/organized

# With custom config directory
ZenSort-CLI /path/to/photos /path/to/organized --config /path/to/config

# Quiet mode (no progress output)
ZenSort-CLI /path/to/photos /path/to/organized --quiet
```

### Python Module
```python
from src.files_organizer import FilesOrganizer

def progress_callback(current, total, stats):
    print(f"Progress: {current}/{total} ({current/total*100:.1f}%)")

organizer = FilesOrganizer("/path/to/source", "/path/to/dest")
success = organizer.organize(progress_callback=progress_callback)
print(f"Organization {'completed' if success else 'failed'}")
```

## Building from Source

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/yourusername/ZenSort.git
cd ZenSort

# Setup virtual environment
./scripts/setup_env.sh  # Linux/macOS
scripts\setup_env.bat   # Windows

# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat # Windows
```

### Build Executables
```bash
# Cross-platform build
python scripts/build_all.py

# Platform-specific
./scripts/build_windows.bat  # Windows
./scripts/build_macos.sh     # macOS  
./scripts/build_linux.sh     # Linux

# Clean build artifacts
python scripts/clean.py
```

## Troubleshooting

### Common Issues

**"Source directory does not exist"**
- Verify the source path is correct and accessible
- Check file permissions

**"Destination cannot be inside source directory"**
- Choose a destination folder outside the source directory
- Use a different drive or parent directory

**"Error extracting EXIF"**
- Image file may be corrupted
- Unsupported image format
- File permissions issue

**"MusicBrainz search failed"**
- Check internet connection
- Verify AcoustID API key if using custom key
- Rate limiting may be active

**High memory usage**
- Reduce batch size in processing settings
- Close other applications
- Process smaller directories at a time

**Slow processing**
- Disable MusicBrainz enhancement for faster processing
- Disable image exports if not needed
- Use SSD storage for better performance

### Performance Tips

1. **Use SSD storage** for source and destination
2. **Disable unnecessary features** (MusicBrainz, image exports)
3. **Process in smaller batches** for large collections
4. **Close other applications** to free up memory
5. **Use wired internet** for MusicBrainz lookups

### Log Analysis

The GUI shows detailed logs with color coding:
- **Blue**: Folder processing
- **Green**: Success messages
- **Red**: Errors
- **Orange**: Warnings
- **Gray**: Information

Check logs for specific error messages and file paths that failed processing.

### Getting Help

1. Check this documentation
2. Review configuration file syntax
3. Enable verbose logging for detailed output
4. Create an issue on GitHub with:
   - Operating system and version
   - Python version
   - Error messages and logs
   - Steps to reproduce

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### v1.0.0
- Initial release
- Complete file organization system
- GUI and CLI interfaces
- Cross-platform support
- Comprehensive configuration options