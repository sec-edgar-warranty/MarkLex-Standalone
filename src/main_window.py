"""
Main application window with tabbed interface
"""

import os
import sys

# Set Qt platform for CI/headless environments before importing QtWidgets
if ('CI' in os.environ or 'GITHUB_ACTIONS' in os.environ or 
    'DISPLAY' not in os.environ or os.environ.get('DISPLAY') == ''):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    os.environ['QT_LOGGING_RULES'] = '*=false'

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                            QWidget, QMenuBar, QStatusBar, QMessageBox,
                            QApplication)
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QFont

from widgets.welcome_widget import WelcomeWidget
from widgets.lexicon_widget import LexiconWidget
from widgets.analysis_widget import AnalysisWidget
from widgets.setup_widget import SetupWidget
from utils.app_dirs import AppDirs
from models.embedding_manager import EmbeddingManager
from styles.modern_style import get_modern_stylesheet

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.app_dirs = AppDirs()
        self.embedding_manager = EmbeddingManager(self.app_dirs)
        
        self.setup_ui()
        self.setup_menus()
        self.setup_status_bar()
        
        # Check embeddings on startup with a slight delay
        QTimer.singleShot(1000, self.check_embeddings_on_startup)
    
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("MarkLex - Marketing Lexicon Creation")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply modern stylesheet
        self.setStyleSheet(get_modern_stylesheet())
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.welcome_tab = WelcomeWidget()
        self.setup_tab = SetupWidget(self.embedding_manager)
        self.lexicon_tab = LexiconWidget(self.embedding_manager)
        self.analysis_tab = AnalysisWidget(self.embedding_manager)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.welcome_tab, "Welcome")
        self.tab_widget.addTab(self.setup_tab, "Setup")
        self.tab_widget.addTab(self.lexicon_tab, "Lexicon")
        self.tab_widget.addTab(self.analysis_tab, "Text Analysis")
        
        # Connect setup completion signal
        self.setup_tab.setup_completed.connect(self.on_setup_completed)
        
        # Initially disable lexicon and analysis tabs
        self.tab_widget.setTabEnabled(2, False)  # Lexicon tab
        self.tab_widget.setTabEnabled(3, False)  # Analysis tab
    
    def setup_menus(self):
        """Setup application menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Export action
        export_action = QAction("&Export Data...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Re-download embeddings action
        redownload_action = QAction("&Re-download Embeddings", self)
        redownload_action.triggered.connect(self.redownload_embeddings)
        tools_menu.addAction(redownload_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About MarkLex", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def check_embeddings_on_startup(self):
        """Check if embeddings are available on startup"""
        if not self.embedding_manager.are_embeddings_available():
            # Show setup tab if embeddings are not available
            self.tab_widget.setCurrentIndex(1)  # Setup tab
            self.status_bar.showMessage("Embeddings not found. Please download them in the Setup tab.")
        else:
            # Enable lexicon and analysis tabs
            self.tab_widget.setTabEnabled(2, True)
            self.tab_widget.setTabEnabled(3, True)
            self.status_bar.showMessage("Ready - Embeddings loaded")
    
    def on_setup_completed(self):
        """Handle setup completion"""
        self.tab_widget.setTabEnabled(2, True)  # Enable Lexicon tab
        self.tab_widget.setTabEnabled(3, True)  # Enable Analysis tab
        self.status_bar.showMessage("Setup completed - Ready to create lexicons")
    
    def export_data(self):
        """Handle export data action"""
        # This will be implemented based on current active tab
        current_index = self.tab_widget.currentIndex()
        if current_index == 2:  # Lexicon tab
            self.lexicon_tab.export_data()
        elif current_index == 3:  # Analysis tab
            self.analysis_tab.export_data()
    
    def redownload_embeddings(self):
        """Handle re-download embeddings action"""
        self.tab_widget.setCurrentIndex(1)  # Switch to setup tab
        self.setup_tab.start_download(force=True)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About MarkLex",
            """
            <h3>MarkLex - Marketing Lexicon Creation</h3>
            <p>Version 1.0.0</p>
            <p>A tool for creating marketing lexicons and analyzing text for specific themes and keywords.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Lexicon Creation using Word2Vec embeddings</li>
            <li>Text Analysis for business dimensions</li>
            <li>Export capabilities for further analysis</li>
            </ul>
            <p>Built with PyQt6 and powered by machine learning.</p>
            """
        )
    
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit MarkLex?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()