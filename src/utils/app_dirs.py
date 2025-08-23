"""
Application directory management for cross-platform compatibility
Handles data directories for Mac, Windows, and Linux
"""

import os
import sys
from pathlib import Path
from typing import Optional

class AppDirs:
    """Cross-platform application directory management"""
    
    def __init__(self, app_name: str = "MarkLex", app_author: str = "MarkLex"):
        self.app_name = app_name
        self.app_author = app_author
        
    @property
    def user_data_dir(self) -> str:
        """Get user data directory path"""
        if sys.platform == "darwin":  # macOS
            base = Path.home() / "Library" / "Application Support"
        elif sys.platform == "win32":  # Windows
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        else:  # Linux and others
            base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
            
        return str(base / self.app_name)
    
    @property
    def user_cache_dir(self) -> str:
        """Get user cache directory path"""
        if sys.platform == "darwin":  # macOS
            base = Path.home() / "Library" / "Caches"
        elif sys.platform == "win32":  # Windows
            base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        else:  # Linux and others
            base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
            
        return str(base / self.app_name)
    
    @property
    def embeddings_dir(self) -> str:
        """Get embeddings storage directory"""
        return str(Path(self.user_data_dir) / "embeddings")
    
    @property
    def lexicon_dir(self) -> str:
        """Get lexicon storage directory"""
        return str(Path(self.user_data_dir) / "lexicons")
    
    @property
    def temp_dir(self) -> str:
        """Get temporary directory for downloads"""
        return str(Path(self.user_cache_dir) / "temp")