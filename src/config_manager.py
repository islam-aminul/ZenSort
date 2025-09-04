import json
import os
from pathlib import Path
try:
    from .default_config import DEFAULT_CONFIG
except ImportError:
    from default_config import DEFAULT_CONFIG


class ConfigManager:
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "zensort_config.json"
        
    def load_config(self):
        """Load config from file, merging with defaults if needed."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                return self._merge_configs(DEFAULT_CONFIG, user_config)
            else:
                # Save default config to file first
                default_config = DEFAULT_CONFIG.copy()
                self.save_config(default_config)
                return default_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}. Creating default config.")
            default_config = DEFAULT_CONFIG.copy()
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config):
        """Save config to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_configs(self, default, user):
        """Recursively merge user config with defaults."""
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def reset_to_defaults(self):
        """Reset config to defaults and save."""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return self.save_config(DEFAULT_CONFIG)
        except OSError as e:
            print(f"Error resetting config: {e}")
            return False