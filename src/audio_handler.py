import re
from pathlib import Path
from mutagen import File
import logging

logger = logging.getLogger('ZenSort')


class AudioHandler:
    def __init__(self, config):
        # Cache call recording rules with compiled patterns for performance
        call_rules = config.get('call_recording_rules', [
            {'pattern': r'call.*recording', 'extension': '3gp'},
            {'pattern': r'phone.*call', 'extension': 'amr'},
            {'pattern': r'voice.*call', 'extension': 'm4a'},
            {'pattern': r'recording.*\d{4}', 'extension': 'mp3'}
        ])
        self.call_rules = [(re.compile(rule['pattern'], re.IGNORECASE), rule['extension']) for rule in call_rules]
        
        # Cache voice recording rules with compiled patterns for performance
        voice_rules = config.get('voice_recording_rules', [
            {'pattern': r'voice', 'extension': 'wav'},
            {'pattern': r'recording', 'extension': 'm4a'},
            {'pattern': r'memo', 'extension': 'mp3'},
            {'pattern': r'note', 'extension': 'm4a'}
        ])
        self.voice_rules = [(re.compile(rule['pattern'], re.IGNORECASE), rule['extension']) for rule in voice_rules]
        
        # Cache voice message rules with compiled patterns for performance
        voice_msg_rules = config.get('voice_message_rules', [])
        self.voice_message_rules = [(re.compile(rule['pattern'], re.IGNORECASE), rule['extension']) for rule in voice_msg_rules]
        
        # Cache music extensions as set for O(1) lookup
        audio_config = config.get('audio_categories', {})
        self.music_extensions = set(f'.{ext}' for ext in audio_config.get('music', ['mp3', 'flac', 'm4a', 'aac', 'ogg']))
    
    def categorize_audio(self, file_path):
        """Categorize audio file with priority system."""
        path = Path(file_path)
        filename = path.name.lower()
        extension = path.suffix.lower().lstrip('.')
        
        # 1. Check for call recordings (pattern-extension pairs)
        for pattern, rule_ext in self.call_rules:
            if extension == rule_ext and pattern.search(filename):
                return 'call_recording'
        
        # 2. Check for voice messages (pattern-extension pairs)
        for pattern, rule_ext in self.voice_message_rules:
            if extension == rule_ext and pattern.search(filename):
                return 'voice_message'
        
        # 3. Check for voice recordings (pattern-extension pairs)
        for pattern, rule_ext in self.voice_rules:
            if extension == rule_ext and pattern.search(filename):
                return 'voice_recording'
        
        # 4. Check for songs (extensions only)
        if f'.{extension}' in self.music_extensions:
            return 'music'
        
        # 5. Default to other audio
        return 'other_audio'
    
    def extract_metadata(self, file_path):
        """Extract audio metadata using mutagen."""
        try:
            audio_file = File(file_path)
            if not audio_file:
                return {}
            
            metadata = {}
            
            # Common tags across formats
            tag_mapping = {
                'title': ['TIT2', 'TITLE', '\xa9nam'],
                'artist': ['TPE1', 'ARTIST', '\xa9ART'],
                'album': ['TALB', 'ALBUM', '\xa9alb'],
                'date': ['TDRC', 'DATE', '\xa9day'],
                'genre': ['TCON', 'GENRE', '\xa9gen']
            }
            
            for key, tags in tag_mapping.items():
                for tag in tags:
                    if tag in audio_file:
                        value = audio_file[tag]
                        metadata[key] = str(value[0]) if isinstance(value, list) else str(value)
                        break
            
            # Add duration if available
            if hasattr(audio_file, 'info') and audio_file.info:
                metadata['duration'] = getattr(audio_file.info, 'length', 0)
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting audio metadata from {file_path}: {e}")
            return {}