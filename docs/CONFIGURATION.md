# ZenSort Configuration Guide

This guide covers all configuration options available in ZenSort.

## Configuration File Location

ZenSort creates a `zensort_config.json` file in your destination directory. You can also specify a custom config directory using the `--config` parameter.

## Complete Configuration Reference

### Image Processing

```json
{
  "image_export": {
    "enabled": true,
    "max_width": 3840,
    "max_height": 2160,
    "quality": 85,
    "formats": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
  },
  "screenshot_patterns": [
    "screenshot",
    "screen.*shot",
    "capture",
    "snap"
  ],
  "editing_software": [
    "photoshop",
    "adobe",
    "lightroom", 
    "gimp",
    "paint.net",
    "canva",
    "pixlr",
    "windows photo",
    "picasa"
  ],
  "datetime_formats": [
    "%Y:%m:%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S"
  ]
}
```

**Options:**
- `enabled`: Enable/disable image exports
- `max_width/max_height`: Maximum export dimensions (preserves aspect ratio)
- `quality`: JPEG quality (1-100)
- `formats`: Supported image formats
- `screenshot_patterns`: Regex patterns for screenshot detection
- `editing_software`: Software names that indicate edited photos
- `datetime_formats`: EXIF datetime parsing formats

### Video Processing

```json
{
  "video_thresholds": {
    "min_duration": 1,
    "max_duration": 7200,
    "min_file_size_mb": 1,
    "max_file_size_mb": 5000,
    "short_video_threshold": 60,
    "supported_formats": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"]
  },
  "motion_photo_patterns": [
    "IMG_\\d+\\.MOV",
    "MVIMG_\\d+",
    ".*_MOTION",
    "LIVE_\\d+"
  ]
}
```

**Options:**
- `short_video_threshold`: Duration in seconds to classify as short video
- `motion_photo_patterns`: Regex patterns for motion photo detection
- `supported_formats`: Video file extensions to process

### Audio Classification

```json
{
  "audio_categories": {
    "music": ["mp3", "flac", "m4a", "aac", "ogg"],
    "call_recordings": ["3gp", "amr", "m4a"],
    "voice_recordings": ["wav", "m4a", "mp3"],
    "podcasts": ["mp3", "m4a", "ogg"],
    "audiobooks": ["mp3", "m4a", "m4b"]
  },
  "call_recording_rules": [
    {"pattern": "call.*recording", "extension": "3gp"},
    {"pattern": "phone.*call", "extension": "amr"},
    {"pattern": "voice.*call", "extension": "m4a"},
    {"pattern": "recording.*\\d{4}", "extension": "mp3"}
  ],
  "voice_recording_rules": [
    {"pattern": "voice", "extension": "wav"},
    {"pattern": "recording", "extension": "m4a"},
    {"pattern": "memo", "extension": "mp3"},
    {"pattern": "note", "extension": "m4a"}
  ]
}
```

**Options:**
- `audio_categories`: File extensions for each audio type
- `call_recording_rules`: Pattern-extension pairs for call detection
- `voice_recording_rules`: Pattern-extension pairs for voice memo detection

### Document Organization

```json
{
  "document_categories": {
    "word": ["doc", "docx", "rtf", "odt"],
    "pdf": ["pdf"],
    "excel": ["xls", "xlsx", "csv", "ods"],
    "powerpoint": ["ppt", "pptx", "odp"],
    "text": ["txt", "md", "log"],
    "ebook": ["epub", "mobi", "azw", "azw3"]
  }
}
```

**Options:**
- Each category maps to file extensions that belong in that folder

### MusicBrainz Integration

```json
{
  "musicbrainz": {
    "enabled": true,
    "user_agent": "ZenSort/1.0",
    "version": "1.0",
    "rate_limit": 1.0,
    "timeout": 30,
    "retry_attempts": 3,
    "retry_delay_base": 2,
    "use_acoustid": true,
    "acoustid_api_key": "",
    "lookup_meta": "recordings+releasegroups+compress",
    "date_format": "year_only",
    "id3_encoding": 3,
    "fetch_cover_art": true,
    "preferred_release_types": ["album", "single", "ep"]
  }
}
```

**Options:**
- `enabled`: Enable/disable MusicBrainz metadata enhancement
- `rate_limit`: Seconds between API requests
- `acoustid_api_key`: Your AcoustID API key (optional)
- `date_format`: "year_only" or "full_date"
- `id3_encoding`: ID3 tag encoding (3 = UTF-8)

