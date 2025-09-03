from pathlib import Path
try:
    from .file_copy import FileCopy
except ImportError:
    from file_copy import FileCopy


class DocumentOrganizer:
    def __init__(self, config):
        # Cache directory names
        directories = config.get('directories', {})
        self.documents_dir = directories.get('documents', 'Documents')
        
        # Cache subdirectory names
        subdirs = config.get('subdirectories', {}).get('documents', {})
        self.other_dir = subdirs.get('other', 'Other')
        
        # Cache document categories to avoid repeated dict lookups
        self.document_categories = config.get('document_categories', {
            'word': ['doc', 'docx', 'rtf', 'odt'],
            'pdf': ['pdf'],
            'excel': ['xls', 'xlsx', 'csv', 'ods'],
            'powerpoint': ['ppt', 'pptx', 'odp'],
            'text': ['txt', 'md', 'log'],
            'ebook': ['epub', 'mobi', 'azw', 'azw3']
        })
    
    def organize_document(self, file_path, base_dir):
        """Organize document by extension into appropriate subdirectory."""
        path = Path(file_path)
        extension = path.suffix.lower().lstrip('.')
        
        # Find category for extension
        category = self._get_document_category(extension)
        
        # Create destination directory
        if category:
            dest_dir = Path(base_dir) / self.documents_dir / category.title()
        else:
            dest_dir = Path(base_dir) / self.documents_dir / self.other_dir
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / path.name
        
        return self._copy_file(file_path, dest_path)
    
    def _get_document_category(self, extension):
        """Get document category for given extension."""
        for category, extensions in self.document_categories.items():
            if extension in extensions:
                return category
        return None
    
    def _copy_file(self, src, dest):
        """Copy file to destination with conflict resolution."""
        return FileCopy.copy_with_conflict_resolution(src, dest)