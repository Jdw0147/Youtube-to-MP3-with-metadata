import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget,
    QHBoxLayout, QFrame, QSizePolicy
)
from SongPage import SongPage
from AlbumPage import AlbumPage
from ManualEntry import ManualEntry
#from ImportPlaylist import ImportPlaylist

from PySide6.QtCore import Qt

class LandingPage(QWidget):
    def __init__(self, switch_to_song, switch_to_album,):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(32)
        layout.setContentsMargins(32, 32, 32, 32)
        label = QLabel("YouTube to MP3 Converter")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(60)

        song_layout = QVBoxLayout()
        btn_song = QPushButton()
        btn_song.setFixedSize(140, 140)
        btn_song.setText("🎵")
        btn_song.setStyleSheet("font-size: 64px;")
        btn_song.clicked.connect(switch_to_song)
        song_label = QLabel("Convert a single song with full metadata control.")
        song_label.setWordWrap(True)
        song_label.setAlignment(Qt.AlignCenter)
        song_layout.addWidget(btn_song, alignment=Qt.AlignCenter)
        song_layout.addWidget(song_label, alignment=Qt.AlignCenter)

        # Album button and description
        album_layout = QVBoxLayout()
        btn_album = QPushButton()
        btn_album.setFixedSize(140, 140)
        btn_album.setText("💿")
        btn_album.setStyleSheet("font-size: 64px;")
        btn_album.clicked.connect(switch_to_album)
        album_label = QLabel(
            "Import multiple songs individually or from a YouTube playlist, "
            "entering album info just once."
        )
        album_label.setWordWrap(True)
        album_label.setAlignment(Qt.AlignCenter)
        album_layout.addWidget(btn_album, alignment=Qt.AlignCenter)
        album_layout.addWidget(album_label, alignment=Qt.AlignCenter)

        # Add layouts to horizontal layout
        h_layout.addStretch(1)
        h_layout.addLayout(song_layout)
        h_layout.addStretch(1)
        h_layout.addLayout(album_layout)
        h_layout.addStretch(1)

        layout.addSpacing(20)
        layout.addLayout(h_layout)
        layout.addSpacing(20)

        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to MP3 Converter")
        self.stack = QStackedWidget()

        self.landing = LandingPage(self.show_song, self.show_album)
        self.album_page = AlbumPage(self.show_landing, self.show_album_manual_entry, self.show_album_playlist_import)
        self.album_manual_entry_page = ManualEntry(self.show_album)
        #self.album_playlist_import_page = ImportPlaylist(self.show_album)
        self.song_page = SongPage(self.show_landing)

        self.stack.addWidget(self.landing)
        self.stack.addWidget(self.album_page)
        self.stack.addWidget(self.album_manual_entry_page)
        #self.stack.addWidget(self.album_playlist_import_page)
        self.stack.addWidget(self.song_page)
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.stack.setCurrentWidget(self.landing)

    def show_song(self):
        self.stack.setCurrentWidget(self.song_page)
        
    def show_album(self):
        self.stack.setCurrentWidget(self.album_page)

    def show_album_manual_entry(self):
        self.stack.setCurrentWidget(self.album_manual_entry_page)

    def show_album_playlist_import(self):
        pass
    #    self.stack.setCurrentWidget(self.album_playlist_import_page)

    def show_landing(self):
        self.stack.setCurrentWidget(self.landing)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
    window = MainWindow()
    window.setFixedSize(700, 700)  # Square window
    window.show()
    sys.exit(app.exec())