### File Skip Patterns

```json
{
  "skip_patterns": {
    "hidden_files": true,
    "system_files": [".DS_Store", "Thumbs.db", "desktop.ini"],
    "temp_extensions": [".tmp", ".temp", ".cache", ".log"],
    "ignore_directories": [".git", "__pycache__", "node_modules", ".vscode"],
    "min_file_size_bytes": 0,
    "max_file_size_gb": 50
  }
}
```

**Options:**
- `hidden_files`: Skip files starting with "."
- `system_files`: Specific filenames to skip
- `temp_extensions`: File extensions to skip
- `ignore_directories`: Directory names to skip
- `min_file_size_bytes`: Skip files smaller than this
- `max_file_size_gb`: Skip files larger than this

### Processing Settings

```json
{
  "processing": {
    "batch_size": 100,
    "parallel_processing": true,
    "max_workers": 4,
    "create_backups": false,
    "dry_run": false,
    "verbose_logging": true
  }
}
```

**Options:**
- `batch_size`: Number of files to process in each batch
- `parallel_processing`: Enable multi-threading (future feature)
- `max_workers`: Number of worker threads
- `create_backups`: Create backup copies before moving
- `dry_run`: Show what would be done without actually moving files
- `verbose_logging`: Enable detailed logging

## Configuration Examples

### Minimal Configuration
```json
{
  "image_export": {
    "enabled": false
  },
  "musicbrainz": {
    "enabled": false
  }
}
```

### Photography Workflow
```json
{
  "image_export": {
    "enabled": true,
    "max_width": 4096,
    "max_height": 4096,
    "quality": 95
  },
  "screenshot_patterns": [
    "screenshot",
    "screen.*capture",
    "snap.*shot"
  ]
}
```

### Audio-Focused Setup
```json
{
  "musicbrainz": {
    "enabled": true,
    "rate_limit": 0.5,
    "acoustid_api_key": "your-api-key-here"
  },
  "call_recording_rules": [
    {"pattern": "call.*\\d{4}", "extension": "m4a"},
    {"pattern": "recording.*call", "extension": "3gp"}
  ]
}
```

### Performance Optimized
```json
{
  "image_export": {
    "enabled": false
  },
  "musicbrainz": {
    "enabled": false
  },
  "skip_patterns": {
    "max_file_size_gb": 10
  },
  "processing": {
    "batch_size": 50
  }
}
```

## Advanced Patterns

### Regex Patterns
ZenSort uses Python regex patterns. Common examples:

- `.*` - Match any characters
- `\\d+` - Match one or more digits
- `.*recording.*` - Match anything containing "recording"
- `^IMG_\\d+$` - Match exactly "IMG_" followed by digits

### Custom Audio Rules
```json
{
  "call_recording_rules": [
    {"pattern": "whatsapp.*audio", "extension": "opus"},
    {"pattern": "telegram.*voice", "extension": "ogg"},
    {"pattern": "zoom.*recording", "extension": "m4a"}
  ]
}
```

### Custom Screenshot Patterns
```json
{
  "screenshot_patterns": [
    "screenshot.*\\d{4}",
    "capture.*screen",
    "snip.*tool",
    "print.*screen"
  ]
}
```

## Configuration Validation

ZenSort validates configuration on startup. Common errors:

- **Invalid JSON syntax**: Check brackets, commas, quotes
- **Invalid regex patterns**: Test patterns with online regex tools
- **Invalid file extensions**: Don't include dots in extension lists
- **Invalid numeric values**: Use numbers for sizes, thresholds, etc.

## Resetting Configuration

To reset to defaults:
1. Delete the `zensort_config.json` file
2. Restart ZenSort
3. New default configuration will be created

Or use the GUI Settings window and click "Reset to Defaults" (if implemented).

## Environment Variables

You can override some settings with environment variables:

- `ZENSORT_CONFIG_DIR`: Custom configuration directory
- `ZENSORT_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MUSICBRAINZ_API_KEY`: MusicBrainz API key

## Configuration Tips

1. **Start simple**: Begin with default settings and customize gradually
2. **Test patterns**: Use small test directories to verify custom patterns
3. **Backup configs**: Save working configurations before making changes
4. **Monitor logs**: Check logs to see how files are being categorized
5. **Performance tuning**: Disable features you don't need for faster processing