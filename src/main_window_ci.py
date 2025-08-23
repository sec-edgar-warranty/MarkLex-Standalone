"""
CI-friendly version of main_window that sets QT platform before imports
"""

import os
import sys

# Set Qt platform for CI environments BEFORE importing any PyQt6
if 'CI' in os.environ or 'GITHUB_ACTIONS' in os.environ:
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
elif 'DISPLAY' not in os.environ:
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Now import the original main_window
from main_window import *

print("✅ main_window_ci imported successfully with proper Qt platform setup")