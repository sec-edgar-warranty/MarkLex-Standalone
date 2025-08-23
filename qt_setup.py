"""
Qt Platform Setup - Must be imported before any PyQt6 imports
This module sets the Qt platform for CI/headless environments
"""

import os
import sys

# Set Qt platform for CI/headless environments BEFORE any PyQt6 imports
def setup_qt_platform():
    """Setup Qt platform for CI/headless environments"""
    if (os.environ.get('CI') == 'true' or 
        'GITHUB_ACTIONS' in os.environ or 
        'RUNNER_OS' in os.environ or
        'DISPLAY' not in os.environ or 
        os.environ.get('DISPLAY') == '' or
        os.environ.get('DISPLAY') == ':0' or
        not hasattr(sys, 'ps1')):  # Not in interactive Python
        
        print("🔧 Setting Qt platform to offscreen for CI/headless environment")
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        os.environ['QT_LOGGING_RULES'] = '*=false'
        return True
    return False

# Run setup immediately when this module is imported
setup_qt_platform()