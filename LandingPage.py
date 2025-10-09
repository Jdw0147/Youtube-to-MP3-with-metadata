import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
)
from YoutubeMp3Window import YoutubeMp3Window

class LandingPage(QWidget):
    def __init__(self, switch_to_song, switch_to_album,):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("YouTube to MP3 Converter")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        btn_song = QPushButton("Convert Song")
        btn_album = QPushButton("Convert Album/Playlist")
        btn_song.clicked.connect(switch_to_song)
        btn_album.clicked.connect(switch_to_album)
        layout.addWidget(btn_song)
        layout.addWidget(btn_album)
        self.setLayout(layout)

class AlbumPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Convert an Album/Playlist")
        label.setAlignment(Qt.AlignCenter)
        btn_playlist = QPushButton("Export from Youtube Playlist")
        btn_manual = QPushButton("Enter songs manually")
        layout.addWidget(label)
        layout.addWidget(btn_playlist)
        layout.addWidget(btn_manual)

