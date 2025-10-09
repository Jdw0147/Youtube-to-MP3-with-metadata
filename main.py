import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
)
from YoutubeMp3Window import YoutubeMp3Window
from PySide6.QtCore import Qt

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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to MP3 Converter")
        self.stack = QStackedWidget()
        self.landing = LandingPage(self.show_song, self.show_album)
        self.song_page = YoutubeMp3Window()
        self.album_page = AlbumPage()
        self.stack.addWidget(self.landing)
        self.stack.addWidget(self.song_page)
        self.stack.addWidget(self.album_page)
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.layout(layout)
        self.stack.setCurrentWidget(self.landing)

    def show_song(self):
        self.stack.setCurrentWidget(self.song_page)
        
    def show_album(self):
        self.stack.setCurrentWidget(self.album_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())