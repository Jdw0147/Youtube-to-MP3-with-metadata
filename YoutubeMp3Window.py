import os
import sys
from PySide6.QtWidgets import (
    QApplication,   # Application object (this manages the event loop)
    QWidget,  # Base class for all UI objects
    QLineEdit,  # Single line text inputs ex.) Title & Artist
    QTextEdit,  # Multi line text input ex.) Lyrics
    QPushButton,    # Clickable button
    QLabel, # Text display label
    QFileDialog,    #File/folder selection windows (for output path and album art path)
    QVBoxLayout,    # Vertical stacking layout manager
    QHBoxLayout,    # Horizontal stacking layout manager
    QFormLayout,    # Layout manager for forms (label + input field)
    QMessageBox    # Popup boxes (errors, success messages, etc)
)
from PySide6.QtCore import Qt
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata