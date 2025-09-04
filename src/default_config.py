DEFAULT_CONFIG = {
    # Directory Settings
    "directories": {
        "images": "Images",
        "videos": "Videos",
        "audios": "Audios",
        "documents": "Documents",
        "archives": "Archives",
        "executables": "Executables",
        "others": "Others"
    },
    
    # Subdirectory Names
    "subdirectories": {
        "images": {
            "originals": "Originals",
            "collections": "Collections",
            "screenshots": "Screenshots",
            "edited": "Edited",
            "hidden": "Hidden",
            "exports": "Exports",
            "social_media": "Social Media"
        },
        "videos": {
            "motion_photos": "Motion Photos",
            "short_videos": "Short Videos"
        },
        "audios": {
            "call_recordings": "Call Recordings",
            "voice_recordings": "Voice Recordings",
            "songs": "Songs",
            "other": "Other",
            "voice_messages": "Voice Messages"
        },
        "documents": {
            "other": "Other"
        }
    },
    
    # Image Export Settings
    "image_export": {
        "enabled": True,
        "formats": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "heic", "heif"],
        "quality": 85,
        "resize": False,
        "max_width": 3840,
        "max_height": 2160
    },
    
    # Screenshot Detection Patterns
    "screenshot_patterns": [
        "screenshot",
        "screen.*shot",
        "capture"
    ],
    
    # Image Editing Software Detection
    "editing_software": [
        "photoshop",
        "lightroom",
        "gimp",
        "canva",
        "pixelmator"
    ],
    
    # EXIF DateTime Formats
    "datetime_formats": [
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S"
    ],
    
    # Video Processing Settings
    "video_thresholds": {
        "min_duration": 1,
        "max_duration": 7200,
        "min_file_size_mb": 1,
        "max_file_size_mb": 5000,
        "supported_formats": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"],
        "short_video_threshold": 60
    },
    
    # Motion Photo Detection Patterns
    "motion_photo_patterns": [
        r"IMG_\d+\.MOV",
        r"MVIMG_\d+",
        r".*_MOTION",
        r"LIVE_\d+"
    ],
    
    # Audio Categories
    "audio_categories": {
        "music": ["mp3", "flac", "m4a", "aac", "ogg"],
        "podcasts": ["mp3", "m4a", "ogg"],
        "audiobooks": ["mp3", "m4a", "m4b"]
    },
    
    # Call Recording Detection Rules (pattern-extension pairs)
    "call_recording_rules": [
        {"pattern": r"call.*recording", "extension": "3gp"},
        {"pattern": r"phone.*call", "extension": "amr"},
        {"pattern": r"voice.*call", "extension": "m4a"},
        {"pattern": r"recording.*\d{4}", "extension": "mp3"}
    ],
    
    # Voice Recording Detection Rules (pattern-extension pairs)
    "voice_recording_rules": [
        {"pattern": r"voice", "extension": "wav"},
        {"pattern": r"recording", "extension": "m4a"},
        {"pattern": r"memo", "extension": "mp3"},
        {"pattern": r"note", "extension": "m4a"}
    ],
    
    # Social Media Image Detection Rules (pattern-extension pairs)
    "social_media_image_rules": [
        {"pattern": r"IMG-\d{8}-WA\d+", "extension": "jpg"},
        {"pattern": r"IMG-\d{8}-WA\d+", "extension": "jpeg"},
        {"pattern": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "extension": "jpg"}
    ],
    
    # Voice Message Detection Rules (pattern-extension pairs)
    "voice_message_rules": [
        {"pattern": r"AUD-\d{8}-WA\d+", "extension": "opus"},
        {"pattern": r"PTT-\d{8}-WA\d+", "extension": "opus"},
        {"pattern": r"AUD-\d{8}-WA\d+", "extension": "aac"},
        {"pattern": r"PTT-\d{8}-WA\d+", "extension": "aac"}
    ],
    
    # Document Categories
    "document_categories": {
        "word": ["doc", "docx", "rtf", "odt"],
        "pdf": ["pdf"],
        "excel": ["xls", "xlsx", "csv", "ods"],
        "powerpoint": ["ppt", "pptx", "odp"],
        "text": ["txt", "md", "log"],
        "ebook": ["epub", "mobi", "azw", "azw3"]
    },
    
    # File Skip Patterns
    "skip_patterns": {
        "hidden_files": True,
        "system_files": [".DS_Store", "Thumbs.db", "desktop.ini"],
        "temp_extensions": [".tmp", ".temp", ".cache", ".log"],
        "ignore_directories": [".git", "__pycache__", "node_modules", ".vscode"],
        "min_file_size_bytes": 0,
        "max_file_size_gb": 50
    },
    
    # MusicBrainz Settings
    "musicbrainz": {
        "enabled": True,
        "user_agent": "ZenSort/1.0",
        "version": "1.0",
        "rate_limit": 1.0,
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay_base": 2,
        "use_acoustid": True,
        "acoustid_api_key": "CyFvbCxTVb",
        "lookup_meta": "recordings+releasegroups+compress",
        "date_format": "year_only",
        "id3_encoding": 3,
        "fetch_cover_art": True,
        "preferred_release_types": ["album", "single", "ep"]
    },
    
    # General Processing Settings
    "processing": {
        "batch_size": 100,
        "parallel_processing": True,
        "max_workers": 4,
        "create_backups": False,
        "dry_run": False,
        "verbose_logging": True
    }
}