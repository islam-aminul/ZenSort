import shutil
from pathlib import Path
import logging

logger = logging.getLogger('ZenSort')


class FileCopy:
    @staticmethod
    def copy_with_conflict_resolution(src, dest):
        """Copy file handling naming conflicts with -- n suffix."""
        try:
            src_path = Path(src)
            dest_path = Path(dest)
            
            # If destination doesn't exist, copy directly
            if not dest_path.exists():
                shutil.copy2(src_path, dest_path)
                return str(dest_path)
            
            # Handle naming conflict
            counter = 1
            stem = dest_path.stem
            suffix = dest_path.suffix
            parent = dest_path.parent
            
            while True:
                new_name = f"{stem} -- {counter}{suffix}"
                new_dest = parent / new_name
                
                if not new_dest.exists():
                    shutil.copy2(src_path, new_dest)
                    return str(new_dest)
                
                counter += 1
                
        except Exception as e:
            logger.error(f"Error copying file from {src_path} to {dest_path}: {e}")
            return None