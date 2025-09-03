import argparse
import sys
from pathlib import Path
try:
    from .files_organizer import FilesOrganizer
except ImportError:
    from files_organizer import FilesOrganizer


def progress_callback(current, total, stats):
    """Display progress information."""
    percentage = (current / total * 100) if total > 0 else 0
    print(f"\rProgress: {current}/{total} ({percentage:.1f}%) | "
          f"Processed: {stats['processed']} | Skipped: {stats['skipped']} | "
          f"Duplicates: {stats['duplicates']} | Errors: {stats['errors']}", end='', flush=True)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='ZenSort - Organize your files automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('source', 
                       help='Source directory to organize')
    parser.add_argument('destination', 
                       help='Destination directory for organized files')
    parser.add_argument('--config', '-c',
                       help='Configuration directory (default: destination directory)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Show what would be done without actually moving files')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress output')
    
    args = parser.parse_args()
    
    # Validate paths
    source_path = Path(args.source)
    dest_path = Path(args.destination)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_path}' does not exist")
        sys.exit(1)
    
    if not source_path.is_dir():
        print(f"Error: Source '{source_path}' is not a directory")
        sys.exit(1)
    
    # Initialize organizer
    try:
        organizer = FilesOrganizer(
            source_dir=source_path,
            dest_dir=dest_path,
            config_path=args.config
        )
        
        print(f"Starting organization...")
        print(f"Source: {source_path}")
        print(f"Destination: {dest_path}")
        print("-" * 50)
        
        # Start organization with progress callback
        callback = None if args.quiet else progress_callback
        success = organizer.organize(progress_callback=callback)
        
        if not args.quiet:
            print()  # New line after progress
        
        # Show final statistics
        stats = organizer.get_stats()
        print(f"\nOrganization {'completed' if success else 'stopped'}!")
        print(f"Total files: {stats['total']}")
        print(f"Processed: {stats['processed']}")
        print(f"Skipped: {stats['skipped']}")
        print(f"Duplicates: {stats['duplicates']}")
        print(f"Errors: {stats['errors']}")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()