from pathlib import Path
try:
    from .file_copy import FileCopy
except ImportError:
    from file_copy import FileCopy


class AudioOrganizer:
    def __init__(self, config, audio_handler, music_enhancer=None):
        self.audio_handler = audio_handler
        self.music_enhancer = music_enhancer
        
        # Cache directory names
        directories = config.get('directories', {})
        self.audios_dir = directories.get('audios', 'Audios')
        
        # Cache subdirectory names
        subdirs = config.get('subdirectories', {}).get('audios', {})
        self.call_recordings_dir = subdirs.get('call_recordings', 'Call Recordings')
        self.voice_recordings_dir = subdirs.get('voice_recordings', 'Voice Recordings')
        self.voice_messages_dir = subdirs.get('voice_messages', 'Voice Messages')
        self.songs_dir = subdirs.get('songs', 'Songs')
        self.other_dir = subdirs.get('other', 'Other')
        
        # Cache config values to avoid repeated dict lookups
        self.enhance_music = config.get('musicbrainz', {}).get('enabled', False)
    
    def organize_audio(self, file_path, base_dir):
        """Organize audio file following exact priority system."""
        # Get audio category from handler
        category = self.audio_handler.categorize_audio(file_path)
        
        # Route to appropriate directory based on category
        if category == 'call_recording':
            return self._move_to_call_recordings(file_path, base_dir)
        elif category == 'voice_message':
            return self._move_to_voice_messages(file_path, base_dir)
        elif category == 'voice_recording':
            return self._move_to_voice_recordings(file_path, base_dir)
        elif category == 'music':
            return self._move_to_songs(file_path, base_dir)
        else:
            return self._move_to_other_audio(file_path, base_dir)
    
    def _move_to_call_recordings(self, file_path, base_dir):
        """Move to Call Recordings directory."""
        dest_dir = Path(base_dir) / self.audios_dir / self.call_recordings_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / Path(file_path).name
        return self._copy_file(file_path, dest_path)
    
    def _move_to_voice_recordings(self, file_path, base_dir):
        """Move to Voice Recordings directory."""
        dest_dir = Path(base_dir) / self.audios_dir / self.voice_recordings_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / Path(file_path).name
        return self._copy_file(file_path, dest_path)
    
    def _move_to_songs(self, file_path, base_dir):
        """Move to Songs directory and enhance with MusicBrainz if enabled."""
        dest_dir = Path(base_dir) / self.audios_dir / self.songs_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / Path(file_path).name
        result = self._copy_file(file_path, dest_path)
        
        # Enhance metadata if enabled and successful copy
        if result and self.enhance_music and self.music_enhancer:
            self.music_enhancer.enhance_metadata(dest_path)
        
        return result
    
    def _move_to_voice_messages(self, file_path, base_dir):
        """Move to Voice Messages directory."""
        dest_dir = Path(base_dir) / self.audios_dir / self.voice_messages_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / Path(file_path).name
        return self._copy_file(file_path, dest_path)
    
    def _move_to_other_audio(self, file_path, base_dir):
        """Move to Other audio directory."""
        dest_dir = Path(base_dir) / self.audios_dir / self.other_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_dir / Path(file_path).name
        return self._copy_file(file_path, dest_path)
    
    def _copy_file(self, src, dest):
        """Copy file to destination with conflict resolution."""
        return FileCopy.copy_with_conflict_resolution(src, dest)