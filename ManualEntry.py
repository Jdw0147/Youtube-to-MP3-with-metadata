from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QScrollArea, QGroupBox
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

    def set_number(self, n):
        self.setTitle(f"Song {n}")

class ManualEntry(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.song_entries = []
        main_layout = QVBoxLayout()

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Album Info section
        album_info_box = QGroupBox("Album Information")
        album_layout = QVBoxLayout()

        # Album Art
        art_layout = QHBoxLayout()
        self.album_art_label = QLabel("No Art")
        self.album_art_label.setFixedSize(80, 80)
        self.album_art_label.setStyleSheet("border: 1px solid black;")
        art_btn = QPushButton("Choose Art")
        art_btn.clicked.connect(self.choose_album_art)
        art_layout.addWidget(self.album_art_label)
        art_layout.addWidget(art_btn)
        album_layout.addLayout(art_layout)

        self.album_name = QLineEdit()
        self.album_name.setPlaceholderText("Album Name")
        self.album_artist = QLineEdit()
        self.album_artist.setPlaceholderText("Album Artist")
        self.album_year = QLineEdit()
        self.album_year.setPlaceholderText("Year")
        self.album_genre = QLineEdit()
        self.album_genre.setPlaceholderText("Genre")

        album_layout.addWidget(QLabel("Album Name:"))
        album_layout.addWidget(self.album_name)
        album_layout.addWidget(QLabel("Album Artist:"))
        album_layout.addWidget(self.album_artist)
        album_layout.addWidget(QLabel("Year:"))
        album_layout.addWidget(self.album_year)
        album_layout.addWidget(QLabel("Genre:"))
        album_layout.addWidget(self.album_genre)

        album_info_box.setLayout(album_layout)
        main_layout.addWidget(album_info_box)

        # Songs section (scrollable)
        self.songs_area = QScrollArea()
        self.songs_area.setWidgetResizable(True)
        self.songs_widget = QWidget()
        self.songs_layout = QVBoxLayout()
        self.songs_widget.setLayout(self.songs_layout)
        self.songs_area.setWidget(self.songs_widget)
        main_layout.addWidget(QLabel("Songs:"))
        main_layout.addWidget(self.songs_area, stretch=1)

        # Add Song button
        add_song_btn = QPushButton("Add Song")
        add_song_btn.clicked.connect(self.add_song_entry)
        main_layout.addWidget(add_song_btn)

        self.setLayout(main_layout)

        # Add the first song entry by default
        self.add_song_entry()

    def choose_album_art(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Album Art", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if path:
            pixmap = QPixmap(path)
            scaled = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.album_art_label.setPixmap(scaled)
            self.album_art_label.setText("")  # Clear "No Art"
            self.album_art_path = path

    def add_song_entry(self):
        song_number = len(self.song_entries) + 1
        entry = SongEntry(song_number, self.remove_song_entry)
        self.song_entries.append(entry)
        self.songs_layout.addWidget(entry)

    def remove_song_entry(self, entry):
        self.songs_layout.removeWidget(entry)
        entry.deleteLater()
        self.song_entries.remove(entry)
        # Re-number remaining songs
        for idx, song in enumerate(self.song_entries, 1):
            song.set_number(idx)