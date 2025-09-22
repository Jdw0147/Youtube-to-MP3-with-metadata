import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata