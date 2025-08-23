"""
Lexicon creation widget - main functionality for creating word lexicons
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QSlider, QTableWidget,
                            QTableWidgetItem, QGroupBox, QTextEdit, QMessageBox,
                            QFileDialog, QProgressDialog, QFrame, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from models.embedding_manager import EmbeddingManager

class LexiconGenerationThread(QThread):
    """Thread for generating lexicon to prevent UI blocking"""
    
    result_ready = pyqtSignal(pd.DataFrame)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, embedding_manager: EmbeddingManager, term: str, n_words: int, model_type: str):
        super().__init__()
        self.embedding_manager = embedding_manager
        self.term = term
        self.n_words = n_words
        self.model_type = model_type
    
    def run(self):
        """Generate lexicon in separate thread"""
        try:
            model = self.embedding_manager.get_model(self.model_type)
            if model is None:
                self.error_occurred.emit(f"❌ {self.model_type.title()}gram model not found or failed to load")
                return
            
            term_formatted = self.term.lower().replace(' ', '_')
            
            if term_formatted not in model.wv.key_to_index:
                self.error_occurred.emit(f'Word "{self.term}" not found in vocabulary')
                return
            
            # Get similar words
            similar_words = model.wv.most_similar(term_formatted, topn=self.n_words)
            
            # Create DataFrame
            df = pd.DataFrame(similar_words, columns=['Similar Word', 'Similarity Score'])
            df['Similarity Score'] = df['Similarity Score'].round(3)
            df.insert(0, 'Word Number', range(1, len(df) + 1))
            
            # Clean up word formatting (replace underscores with spaces)
            df['Similar Word'] = df['Similar Word'].str.replace('_', ' ')
            
            self.result_ready.emit(df)
            
        except Exception as e:
            self.error_occurred.emit(f"Error generating lexicon: {str(e)}")

class LexiconWidget(QWidget):
    """Widget for creating lexicons"""
    
    def __init__(self, embedding_manager: EmbeddingManager):
        super().__init__()
        self.embedding_manager = embedding_manager
        self.current_data = None
        self.current_term = ""
        self.generation_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Lexicon Creation")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Quick start info
        info_frame = QFrame()
        info_frame.setProperty("class", "info")
        info_layout = QVBoxLayout(info_frame)
        
        info_label = QLabel("""
        <b>💡 Quick Start:</b> Enter a unigram (e.g., 'marketing') or bigram (e.g., 'profit margin') below, 
        set the number of words, and click 'Create Lexicon' to generate semantically similar terms.
        """)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        layout.addWidget(info_frame)
        
        # Create splitter for two-panel layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Input group
        input_group = QGroupBox("Input Parameters")
        input_layout = QVBoxLayout(input_group)
        
        # Term input
        term_label = QLabel("Term (max 2 words):")
        input_layout.addWidget(term_label)
        
        self.term_input = QLineEdit()
        self.term_input.setPlaceholderText("sustainability")
        self.term_input.returnPressed.connect(self.create_lexicon)
        input_layout.addWidget(self.term_input)
        
        # Number of words slider
        words_label = QLabel("Number of words:")
        input_layout.addWidget(words_label)
        
        self.words_slider = QSlider(Qt.Orientation.Horizontal)
        self.words_slider.setMinimum(10)
        self.words_slider.setMaximum(100)
        self.words_slider.setValue(20)
        self.words_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.words_slider.setTickInterval(10)
        input_layout.addWidget(self.words_slider)
        
        self.words_value_label = QLabel("20")
        self.words_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.words_slider.valueChanged.connect(lambda v: self.words_value_label.setText(str(v)))
        input_layout.addWidget(self.words_value_label)
        
        left_layout.addWidget(input_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.create_button = QPushButton("Create Lexicon")
        self.create_button.clicked.connect(self.create_lexicon)
        button_layout.addWidget(self.create_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setProperty("class", "secondary")
        self.reset_button.clicked.connect(self.reset_data)
        button_layout.addWidget(self.reset_button)
        
        left_layout.addLayout(button_layout)
        
        # Export button
        self.export_button = QPushButton("📥 Export Lexicon")
        self.export_button.clicked.connect(self.export_data)
        self.export_button.setEnabled(False)
        left_layout.addWidget(self.export_button)
        
        left_layout.addStretch()
        splitter.addWidget(left_panel)
        
        # Right panel - Results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Results label
        self.results_label = QLabel("Lexicon results will appear here")
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setStyleSheet("color: #666; font-style: italic;")
        right_layout.addWidget(self.results_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setVisible(False)
        right_layout.addWidget(self.results_table)
        
        splitter.addWidget(right_panel)
        
        # Set splitter sizes (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        # Instructions section
        self.setup_instructions(layout)
    
    def setup_instructions(self, layout):
        """Setup detailed instructions section"""
        instructions_group = QGroupBox("📚 6-Step Lexicon Development Process")
        instructions_layout = QVBoxLayout(instructions_group)
        
        instructions_text = QTextEdit()
        instructions_text.setMaximumHeight(200)
        instructions_text.setReadOnly(True)
        instructions_text.setHtml("""
        <p><b>Follow this systematic approach for building high-quality lexicons:</b></p>
        
        <p><b>Step 1: Enter Construct</b><br>
        Enter a unigram (single term: marketing, profit, privacy) or bigram (two terms: profit margin, customer satisfaction).
        Use domain-specific terminology relevant to your research construct.</p>
        
        <p><b>Step 2: Export Top-N Neighbors</b><br>
        Start with N=50 similar words to get initial coverage. Expand to N=100 if recall seems thin.
        Download the results as CSV for systematic review.</p>
        
        <p><b>Step 3: Iterative Expansion</b><br>
        Promote good neighbors to seeds for the next iteration. Re-run the process 1–2 times to widen coverage.
        Domain-specific variants emerge quickly through this iterative approach.</p>
        
        <p><b>Step 4: Prune & Disambiguate</b><br>
        Remove irrelevant or ambiguous terms from your lexicon. Prefer bigrams where needed to reduce ambiguity.
        Focus on terms that clearly represent your target construct.</p>
        
        <p><b>Step 5: Validation</b><br>
        Conduct human review with Inter-Annotator Agreement (IAA) on a sentence sample.
        Report key metrics: Accuracy, Precision, Recall, and F1 score.</p>
        
        <p><b>Step 6: Documentation & Versioning</b><br>
        Version your final lexicon (e.g., v1.0, v1.1). Include provenance notes: seed words used, app version, source corpus.
        Maintain documentation for reproducibility and future updates.</p>
        
        <p><b>Troubleshooting:</b> If the app fails to return results, try variations of your search terms or related concepts.
        Not all terms may be present in the vocabulary - experiment with synonyms or broader/narrower terms.</p>
        """)
        
        instructions_layout.addWidget(instructions_text)
        layout.addWidget(instructions_group)
    
    def create_lexicon(self):
        """Create lexicon from input parameters"""
        term = self.term_input.text().strip()
        if not term:
            QMessageBox.warning(self, "Input Required", "Please enter a term to create a lexicon.")
            return
        
        # Check word count
        word_count = len(term.split())
        if word_count > 2:
            QMessageBox.warning(self, "Invalid Input", "Please enter maximum 2 words.")
            return
        
        # Determine model type
        model_type = 'uni' if word_count == 1 else 'bi'
        n_words = self.words_slider.value()
        
        # Disable controls during generation
        self.create_button.setEnabled(False)
        self.create_button.setText("Creating...")
        
        # Show progress dialog
        self.progress = QProgressDialog("Generating lexicon...", "Cancel", 0, 0, self)
        self.progress.setModal(True)
        self.progress.show()
        
        # Start generation thread
        self.generation_thread = LexiconGenerationThread(
            self.embedding_manager, term, n_words, model_type
        )
        self.generation_thread.result_ready.connect(self.on_lexicon_ready)
        self.generation_thread.error_occurred.connect(self.on_lexicon_error)
        self.generation_thread.start()
    
    def on_lexicon_ready(self, df: pd.DataFrame):
        """Handle lexicon generation completion"""
        self.progress.close()
        
        self.current_data = df
        self.current_term = self.term_input.text().strip()
        
        # Update results table
        self.display_results(df)
        
        # Re-enable controls
        self.create_button.setEnabled(True)
        self.create_button.setText("Create Lexicon")
        self.export_button.setEnabled(True)
        
        self.results_label.setText(f"Generated {len(df)} similar terms for '{self.current_term}'")
        self.results_label.setStyleSheet("color: #2E5CB8; font-weight: bold;")
    
    def on_lexicon_error(self, error_msg: str):
        """Handle lexicon generation error"""
        self.progress.close()
        
        # Re-enable controls
        self.create_button.setEnabled(True)
        self.create_button.setText("Create Lexicon")
        
        # Show error
        QMessageBox.critical(self, "Lexicon Generation Error", error_msg)
        
        self.results_label.setText("Error generating lexicon")
        self.results_label.setStyleSheet("color: red;")
    
    def display_results(self, df: pd.DataFrame):
        """Display results in table"""
        self.results_table.setVisible(True)
        self.results_table.setRowCount(len(df))
        self.results_table.setColumnCount(len(df.columns))
        self.results_table.setHorizontalHeaderLabels(df.columns.tolist())
        
        # Populate table
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.results_table.setItem(row, col, item)
        
        # Adjust column widths
        self.results_table.resizeColumnsToContents()
        
        # Hide row numbers if desired
        self.results_table.verticalHeader().setVisible(False)
    
    def reset_data(self):
        """Reset all data and UI"""
        self.current_data = None
        self.current_term = ""
        
        self.term_input.clear()
        self.words_slider.setValue(20)
        
        self.results_table.setVisible(False)
        self.results_label.setText("Lexicon results will appear here")
        self.results_label.setStyleSheet("color: #666; font-style: italic;")
        
        self.export_button.setEnabled(False)
    
    def export_data(self):
        """Export current lexicon data"""
        if self.current_data is None:
            QMessageBox.warning(self, "No Data", "No lexicon data available to export.")
            return
        
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"lexicon_{self.current_term.replace(' ', '_')}_{timestamp}.csv"
        
        # Get save location
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Lexicon Data",
            default_filename,
            "CSV files (*.csv);;All files (*)"
        )
        
        if filename:
            try:
                self.current_data.to_csv(filename, index=False)
                QMessageBox.information(self, "Export Successful", f"Lexicon data exported to:\\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export data:\\n{str(e)}")