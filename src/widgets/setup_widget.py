"""
Setup widget for downloading embeddings
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QProgressBar, QTextEdit, QGroupBox,
                            QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from models.embedding_manager import EmbeddingManager

class SetupWidget(QWidget):
    """Widget for setting up embeddings"""
    
    setup_completed = pyqtSignal()
    
    def __init__(self, embedding_manager: EmbeddingManager):
        super().__init__()
        self.embedding_manager = embedding_manager
        self.download_thread = None
        
        self.setup_ui()
        self.check_initial_state()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Setup MarkLex")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
        <p>MarkLex requires embedding models for lexicon creation and text analysis. 
        These models will be downloaded from the official GitHub repository.</p>
        
        <p><b>What will be downloaded:</b></p>
        <ul>
        <li>Unigram embedding model (embeddings_8)</li>
        <li>Bigram embedding model (embeddings_bi_grams)</li>
        <li>Default lexicon file</li>
        </ul>
        
        <p><b>Note:</b> This is a one-time setup. The files are approximately 300MB total.</p>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Status group
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Checking embedding files...")
        status_layout.addWidget(self.status_label)
        
        # Missing files list
        self.missing_files_edit = QTextEdit()
        self.missing_files_edit.setMaximumHeight(100)
        self.missing_files_edit.setReadOnly(True)
        status_layout.addWidget(self.missing_files_edit)
        
        layout.addWidget(status_group)
        
        # Download section
        download_group = QGroupBox("Download")
        download_layout = QVBoxLayout(download_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        download_layout.addWidget(self.progress_bar)
        
        # Status text
        self.download_status = QLabel("")
        download_layout.addWidget(self.download_status)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.download_button = QPushButton("Download Embeddings")
        self.download_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_button)
        
        self.force_download_button = QPushButton("Force Re-download")
        self.force_download_button.clicked.connect(lambda: self.start_download(force=True))
        button_layout.addWidget(self.force_download_button)
        
        self.check_button = QPushButton("Check Again")
        self.check_button.clicked.connect(self.check_initial_state)
        button_layout.addWidget(self.check_button)
        
        button_layout.addStretch()
        download_layout.addLayout(button_layout)
        
        layout.addWidget(download_group)
        
        layout.addStretch()
    
    def check_initial_state(self):
        """Check initial state of embeddings"""
        if self.embedding_manager.are_embeddings_available():
            self.status_label.setText("✅ All embedding files are available")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            # Show detailed file status
            status = self.embedding_manager.get_embeddings_status()
            status_text = "File Status:\\n"
            for file, info in status.items():
                if info['exists']:
                    size_mb = info['size'] / (1024 * 1024)
                    status_text += f"✅ {file} ({size_mb:.1f} MB)\\n"
                else:
                    status_text += f"❌ {file} (missing)\\n"
            
            self.missing_files_edit.setPlainText(status_text)
            self.download_button.setText("Download Completed")
            self.download_button.setEnabled(False)
            self.setup_completed.emit()
        else:
            missing_files = self.embedding_manager.get_missing_files()
            self.status_label.setText(f"❌ Missing {len(missing_files)} embedding files")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            # Show detailed file status
            status = self.embedding_manager.get_embeddings_status()
            status_text = "File Status:\\n"
            for file, info in status.items():
                if info['exists']:
                    size_mb = info['size'] / (1024 * 1024)
                    status_text += f"✅ {file} ({size_mb:.1f} MB)\\n"
                else:
                    status_text += f"❌ {file} (missing)\\n"
            
            self.missing_files_edit.setPlainText(status_text)
            self.download_button.setText("Download Embeddings")
            self.download_button.setEnabled(True)
    
    def start_download(self, force: bool = False):
        """Start downloading embeddings"""
        if not force and self.embedding_manager.are_embeddings_available():
            reply = QMessageBox.question(
                self,
                "Embeddings Already Available",
                "Embedding files are already available. Do you want to re-download them?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Disable buttons during download
        self.download_button.setEnabled(False)
        self.force_download_button.setEnabled(False)
        self.check_button.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start download thread
        self.download_thread = self.embedding_manager.create_download_thread(force)
        self.download_thread.progress_updated.connect(self.on_progress_updated)
        self.download_thread.status_updated.connect(self.on_status_updated)
        self.download_thread.download_completed.connect(self.on_download_completed)
        self.download_thread.start()
    
    def on_progress_updated(self, progress: int):
        """Handle progress update"""
        self.progress_bar.setValue(progress)
    
    def on_status_updated(self, status: str):
        """Handle status update"""
        self.download_status.setText(status)
    
    def on_download_completed(self, success: bool):
        """Handle download completion"""
        # Re-enable buttons
        self.download_button.setEnabled(True)
        self.force_download_button.setEnabled(True)
        self.check_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        if success:
            self.download_status.setText("✅ Download completed successfully!")
            self.download_status.setStyleSheet("color: green; font-weight: bold;")
            
            # Clear model cache to force reload
            self.embedding_manager.clear_cache()
            
            # Check state again
            self.check_initial_state()
            
            QMessageBox.information(
                self,
                "Download Complete",
                "Embedding files have been downloaded successfully. You can now use the Lexicon and Text Analysis tabs."
            )
        else:
            self.download_status.setText("❌ Download failed. Please try again.")
            self.download_status.setStyleSheet("color: red; font-weight: bold;")
            
            QMessageBox.warning(
                self,
                "Download Failed",
                "Failed to download embedding files. Please check your internet connection and try again."
            )