"""
Embedding model manager for downloading and loading Word2Vec models
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Callable
import zipfile

import requests
from tqdm import tqdm
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from gensim.models import Word2Vec

from utils.app_dirs import AppDirs

class DownloadThread(QThread):
    """Thread for downloading embeddings from GitHub"""
    
    progress_updated = pyqtSignal(int)  # Progress percentage
    status_updated = pyqtSignal(str)    # Status message
    download_completed = pyqtSignal(bool)  # Success/failure
    
    def __init__(self, app_dirs: AppDirs, force: bool = False):
        super().__init__()
        self.app_dirs = app_dirs
        self.force = force
        self.repo_url = "https://github.com/sec-edgar-warranty/MarkLex"
        
    def run(self):
        """Run download in separate thread"""
        try:
            self.status_updated.emit("Starting download...")
            
            # Since files are stored in Git LFS, we need to download them directly from GitHub's raw API
            # The files in the zip archive are just LFS pointer files
            
            embeddings_dest = self.app_dirs.embeddings_dir
            os.makedirs(embeddings_dest, exist_ok=True)
            
            # Define files to download with their raw URLs
            embedding_files = [
                "embeddings_8",
                "embeddings_8.trainables.syn1neg.npy", 
                "embeddings_8.wv.vectors.npy",
                "embeddings_bi_grams"
            ]
            
            files_downloaded = 0
            total_files = len(embedding_files)
            
            for i, file_name in enumerate(embedding_files):
                try:
                    self.status_updated.emit(f"Downloading {file_name}... ({i+1}/{total_files})")
                    
                    # Use GitHub's raw content API
                    file_url = f"{self.repo_url}/raw/main/{file_name}"
                    dest_path = os.path.join(embeddings_dest, file_name)
                    
                    # Download the file
                    self._download_file_direct(file_url, dest_path)
                    
                    # Check if file was downloaded successfully
                    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:  # Should be much larger than 1KB
                        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
                        files_downloaded += 1
                        self.status_updated.emit(f"✅ Downloaded {file_name} ({size_mb:.1f} MB)")
                    else:
                        self.status_updated.emit(f"❌ Failed to download {file_name} - file too small or missing")
                        # Remove empty file if it exists
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                    
                    # Update progress
                    progress = int(((i + 1) / total_files) * 80)  # Use 80% for downloads
                    self.progress_updated.emit(progress)
                    
                except Exception as e:
                    self.status_updated.emit(f"❌ Error downloading {file_name}: {str(e)}")
            
            # Also download lexicon file
            try:
                self.status_updated.emit("Downloading lexicon file...")
                lexicon_url = f"{self.repo_url}/raw/main/Lexicon List.xlsx"
                lexicon_dest = os.path.join(self.app_dirs.user_data_dir, "Lexicon List.xlsx")
                
                self._download_file_direct(lexicon_url, lexicon_dest)
                
                if os.path.exists(lexicon_dest) and os.path.getsize(lexicon_dest) > 1000:
                    self.status_updated.emit("✅ Downloaded lexicon file")
                else:
                    self.status_updated.emit("⚠️ Lexicon file download failed, using default")
            except:
                self.status_updated.emit("⚠️ Lexicon file download failed, using default")
            
            self.progress_updated.emit(100)
            
            if files_downloaded > 0:
                self.status_updated.emit(f"✅ Successfully downloaded {files_downloaded}/{total_files} embedding files")
                self.download_completed.emit(True)
            else:
                self.status_updated.emit("❌ No embedding files were downloaded successfully")
                self.download_completed.emit(False)
                    
        except Exception as e:
            self.status_updated.emit(f"Download failed: {str(e)}")
            self.download_completed.emit(False)
    
    def _download_file_direct(self, url: str, dest_path: str):
        """Download file directly with progress tracking"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # We don't emit progress here since we're doing it per file in the main loop
    
    def _download_file(self, url: str, dest_path: str):
        """Download file with progress tracking (legacy method)"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 40)  # Use 40% for download
                        self.progress_updated.emit(progress)

class EmbeddingManager(QObject):
    """Manager for embedding models with download capabilities"""
    
    def __init__(self, app_dirs: AppDirs):
        super().__init__()
        self.app_dirs = app_dirs
        self._uni_model = None
        self._bi_model = None
    
    def are_embeddings_available(self) -> bool:
        """Check if embedding files are available"""
        embeddings_dir = Path(self.app_dirs.embeddings_dir)
        
        required_files = [
            "embeddings_8",
            "embeddings_bi_grams"
        ]
        
        return all((embeddings_dir / file).exists() for file in required_files)
    
    def get_missing_files(self) -> list:
        """Get list of missing embedding files"""
        embeddings_dir = Path(self.app_dirs.embeddings_dir)
        
        required_files = [
            "embeddings_8",
            "embeddings_8.trainables.syn1neg.npy", 
            "embeddings_8.wv.vectors.npy",
            "embeddings_bi_grams"
        ]
        
        missing = []
        for file in required_files:
            if not (embeddings_dir / file).exists():
                missing.append(file)
                
        return missing
    
    def create_download_thread(self, force: bool = False) -> DownloadThread:
        """Create a download thread for embeddings"""
        return DownloadThread(self.app_dirs, force)
    
    def get_embeddings_status(self) -> dict:
        """Get detailed status of embedding files"""
        embeddings_dir = Path(self.app_dirs.embeddings_dir)
        required_files = [
            "embeddings_8",
            "embeddings_8.trainables.syn1neg.npy", 
            "embeddings_8.wv.vectors.npy",
            "embeddings_bi_grams"
        ]
        
        status = {}
        for file in required_files:
            file_path = embeddings_dir / file
            if file_path.exists():
                status[file] = {
                    'exists': True,
                    'size': file_path.stat().st_size,
                    'path': str(file_path)
                }
            else:
                status[file] = {
                    'exists': False,
                    'size': 0,
                    'path': str(file_path)
                }
        
        return status
    
    def load_unigram_model(self) -> Optional[Word2Vec]:
        """Load unigram Word2Vec model"""
        if self._uni_model is None:
            model_path = os.path.join(self.app_dirs.embeddings_dir, "embeddings_8")
            if os.path.exists(model_path):
                try:
                    self._uni_model = Word2Vec.load(model_path)
                except Exception as e:
                    print(f"Error loading unigram model: {e}")
                    return None
            else:
                return None
        return self._uni_model
    
    def load_bigram_model(self) -> Optional[Word2Vec]:
        """Load bigram Word2Vec model"""
        if self._bi_model is None:
            model_path = os.path.join(self.app_dirs.embeddings_dir, "embeddings_bi_grams")
            if os.path.exists(model_path):
                try:
                    self._bi_model = Word2Vec.load(model_path)
                except Exception as e:
                    print(f"Error loading bigram model: {e}")
                    return None
            else:
                return None
        return self._bi_model
    
    def get_model(self, model_type: str) -> Optional[Word2Vec]:
        """Get model by type ('uni' or 'bi')"""
        if model_type == 'uni':
            return self.load_unigram_model()
        elif model_type == 'bi':
            return self.load_bigram_model()
        else:
            return None
    
    def clear_cache(self):
        """Clear cached models"""
        self._uni_model = None
        self._bi_model = None