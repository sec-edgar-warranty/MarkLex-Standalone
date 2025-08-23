"""
Text analysis widget for analyzing documents against lexicons
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
                            QGroupBox, QMessageBox, QFileDialog, QProgressDialog,
                            QFrame, QSplitter, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from models.embedding_manager import EmbeddingManager
from models.text_processor import TextProcessor
from models.lexicon_manager import LexiconManager

class TextAnalysisThread(QThread):
    """Thread for text analysis to prevent UI blocking"""
    
    result_ready = pyqtSignal(pd.DataFrame)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, text_processor: TextProcessor, text_input: str, lexicon: pd.DataFrame):
        super().__init__()
        self.text_processor = text_processor
        self.text_input = text_input
        self.lexicon = lexicon
    
    def run(self):
        """Analyze text in separate thread"""
        try:
            result = self.text_processor.analyze_text(self.text_input, self.lexicon)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(f"Error analyzing text: {str(e)}")

class AnalysisWidget(QWidget):
    """Widget for text analysis"""
    
    def __init__(self, embedding_manager: EmbeddingManager):
        super().__init__()
        self.embedding_manager = embedding_manager
        self.text_processor = TextProcessor()
        self.lexicon_manager = LexiconManager(embedding_manager.app_dirs)
        self.current_data = None
        self.current_text_preview = ""
        self.analysis_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Text Analysis")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Instructions
        instructions_frame = QFrame()
        instructions_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        instructions_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        instructions_layout = QVBoxLayout(instructions_frame)
        
        instructions_text = QLabel("""
        <b>📝 Instructions:</b> This section provides a demonstration of lexicon usage. 
        The system analyzes text against eight business dimensions: <b>Marketing, ESG, DEI, Risk & Security, 
        Employee, AI & Data, Innovation, and Investor Focus</b>. Paste your text below and click "Analyze Text". 
        The output table shows each sentence and the number of words associated with these dimensions.
        """)
        instructions_text.setWordWrap(True)
        instructions_layout.addWidget(instructions_text)
        layout.addWidget(instructions_frame)
        
        # Create splitter for input and results
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Input section
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Text input
        input_group = QGroupBox("Text Input")
        input_group_layout = QVBoxLayout(input_group)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Paste your text here for analysis...")
        self.text_input.setMaximumHeight(200)
        input_group_layout.addWidget(self.text_input)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.analyze_button = QPushButton("Analyze Text")
        self.analyze_button.clicked.connect(self.analyze_text)
        button_layout.addWidget(self.analyze_button)
        
        self.reset_button = QPushButton("Reset Analysis")
        self.reset_button.setProperty("class", "secondary")
        self.reset_button.clicked.connect(self.reset_analysis)
        button_layout.addWidget(self.reset_button)
        
        self.load_file_button = QPushButton("Load Text File")
        self.load_file_button.setProperty("class", "secondary")
        self.load_file_button.clicked.connect(self.load_text_file)
        button_layout.addWidget(self.load_file_button)
        
        button_layout.addStretch()
        input_group_layout.addLayout(button_layout)
        
        input_layout.addWidget(input_group)
        splitter.addWidget(input_widget)
        
        # Results section
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        
        # Results header
        results_header = QHBoxLayout()
        
        self.results_label = QLabel("Analysis results will appear here")
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.results_label.setStyleSheet("color: #666; font-style: italic;")
        results_header.addWidget(self.results_label)
        
        results_header.addStretch()
        
        self.export_button = QPushButton("📥 Export Analysis Data")
        self.export_button.clicked.connect(self.export_data)
        self.export_button.setEnabled(False)
        results_header.addWidget(self.export_button)
        
        results_layout.addLayout(results_header)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setVisible(False)
        results_layout.addWidget(self.results_table)
        
        splitter.addWidget(results_widget)
        
        # Set splitter sizes (40% input, 60% results)
        splitter.setSizes([400, 600])
        
        # Lexicon info section
        self.setup_lexicon_info(layout)
    
    def setup_lexicon_info(self, layout):
        """Setup lexicon information section"""
        lexicon_info = QGroupBox("📊 Current Lexicon Dimensions")
        lexicon_layout = QVBoxLayout(lexicon_info)
        
        # Create scrollable area for lexicon info
        scroll_area = QScrollArea()
        scroll_area.setMaximumHeight(150)
        scroll_area.setWidgetResizable(True)
        
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        
        # Load and display lexicon information
        lexicon = self.lexicon_manager.load_lexicon()
        entities = self.lexicon_manager.get_entities()
        
        info_text = "<p><b>Available analysis dimensions:</b></p><ul>"
        for entity in entities:
            keywords = self.lexicon_manager.get_keywords_for_entity(entity)
            keyword_preview = ", ".join(keywords[:5])  # Show first 5 keywords
            if len(keywords) > 5:
                keyword_preview += f" (and {len(keywords) - 5} more)"
            info_text += f"<li><b>{entity}</b>: {keyword_preview}</li>"
        info_text += "</ul>"
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        scroll_area.setWidget(info_widget)
        lexicon_layout.addWidget(scroll_area)
        layout.addWidget(lexicon_info)
    
    def load_text_file(self):
        """Load text from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Text File",
            "",
            "Text files (*.txt);;All files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Load Failed", f"Failed to load file:\\n{str(e)}")
    
    def analyze_text(self):
        """Analyze the input text"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "No Text", "Please enter some text to analyze.")
            return
        
        # Disable controls during analysis
        self.analyze_button.setEnabled(False)
        self.analyze_button.setText("Analyzing...")
        
        # Show progress dialog
        self.progress = QProgressDialog("Analyzing text...", "Cancel", 0, 0, self)
        self.progress.setModal(True)
        self.progress.show()
        
        # Load lexicon
        lexicon = self.lexicon_manager.load_lexicon()
        
        # Start analysis thread
        self.analysis_thread = TextAnalysisThread(self.text_processor, text, lexicon)
        self.analysis_thread.result_ready.connect(self.on_analysis_ready)
        self.analysis_thread.error_occurred.connect(self.on_analysis_error)
        self.analysis_thread.start()
    
    def on_analysis_ready(self, df: pd.DataFrame):
        """Handle analysis completion"""
        self.progress.close()
        
        self.current_data = df
        self.current_text_preview = self.text_input.toPlainText()[:100]
        if len(self.text_input.toPlainText()) > 100:
            self.current_text_preview += "..."
        
        # Display results
        self.display_results(df)
        
        # Re-enable controls
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("Analyze Text")
        self.export_button.setEnabled(True)
        
        # Update status
        sentence_count = len(df) if not df.empty else 0
        self.results_label.setText(f"Analysis completed: {sentence_count} sentences analyzed")
        self.results_label.setStyleSheet("color: #2E5CB8; font-weight: bold;")
    
    def on_analysis_error(self, error_msg: str):
        """Handle analysis error"""
        self.progress.close()
        
        # Re-enable controls
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("Analyze Text")
        
        # Show error
        QMessageBox.critical(self, "Analysis Error", error_msg)
        
        self.results_label.setText("Error analyzing text")
        self.results_label.setStyleSheet("color: red;")
    
    def display_results(self, df: pd.DataFrame):
        """Display analysis results in table"""
        if df.empty:
            self.results_table.setVisible(False)
            return
        
        self.results_table.setVisible(True)
        self.results_table.setRowCount(len(df))
        self.results_table.setColumnCount(len(df.columns))
        self.results_table.setHorizontalHeaderLabels(df.columns.tolist())
        
        # Populate table
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = df.iloc[row, col]
                # Truncate long text for display
                if col == 0 and isinstance(value, str) and len(value) > 100:
                    display_value = value[:97] + "..."
                else:
                    display_value = str(value)
                    
                item = QTableWidgetItem(display_value)
                
                # Set tooltip for full text
                if col == 0 and isinstance(value, str):
                    item.setToolTip(value)
                
                self.results_table.setItem(row, col, item)
        
        # Adjust column widths
        self.results_table.resizeColumnsToContents()
        
        # Set minimum width for text column
        if df.shape[1] > 0:
            self.results_table.setColumnWidth(0, 300)
        
        # Hide row numbers
        self.results_table.verticalHeader().setVisible(False)
    
    def reset_analysis(self):
        """Reset analysis data and UI"""
        self.current_data = None
        self.current_text_preview = ""
        
        self.text_input.clear()
        self.results_table.setVisible(False)
        self.results_label.setText("Analysis results will appear here")
        self.results_label.setStyleSheet("color: #666; font-style: italic;")
        
        self.export_button.setEnabled(False)
    
    def export_data(self):
        """Export analysis results"""
        if self.current_data is None:
            QMessageBox.warning(self, "No Data", "No analysis data available to export.")
            return
        
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"text_analysis_{timestamp}.csv"
        
        # Get save location
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Analysis Data",
            default_filename,
            "CSV files (*.csv);;All files (*)"
        )
        
        if filename:
            try:
                self.current_data.to_csv(filename, index=False)
                QMessageBox.information(self, "Export Successful", f"Analysis data exported to:\\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export data:\\n{str(e)}")