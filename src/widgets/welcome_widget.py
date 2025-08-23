"""
Welcome widget with application introduction
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class WelcomeWidget(QWidget):
    """Welcome tab widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Set white background
        self.setStyleSheet("QWidget { background-color: #ffffff; }")
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { background-color: #ffffff; border: none; }")
        layout.addWidget(scroll)
        
        # Content widget
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #ffffff; }")
        scroll.setWidget(content)
        content_layout = QVBoxLayout(content)
        
        # Title
        title = QLabel("Welcome to MarkLex")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Marketing Lexicon Creation Tool")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        content_layout.addWidget(subtitle)
        
        # Main content
        content_text = QLabel("""
        <div style="max-width: 800px;">
        <p style="font-size: 14px; line-height: 1.6;">
        MarkLex is a powerful desktop application designed to help researchers, analysts, and marketers 
        create comprehensive lexicons and analyze text for specific themes and keywords.
        </p>
        
        <h3 style="color: #2E5CB8; margin-top: 30px;">🔍 Key Features</h3>
        
        <div style="margin: 20px 0;">
        <h4>📝 Lexicon Creation</h4>
        <p style="margin-left: 20px; line-height: 1.5;">
        Generate semantically similar terms based on seed words using advanced Word2Vec embeddings:
        </p>
        <ul style="margin-left: 40px; line-height: 1.5;">
        <li><strong>Unigram Support:</strong> Single word terms (e.g., "marketing", "sustainability")</li>
        <li><strong>Bigram Support:</strong> Two-word phrases (e.g., "profit margin", "customer satisfaction")</li>
        <li><strong>Customizable Results:</strong> Generate 10-100 similar terms per seed word</li>
        <li><strong>Export Capabilities:</strong> Download results as CSV for further analysis</li>
        </ul>
        </div>
        
        <div style="margin: 20px 0;">
        <h4>🔬 Text Analysis</h4>
        <p style="margin-left: 20px; line-height: 1.5;">
        Analyze documents against predefined business dimensions:
        </p>
        <ul style="margin-left: 40px; line-height: 1.5;">
        <li><strong>Marketing:</strong> Brand, advertising, promotion themes</li>
        <li><strong>ESG:</strong> Environmental, social, and governance topics</li>
        <li><strong>Risk & Security:</strong> Compliance, audit, security themes</li>
        <li><strong>Custom Dimensions:</strong> Build your own analysis categories</li>
        </ul>
        </div>
        
        <div style="margin: 20px 0;">
        <h4>⚡ Advanced Processing</h4>
        <ul style="margin-left: 40px; line-height: 1.5;">
        <li><strong>Intelligent Text Processing:</strong> Advanced tokenization and cleaning</li>
        <li><strong>N-gram Analysis:</strong> Analyze unigrams, bigrams, and trigrams</li>
        <li><strong>Sentence-level Analysis:</strong> Detailed breakdown by sentence</li>
        <li><strong>Batch Processing:</strong> Analyze large documents efficiently</li>
        </ul>
        </div>
        
        <h3 style="color: #2E5CB8; margin-top: 30px;">🚀 Getting Started</h3>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #2E5CB8; margin: 20px 0;">
        <p><strong>First Time Setup:</strong></p>
        <ol style="line-height: 1.5;">
        <li>Go to the <strong>Setup</strong> tab to download required embedding models</li>
        <li>Once download is complete, explore the <strong>Lexicon</strong> tab to create word lists</li>
        <li>Use the <strong>Text Analysis</strong> tab to analyze documents</li>
        <li>Export your results for further research and analysis</li>
        </ol>
        </div>
        
        <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <p><strong>💡 Tip:</strong> Start with broad seed terms and use the iterative expansion process 
        described in the Lexicon tab for best results. The 6-step lexicon development process will 
        guide you through creating high-quality, validated lexicons.</p>
        </div>
        
        <h3 style="color: #2E5CB8; margin-top: 30px;">🔬 Research Applications</h3>
        
        <p style="line-height: 1.6;">MarkLex is ideal for:</p>
        <ul style="line-height: 1.5;">
        <li><strong>Academic Research:</strong> Content analysis, theme identification, systematic literature reviews</li>
        <li><strong>Business Intelligence:</strong> Market analysis, competitor monitoring, trend identification</li>
        <li><strong>Policy Research:</strong> Document analysis, regulatory compliance, stakeholder communication</li>
        <li><strong>Marketing Research:</strong> Brand analysis, campaign evaluation, consumer sentiment</li>
        </ul>
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; background-color: #f0f8ff; border-radius: 5px;">
        <p style="font-size: 16px; color: #2E5CB8; font-weight: bold;">
        Ready to start building lexicons? Head to the Setup tab to get started!
        </p>
        </div>
        </div>
        """)
        
        content_text.setWordWrap(True)
        content_text.setTextFormat(Qt.TextFormat.RichText)
        content_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_text.setStyleSheet("margin: 20px;")
        content_layout.addWidget(content_text)
        
        content_layout.addStretch()