import os
import time
from pathlib import Path

def format_time(seconds):
    """Format seconds into human readable time string."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
try:
    from .logger import ZenSortLogger
except ImportError:
    from logger import ZenSortLogger
try:
    from .database import FileHashDB
except ImportError:
    try:
        from database import FileHashDB
    except ImportError:
        from database_sqlite import FileHashDB
try:
    from .config_manager import ConfigManager
    from .audio_handler import AudioHandler
    from .music_metadata import MusicMetadataEnhancer
    from .file_organizer import FileOrganizer as SingleFileOrganizer
except ImportError:
    from config_manager import ConfigManager
    from audio_handler import AudioHandler
    from music_metadata import MusicMetadataEnhancer
    from file_organizer import FileOrganizer as SingleFileOrganizer


class FilesOrganizer:
    def __init__(self, source_dir, dest_dir, config_path=None):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.paused = False
        self.stopped = False
        
        # Load configuration
        config_dir = config_path or self.dest_dir
        self.config_manager = ConfigManager(config_dir)
        self.config = self.config_manager.load_config()
        
        # Initialize components
        self.database = None
        self.processor = None
        self.progress_callback = None
        self.logger = None
        
        # Statistics
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'duplicates': 0,
            'errors': 0,
            'total': 0
        }
    
    def organize(self, progress_callback=None):
        """Main organization method with pause/resume support."""
        self.progress_callback = progress_callback
        print("DEBUG: Starting organize method")
        
        try:
            # Initialize logger
            try:
                self.logger = ZenSortLogger(self.dest_dir)
                self.logger.info(f"Starting ZenSort organization")
                self.logger.info(f"Source: {self.source_dir}")
                self.logger.info(f"Destination: {self.dest_dir}")
            except Exception as e:
                print(f"Logger initialization failed: {e}")
                print(f"Starting ZenSort organization")
                print(f"Source: {self.source_dir}")
                print(f"Destination: {self.dest_dir}")
            
            print("DEBUG: About to validate paths")
            # Validate paths
            if not self._validate_paths():
                print("DEBUG: Path validation failed")
                return False
            print("DEBUG: Path validation passed")
            
            print("DEBUG: About to initialize database")
            # Initialize database
            if not self._init_database():
                print("DEBUG: Database initialization failed")
                return False
            print("DEBUG: Database initialized")
            
            print("DEBUG: About to initialize processor")
            # Initialize processor
            self._init_processor()
            print("DEBUG: Processor initialized")
            
            print("DEBUG: About to process files")
            # Scan and process files
            result = self._process_files()
            print(f"DEBUG: Process files returned: {result}")
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Organization error: {e}")
            else:
                print(f"Organization error: {e}")
            return False
        finally:
            if self.database:
                self.database.close()
    
    def pause(self):
        """Pause the organization process."""
        self.paused = True
    
    def resume(self):
        """Resume the organization process."""
        self.paused = False
    
    def stop(self):
        """Stop the organization process."""
        self.stopped = True
    
    def _validate_paths(self):
        """Validate source and destination paths."""
        if not self.source_dir.exists():
            msg = f"Source directory does not exist: {self.source_dir}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(f"ERROR: {msg}")
            return False
        
        # Check if destination is inside source
        try:
            self.dest_dir.resolve().relative_to(self.source_dir.resolve())
            msg = "Destination directory cannot be inside source directory"
            if self.logger:
                self.logger.error(msg)
            else:
                print(f"ERROR: {msg}")
            return False
        except ValueError:
            # This is good - dest is not inside source
            pass
        
        # Create destination directory
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        msg = "Path validation completed successfully"
        if self.logger:
            self.logger.info(msg)
        else:
            print(f"INFO: {msg}")
        return True
    
    def _init_database(self):
        """Initialize database connection."""
        db_path = self.dest_dir / 'zensort.db'
        self.database = FileHashDB(db_path)
        success = self.database.connect()
        if success:
            msg = "Database initialized successfully"
            if self.logger:
                self.logger.info(msg)
            else:
                print(f"INFO: {msg}")
        else:
            msg = "Failed to initialize database"
            if self.logger:
                self.logger.error(msg)
            else:
                print(f"ERROR: {msg}")
        return success
    
    def _init_processor(self):
        """Initialize file processor with all components."""
        msg = "Initializing file processor..."
        if self.logger:
            self.logger.info(msg)
        else:
            print(f"INFO: {msg}")
        audio_handler = AudioHandler(self.config)
        music_enhancer = MusicMetadataEnhancer(self.config) if self.config.get('musicbrainz', {}).get('enabled') else None
        
        self.processor = SingleFileOrganizer(
            self.config,
            self.database,
            audio_handler,
            music_enhancer
        )
        msg = "File processor initialized successfully"
        if self.logger:
            self.logger.info(msg)
        else:
            print(f"INFO: {msg}")
    
    def _process_files(self):
        """Recursively process all files in source directory."""
        # Count total files first
        msg = "Scanning source directory for files..."
        if self.logger:
            self.logger.info(msg)
        else:
            print(f"INFO: {msg}")
        all_files = list(self._scan_files())
        self.stats['total'] = len(all_files)
        msg = f"Found {self.stats['total']} files to process"
        if self.logger:
            self.logger.info(msg)
        else:
            print(f"INFO: {msg}")
        
        # Initialize timing
        start_time = time.time()
        
        if self.progress_callback:
            self.progress_callback(0, self.stats['total'], self.stats, "0s", "0s")
        
        # Process each file
        for i, file_path in enumerate(all_files):
            if self.stopped:
                break
            
            # Handle pause
            while self.paused and not self.stopped:
                time.sleep(0.1)
            
            if self.stopped:
                break
            
            # Process file
            result = self.processor.process_file(file_path, self.dest_dir)
            
            # Calculate timing info
            elapsed_time = time.time() - start_time
            if i > 0:
                avg_time_per_file = elapsed_time / (i + 1)
                remaining_files = self.stats['total'] - (i + 1)
                eta_seconds = avg_time_per_file * remaining_files
            else:
                eta_seconds = 0
            
            # Log file processing with aligned format
            action = result['status'].upper().ljust(10)
            file_path_str = str(file_path)
            
            # Format timing for human readability
            elapsed_str = format_time(elapsed_time)
            eta_str = format_time(eta_seconds)
            
            if result['status'] == 'processed':
                if self.logger:
                    self.logger.info(f"Processed: {file_path} -> {result.get('destination', 'unknown')}")
                if self.progress_callback:
                    self.progress_callback(i + 1, self.stats['total'], self.stats, elapsed_str, eta_str, f"{action} {file_path_str}")
            elif result['status'] == 'skipped':
                if self.logger:
                    self.logger.info(f"Skipped: {file_path} ({result.get('reason', 'unknown')})")
                if self.progress_callback:
                    self.progress_callback(i + 1, self.stats['total'], self.stats, elapsed_str, eta_str, f"{action} {file_path_str}")
            elif result['status'] == 'duplicate':
                if self.logger:
                    self.logger.warning(f"Duplicate: {file_path} (original: {result.get('original', 'unknown')})")
                if self.progress_callback:
                    self.progress_callback(i + 1, self.stats['total'], self.stats, elapsed_str, eta_str, f"{action} {file_path_str}")
            else:
                if self.logger:
                    self.logger.error(f"Error processing {file_path}: {result.get('reason', 'unknown')}")
                if self.progress_callback:
                    self.progress_callback(i + 1, self.stats['total'], self.stats, elapsed_str, eta_str, f"{action} {file_path_str}")
            
            # Update statistics
            if result['status'] == 'processed':
                self.stats['processed'] += 1
            elif result['status'] == 'skipped':
                self.stats['skipped'] += 1
            elif result['status'] == 'duplicate':
                self.stats['duplicates'] += 1
            else:
                self.stats['errors'] += 1
            
            # Progress callback (already called above with file info)
        
        # Log final results
        if self.logger:
            if self.stopped:
                self.logger.warning("Organization stopped by user")
            else:
                self.logger.info("Organization completed successfully")
            
            self.logger.info(f"Final statistics: {self.stats}")
        
        return not self.stopped
    
    def _scan_files(self):
        """Recursively scan source directory for files."""
        for root, dirs, files in os.walk(self.source_dir):
            # Skip directories that should be ignored
            dirs[:] = [d for d in dirs if not self.processor.skipper.should_skip_directory(Path(root) / d)]
            
            for file in files:
                # Sanitize filename to remove null characters
                clean_file = file.replace('\x00', '')
                if clean_file != file:
                    if self.logger:
                        self.logger.warning(f"Sanitized filename with null characters: {repr(file)}")
                
                file_path = Path(root) / clean_file
                if not self.processor.skipper.should_skip_file(file_path):
                    yield file_path
    
    def get_stats(self):
        """Get current processing statistics."""
        return self.stats.copy()