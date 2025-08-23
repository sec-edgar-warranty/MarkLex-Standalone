#!/usr/bin/env python3
"""
MarkLex Desktop - Marketing Lexicon Creation Tool
Main application entry point
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QIcon

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.main_window import MainWindow
from src.utils.app_dirs import AppDirs

def setup_app_directories():
    """Create necessary application directories"""
    app_dirs = AppDirs()
    os.makedirs(app_dirs.user_data_dir, exist_ok=True)
    os.makedirs(app_dirs.user_cache_dir, exist_ok=True)
    os.makedirs(app_dirs.embeddings_dir, exist_ok=True)

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MarkLex")
    app.setApplicationDisplayName("MarkLex - Marketing Lexicon Creation")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("MarkLex")
    app.setOrganizationDomain("marklex.app")
    
    # Setup application directories
    setup_app_directories()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()