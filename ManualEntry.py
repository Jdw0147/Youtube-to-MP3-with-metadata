from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QMessageBox, QScrollArea, QGridLayout, QGroupBox
)
import os
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata
import re

def safe_filename(name):
    # Remove invalid filename characters for Windows
    return re.sub(r'[\\/*?:"<>|]', "", name).strip() or "untitled"

class SongEntry(QGroupBox):
    def __init__(self, song_number, remove_callback):
        super().__init__(f"Song {song_number}")
        self.remove_callback = remove_callback
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 8, 12, 8)

        url_row = QHBoxLayout()
        self.song_url = QLineEdit()
        self.song_url.setPlaceholderText("Song URL")
        self.song_url.setMinimumWidth(220)
        url_row.addWidget(QLabel("Song URL:"))
        url_row.addWidget(self.song_url, stretch=2)

        self.track_number = QLineEdit()
        self.track_number.setPlaceholderText("Track #")
        self.track_number.setFixedWidth(60)
        url_row.addWidget(QLabel("Track #:"))
        url_row.addWidget(self.track_number)

        layout.addLayout(url_row)

        # Second row: Song Name and Song Artist
        name_row = QHBoxLayout()
        self.song_name = QLineEdit()
        self.song_name.setPlaceholderText("Song Name")
        self.song_name.setMinimumWidth(180)
        name_row.addWidget(QLabel("Song Name:"))
        name_row.addWidget(self.song_name, stretch=2)

        self.song_artist = QLineEdit()
        self.song_artist.setPlaceholderText("Artist (leave blank to use Album Artist)")
        self.song_artist.setMinimumWidth(120)
        self.song_artist.setMaximumWidth(180)
        name_row.addWidget(QLabel("Song Artist:"))
        name_row.addWidget(self.song_artist, stretch=1)

        layout.addLayout(name_row)
        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_self)
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
        self.output_folder = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 16, 24, 16)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # --- Top: Album Art + Album Info ---
        top_layout = QHBoxLayout()

        # Album Art
        art_layout = QVBoxLayout()
        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(200, 200)
        self.album_art_label.setStyleSheet(
            "border: 2px dashed #888;"
            "background: #eee;"
            "border-radius: 16px;"
        )
        self.album_art_label.setAlignment(Qt.AlignCenter)
        self.album_art_label.setText("No Art")
        art_btn = QPushButton("Choose Art")
        art_btn.clicked.connect(self.choose_album_art)
        art_layout.addWidget(self.album_art_label, alignment=Qt.AlignCenter)
        art_layout.addWidget(art_btn, alignment=Qt.AlignCenter)
        top_layout.addLayout(art_layout)

        self.album_name = QLineEdit()
        self.album_name.setPlaceholderText("Album Name")
        self.album_artist = QLineEdit()
        self.album_artist.setPlaceholderText("Album Artist")
        self.album_year = QLineEdit()
        self.album_year.setPlaceholderText("Year")
        self.album_genre = QLineEdit()
        self.album_genre.setPlaceholderText("Genre")

        # Album Info Fields (2 columns)
        info_layout = QGridLayout()
        info_layout.setHorizontalSpacing(12)
        info_layout.setVerticalSpacing(8)
        self.album_name = QLineEdit()
        self.album_artist = QLineEdit()
        self.album_year = QLineEdit()
        self.album_genre = QLineEdit()
        self.album_name.setPlaceholderText("Album Name")
        self.album_artist.setPlaceholderText("Album Artist")
        self.album_year.setPlaceholderText("Year")
        self.album_genre.setPlaceholderText("Genre")

        info_layout.addWidget(QLabel("Album Name:"), 0, 0)
        info_layout.addWidget(self.album_name, 0, 1)
        info_layout.addWidget(QLabel("Album Artist:"), 1, 0)
        info_layout.addWidget(self.album_artist, 1, 1)
        info_layout.addWidget(QLabel("Year:"), 2, 0)
        info_layout.addWidget(self.album_year, 2, 1)
        info_layout.addWidget(QLabel("Genre:"), 3, 0)
        info_layout.addWidget(self.album_genre, 3, 1)

        top_layout.addLayout(info_layout)
        main_layout.addLayout(top_layout)

        # Info label about song artist fallback
        info_label = QLabel("Tip: If a song's Artist is left blank, the Album Artist will be used.")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        main_layout.addWidget(info_label)

        # Songs section (scrollable)
        songs_box = QGroupBox("Songs")
        songs_box_layout = QVBoxLayout()
        self.songs_area = QScrollArea()
        self.songs_area.setWidgetResizable(True)
        self.songs_area.setMinimumHeight(350)
        self.songs_widget = QWidget()
        self.songs_widget.setStyleSheet("background: white;")
        self.songs_layout = QVBoxLayout()
        self.songs_widget.setLayout(self.songs_layout)
        self.songs_area.setWidget(self.songs_widget)
        songs_box_layout.addWidget(self.songs_area)
        songs_box.setLayout(songs_box_layout)
        main_layout.addWidget(songs_box)

        dest_layout = QHBoxLayout()
        self.dest_label = QLabel("Download Destination: Not selected")
        select_dest_btn = QPushButton("Choose Folder")
        select_dest_btn.clicked.connect(self.select_output_folder)
        dest_layout.addWidget(self.dest_label)
        dest_layout.addWidget(select_dest_btn)
        main_layout.addLayout(dest_layout)

        # Add Song button
        add_song_btn = QPushButton("Add Song")
        add_song_btn.clicked.connect(self.add_song_entry)
        main_layout.addWidget(add_song_btn)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_album)
        main_layout.addWidget(submit_btn, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

        # Add the first song entry by default
        self.add_song_entry()

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.dest_label.setText(f"Download Destination: {folder}")
        else:
            self.output_folder = None
            self.dest_label.setText("Download Destination: Not selected")

    def choose_album_art(self):
        valid_exts = (".jpg", ".jpeg", ".png")
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Album Art",
            "",
            "Images (*.jpg *.jpeg *.png *.heic *.webp *.bmp *.tiff *.gif)"
        )
        if not path:
            return

        ext = path.lower().rsplit(".", 1)[-1]
        ext = f".{ext}"
        if ext not in valid_exts:
            msg = QMessageBox(self)
            msg.setWindowTitle("Invalid Image Type")
            msg.setText("This image is not of valid type.\nWould you like to convert it to a valid type?")
            png_btn = msg.addButton("Yes, to PNG", QMessageBox.AcceptRole)
            jpg_btn = msg.addButton("Yes, to JPG", QMessageBox.AcceptRole)
            no_btn = msg.addButton("No", QMessageBox.RejectRole)
            msg.setIcon(QMessageBox.Question)
            msg.exec()

            if msg.clickedButton() == no_btn:
                return

            out_ext = ".png" if msg.clickedButton() == png_btn else ".jpg"
            out_path = path.rsplit(".", 1)[0] + "_converted" + out_ext

            try:
                img = Image.open(path)
                if out_ext == ".jpg" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(out_path)
                path = out_path
            except Exception as e:
                QMessageBox.critical(self, "Conversion Error", f"Could not convert image:\n{e}")
                return

        pixmap = QPixmap(path)
        scaled = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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

    def get_album_data(self):
        """Collect all album and song info as a dictionary."""
        album_data = {
            "album_art": getattr(self, "album_art_path", None),
            "album_name": self.album_name.text().strip(),
            "album_artist": self.album_artist.text().strip(),
            "album_year": self.album_year.text().strip(),
            "album_genre": self.album_genre.text().strip(),
            "songs": []
        }
        album_artist = album_data["album_artist"]
        for entry in self.song_entries:
            song_name = entry.song_name.text().strip()
            song_artist = entry.song_artist.text().strip() or album_artist
            track_number = entry.track_number.text().strip()
            song_url = entry.song_url.text().strip()
            album_data["songs"].append({
                "song_name": song_name,
                "song_artist": song_artist,
                "track_number": track_number,
                "song_url": song_url
            })
        return album_data
    
    def submit_album(self):
        album_data = self.get_album_data()
        if not album_data["album_name"] or not album_data["songs"]:
            QMessageBox.warning(self, "Missing Info", "Please enter an album name and at least one song.")
            return

        if not self.output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please select a download destination folder before submitting.")
            return
        
        confirm = QMessageBox.question(
            self,
            "Confirm Submission",
            "Are you sure you want to submit?\nThis will download and tag all songs.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        errors = []
        for song in album_data["songs"]:
            try:
                # 1. Download audio
                audio_path = download_youtube_audio(song["song_url"], self.output_folder)
                filename = safe_filename(song.get("filename", "") or song["song_name"])
                mp3_path = os.path.join(self.output_folder, f"{filename}.mp3")
                # 2. Convert to mp3 (only once, with both input and output)
                to_mp3(audio_path, mp3_path)
                # 3. Add metadata
                add_metadata(
                    mp3_path,
                    {
                        "title": song["song_name"],
                        "artist": song["song_artist"],
                        "album": album_data["album_name"],
                        "album_artist": album_data["album_artist"],
                        "year": album_data["album_year"],
                        "genre": album_data["album_genre"],
                        "track_number": song["track_number"],
                        "cover_art_path": album_data["album_art"],
                    }
                )
            except Exception as e:
                errors.append(f"{song['song_name']}: {e}")

        if errors:
            QMessageBox.warning(self, "Some Errors Occurred", "\n".join(errors))
        else:
            QMessageBox.information(self, "Success", "All songs downloaded and tagged!")