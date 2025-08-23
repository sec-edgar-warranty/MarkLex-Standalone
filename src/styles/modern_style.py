"""
Modern styling for MarkLex Desktop Application
Inspired by contemporary design trends
"""

def get_modern_stylesheet():
    """
    Return modern stylesheet for the application
    """
    return """
    /* Main Application Styles */
    QMainWindow {
        background-color: #ffffff;
        color: #1e293b;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Tab Widget Styles */
    QTabWidget::pane {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background-color: #ffffff;
        margin-top: 4px;
    }
    
    /* Ensure tab content area is white */
    QWidget {
        background-color: #ffffff;
    }
    
    QTabWidget::tab-bar {
        left: 10px;
    }
    
    QTabBar::tab {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 24px;
        margin-right: 2px;
        color: #64748b;
        font-weight: 500;
        font-size: 14px;
        min-width: 80px;
    }
    
    QTabBar::tab:selected {
        background-color: #ffffff;
        color: #2563eb;
        border-color: #e2e8f0;
        font-weight: 600;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #f8fafc;
        color: #475569;
    }
    
    /* Button Styles */
    QPushButton {
        background-color: #3b82f6;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        color: white;
        font-weight: 600;
        font-size: 14px;
        min-width: 100px;
    }
    
    QPushButton:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }
    
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    
    QPushButton:disabled {
        background-color: #94a3b8;
        color: #e2e8f0;
    }
    
    /* Secondary Button */
    QPushButton[class="secondary"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #475569;
    }
    
    QPushButton[class="secondary"]:hover {
        background-color: #f1f5f9;
        border-color: #cbd5e1;
    }
    
    /* Success Button */
    QPushButton[class="success"] {
        background-color: #10b981;
    }
    
    QPushButton[class="success"]:hover {
        background-color: #059669;
    }
    
    /* Input Field Styles */
    QLineEdit, QTextEdit, QPlainTextEdit {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px 16px;
        background-color: #ffffff;
        font-size: 14px;
        selection-background-color: #dbeafe;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #3b82f6;
        outline: none;
    }
    
    /* Slider Styles */
    QSlider::groove:horizontal {
        border: none;
        height: 6px;
        background-color: #e5e7eb;
        border-radius: 3px;
    }
    
    QSlider::handle:horizontal {
        background-color: #3b82f6;
        border: none;
        width: 20px;
        height: 20px;
        margin: -7px 0;
        border-radius: 10px;
    }
    
    QSlider::handle:horizontal:hover {
        background-color: #2563eb;
    }
    
    QSlider::sub-page:horizontal {
        background-color: #3b82f6;
        border-radius: 3px;
    }
    
    /* Table Styles */
    QTableWidget {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background-color: #ffffff;
        alternate-background-color: #f9fafb;
        gridline-color: #f3f4f6;
        font-size: 13px;
        selection-background-color: #dbeafe;
    }
    
    QTableWidget::item {
        padding: 8px 12px;
        border: none;
    }
    
    QHeaderView::section {
        background-color: #f8fafc;
        padding: 12px 16px;
        border: none;
        border-bottom: 1px solid #e5e7eb;
        font-weight: 600;
        color: #374151;
        font-size: 13px;
    }
    
    /* Group Box Styles */
    QGroupBox {
        font-weight: 600;
        font-size: 16px;
        color: #1f2937;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 16px;
        background-color: #ffffff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 16px;
        padding: 0 8px;
        background-color: #ffffff;
    }
    
    /* Label Styles */
    QLabel {
        color: #374151;
        font-size: 14px;
    }
    
    QLabel[class="title"] {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
    }
    
    QLabel[class="subtitle"] {
        font-size: 16px;
        font-weight: 500;
        color: #6b7280;
    }
    
    QLabel[class="info"] {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 6px;
        padding: 12px;
        color: #1e40af;
    }
    
    QLabel[class="success"] {
        color: #059669;
        font-weight: 500;
    }
    
    QLabel[class="error"] {
        color: #dc2626;
        font-weight: 500;
    }
    
    /* Progress Bar Styles */
    QProgressBar {
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        text-align: center;
        font-weight: 500;
        color: #374151;
        background-color: #f9fafb;
    }
    
    QProgressBar::chunk {
        background-color: #3b82f6;
        border-radius: 5px;
    }
    
    /* Frame Styles */
    QFrame[class="card"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Scrollbar Styles */
    QScrollBar:vertical {
        background-color: #f1f5f9;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #cbd5e1;
        border-radius: 6px;
        margin: 2px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #94a3b8;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    /* Menu Bar Styles */
    QMenuBar {
        background-color: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 4px 0px;
    }
    
    QMenuBar::item {
        padding: 8px 12px;
        background-color: transparent;
        border-radius: 4px;
        margin: 0px 4px;
    }
    
    QMenuBar::item:selected {
        background-color: #f1f5f9;
    }
    
    /* Status Bar Styles */
    QStatusBar {
        background-color: #f8fafc;
        border-top: 1px solid #e5e7eb;
        padding: 8px 16px;
        color: #64748b;
    }
    
    /* Message Box Styles */
    QMessageBox {
        background-color: #ffffff;
        color: #1f2937;
    }
    
    QMessageBox QPushButton {
        min-width: 80px;
        margin: 4px;
    }
    
    /* Splitter Styles */
    QSplitter::handle {
        background-color: #e5e7eb;
        width: 2px;
        height: 2px;
    }
    
    QSplitter::handle:hover {
        background-color: #cbd5e1;
    }
    """

def get_card_style():
    """Return styles for card-like containers"""
    return """
    QWidget {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        margin: 8px;
    }
    """

def get_info_card_style():
    """Return styles for info cards"""
    return """
    QWidget {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0px;
    }
    """

def get_success_card_style():
    """Return styles for success cards"""
    return """
    QWidget {
        background-color: #ecfdf5;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0px;
    }
    """