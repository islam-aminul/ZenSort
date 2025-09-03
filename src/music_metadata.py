import time
try:
    import acoustid
    import musicbrainzngs
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON
    from mutagen import File
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Optional music dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False


class MusicMetadataEnhancer:
    def __init__(self, config):
        self.config = config.get('musicbrainz', {})
        self.enabled = self.config.get('enabled', False) and DEPENDENCIES_AVAILABLE
        
        if self.enabled and DEPENDENCIES_AVAILABLE:
            # Configure MusicBrainz
            musicbrainzngs.set_useragent(
                self.config.get('user_agent'),
                self.config.get('version', '1.0')
            )
            self.rate_limit = self.config.get('rate_limit')
            self.timeout = self.config.get('timeout')
            self.retry_attempts = self.config.get('retry_attempts')
            self.use_acoustid = self.config.get('use_acoustid')
            self.acoustid_api_key = self.config.get('acoustid_api_key', '')
            self.last_request_time = 0
    
    def enhance_metadata(self, file_path):
        """Enhance music metadata using MusicBrainz."""
        if not self.enabled:
            return False
        
        try:
            # Rate limiting
            self._rate_limit()
            
            # Generate acoustic fingerprint
            if self.use_acoustid:
                fingerprint_data = self._get_fingerprint(file_path)
                if fingerprint_data:
                    metadata = self._search_by_fingerprint(fingerprint_data)
                    if metadata:
                        return self._update_tags(file_path, metadata)
            
            return False
            
        except Exception as e:
            print(f"Error enhancing metadata for {file_path}: {e}")
            return False
    
    def _get_fingerprint(self, file_path):
        """Generate acoustic fingerprint using AcoustID."""
        try:
            duration, fingerprint = acoustid.fingerprint_file(str(file_path))
            return {'duration': duration, 'fingerprint': fingerprint}
        except Exception as e:
            print(f"Error generating fingerprint: {e}")
            return None
    
    def _search_by_fingerprint(self, fingerprint_data):
        """Search MusicBrainz using acoustic fingerprint."""
        for attempt in range(self.retry_attempts):
            try:
                results = acoustid.lookup(
                    api_key=self.acoustid_api_key,
                    fingerprint=fingerprint_data['fingerprint'],
                    duration=fingerprint_data['duration'],
                    meta=self.config.get('lookup_meta', 'recordings+releasegroups+compress')
                )
                
                if results.get('results'):
                    recording = results['results'][0].get('recordings', [{}])[0]
                    if recording:
                        return self._extract_metadata(recording)
                
                break
                
            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.config.get('retry_delay_base', 2) ** attempt)
                else:
                    print(f"MusicBrainz search failed: {e}")
        
        return None
    
    def _extract_metadata(self, recording):
        """Extract metadata from MusicBrainz recording."""
        metadata = {}
        
        if 'title' in recording:
            metadata['title'] = recording['title']
        
        if 'artist-credit' in recording:
            artists = [artist['artist']['name'] for artist in recording['artist-credit'] if 'artist' in artist]
            if artists:
                metadata['artist'] = ', '.join(artists)
        
        if 'releases' in recording:
            release = recording['releases'][0]
            if 'title' in release:
                metadata['album'] = release['title']
            if 'date' in release:
                date_format = self.config.get('date_format', 'year_only')
                if date_format == 'year_only':
                    metadata['date'] = release['date'][:4]
                else:
                    metadata['date'] = release['date']
        
        return metadata
    
    def _update_tags(self, file_path, metadata):
        """Update ID3v2 tags with enhanced metadata."""
        try:
            audio_file = File(file_path)
            if not audio_file:
                return False
            
            # Add ID3 tags if not present
            if not hasattr(audio_file, 'tags') or audio_file.tags is None:
                audio_file.add_tags()
            
            # Update tags
            tag_mapping = {
                'title': TIT2,
                'artist': TPE1,
                'album': TALB,
                'date': TDRC,
                'genre': TCON
            }
            
            encoding = self.config.get('id3_encoding', 3)
            for key, tag_class in tag_mapping.items():
                if key in metadata:
                    audio_file.tags[tag_class.__name__] = tag_class(encoding=encoding, text=metadata[key])
            
            audio_file.save()
            return True
            
        except Exception as e:
            print(f"Error updating tags: {e}")
            return False
    
    def _rate_limit(self):
        """Implement rate limiting for API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        self.last_request_time = time.time()