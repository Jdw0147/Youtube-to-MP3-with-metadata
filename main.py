import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget,
    QHBoxLayout, QFrame, QSizePolicy
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

        h_layout = QHBoxLayout()

        song_layout = QVBoxLayout()
        btn_song = QPushButton()
        btn_song.setFixedSize(80, 80)
        btn_song.setText("🎵")
        btn_song.setStyleSheet("font-size: 32px;")
        btn_song.clicked.connect(switch_to_song)
        song_label = QLabel("Convert a single song with full metadata control.")
        song_label.setWordWrap(True)
        song_label.setAlignment(Qt.AlignCenter)
        song_layout.addWidget(btn_song, alignment=Qt.AlignCenter)
        song_layout.addWidget(song_label)

        # Album button and description
        album_layout = QVBoxLayout()
        btn_album = QPushButton()
        btn_album.setFixedSize(80, 80)
        btn_album.setText("💿")
        btn_album.setStyleSheet("font-size: 32px;")
        btn_album.clicked.connect(switch_to_album)
        album_label = QLabel(
            "Import multiple songs individually or from a YouTube playlist, "
            "entering album info just once."
        )
        album_label.setWordWrap(True)
        album_label.setAlignment(Qt.AlignCenter)
        album_layout.addWidget(btn_album, alignment=Qt.AlignCenter)
        album_layout.addWidget(album_label)

        # Add layouts to horizontal layout
        h_layout.addLayout(song_layout)
        # Vertical line separator
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        h_layout.addWidget(vline)
        h_layout.addLayout(album_layout)

        layout.addSpacing(20)
        layout.addLayout(h_layout)
        layout.addSpacing(20)

        self.setLayout(layout)

class AlbumPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)  # <-- use go_back here
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        label = QLabel("Convert an Album/Playlist")
        label.setAlignment(Qt.AlignCenter)
        btn_playlist = QPushButton("Export from Youtube Playlist")
        btn_manual = QPushButton("Enter songs manually")
        layout.addWidget(label)
        layout.addWidget(btn_playlist)
        layout.addWidget(btn_manual)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to MP3 Converter")
        self.stack = QStackedWidget()
        self.landing = LandingPage(self.show_song, self.show_album)
        self.song_page = YoutubeMp3Window()
        self.album_page = AlbumPage(self.show_landing)
        self.stack.addWidget(self.landing)
        self.stack.addWidget(self.song_page)
        self.stack.addWidget(self.album_page)
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.stack.setCurrentWidget(self.landing)

    def add_back_button_to_song_page(self):
        # Insert a back button at the top of the song page
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(self.show_landing)
        # Insert at the top of the layout
        if hasattr(self.song_page, 'layout'):
            main_layout = self.song_page.layout()
            if main_layout is not None:
                main_layout.insertWidget(0, back_btn, alignment=Qt.AlignLeft)

    def show_song(self):
        self.stack.setCurrentWidget(self.song_page)
        
    def show_album(self):
        self.stack.setCurrentWidget(self.album_page)

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
    window.show()
    sys.exit(app.exec())