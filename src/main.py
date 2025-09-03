#!/usr/bin/env python3
"""
ZenSort - Unified CLI/GUI launcher
Launches GUI if no arguments, CLI if arguments provided
"""

import sys

def main():
    """Main entry point - decide between CLI and GUI based on arguments."""
    if len(sys.argv) > 1:
        # Arguments provided - run CLI
        try:
            from .cli import main as cli_main
        except ImportError:
            from cli import main as cli_main
        cli_main()
    else:
        # No arguments - run GUI
        try:
            from .gui import main as gui_main
        except ImportError:
            from gui import main as gui_main
        gui_main()

if __name__ == '__main__':
    main()