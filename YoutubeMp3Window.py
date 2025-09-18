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

class YoutubeMp3Window(QWidget):
    """
    Main window for the YouTube → MP3 converter app using PySide6 (Qt).
    In Qt, every visible window is a QWidget (or subclass of QWidget).
    """

    def __init__(self):
        super().__init__()  # Initializing the base (parent) QWidget class
        self.setWindowTitle("Convert Youtube to MP3")   # Setting window title

        # INPUT FIELDS
        # Remember QLineEdit is single line input, QTextEdit is multi-line input
        # Defining as a dictionary so we can loop over it, creating the form easily
        self.fields = {
            "YouTube URL": QLineEdit(),
            "Title": QLineEdit(),
            "Artist": QLineEdit(),
            "Album": QLineEdit(),
            "Year": QLineEdit(),
            "Genre": QLineEdit(),
            "Track Number": QLineEdit(),
            "Lyrics": QTextEdit(),
        }