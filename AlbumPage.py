from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QScrollArea, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class SongEntry(QGroupBox):
    def __init__(self, song_number, remove_callback):
        super().__init__(f"Song {song_number}")
        self.remove_callback = remove_callback
        layout = QVBoxLayout()

        self.song_name = QLineEdit()
        self.song_name.setPlaceholderText("Song Name")
        self.song_artist = QLineEdit()
        self.song_artist.setPlaceholderText("Artist")
        self.track_number = QLineEdit()
        self.track_number.setPlaceholderText("Track Number")
        self.lyrics = QTextEdit()
        self.lyrics.setPlaceholderText("Lyrics")

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_self)

        layout.addWidget(QLabel("Song Name:"))
        layout.addWidget(self.song_name)
        layout.addWidget(QLabel("Song Artist:"))
        layout.addWidget(self.song_artist)
        layout.addWidget(QLabel("Track Number:"))
        layout.addWidget(self.track_number)
        layout.addWidget(QLabel("Lyrics:"))
        layout.addWidget(self.lyrics)
        layout.addWidget(remove_btn, alignment=Qt.AlignRight)
        self.setLayout(layout)

    def remove_self(self):
        self.remove_callback(self)

class AlbumPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn, alignment=0)
        label = QLabel("Convert an Album/Playlist")
        label.setAlignment(0x84)  # Qt.AlignCenter
        btn_playlist = QPushButton("Export from Youtube Playlist")
        btn_manual = QPushButton("Enter songs manually")
        layout.addWidget(label)
        layout.addWidget(btn_playlist)
        layout.addWidget(btn_manual)
        self.setLayout(layout)