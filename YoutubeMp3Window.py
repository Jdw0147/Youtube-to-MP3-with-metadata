import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata


class YoutubeMp3Window(QWidget):
    """
    Main window for the YouTube → MP3 converter app using PySide6 (Qt).
    Handles all UI logic (layouts, album art preview, dialogs).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convert YouTube to MP3")

        # =========
        # VARIABLES
        # =========
        self.cover_art_path = ""  # Will hold string path to image file

        # ===========
        # MAIN FIELDS
        # ===========
        self.url_field = QLineEdit()
        self.url_field.setPlaceholderText("Enter YouTube URL...")

        self.title_field = QLineEdit()
        self.artist_field = QLineEdit()
        self.album_field = QLineEdit()
        self.album_artist_field = QLineEdit()

        self.year_field = QLineEdit()
        self.genre_field = QLineEdit()
        self.track_field = QLineEdit()
        self.output_filename = QLineEdit()

        self.lyrics_field = QTextEdit()
        self.lyrics_field.setPlaceholderText("Enter lyrics here...")

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Choose save folder...")

        # ============
        # COVER ART UI
        # ============
        self.cover_art_label = QLabel("No Image")
        self.cover_art_label.setFixedSize(150, 150)
        self.cover_art_label.setAlignment(Qt.AlignCenter)
        self.cover_art_label.setObjectName("CoverArtLabel")

        cover_btn = QPushButton("Choose")
        cover_btn.clicked.connect(self.select_cover_art)

        cover_layout = QVBoxLayout()
        cover_layout.addWidget(self.cover_art_label, alignment=Qt.AlignCenter)
        cover_layout.addWidget(cover_btn, alignment=Qt.AlignCenter)

        # ====================
        # TOP SECTION (URL row)
        # ====================
        top_url_layout = QHBoxLayout()
        top_url_layout.addWidget(QLabel("YouTube URL:"))
        top_url_layout.addWidget(self.url_field)

        # =====================
        # TOP SECTION (cover + 4 fields)
        # =====================
        fields_form = QFormLayout()
        fields_form.addRow("Title:", self.title_field)
        fields_form.addRow("Artist:", self.artist_field)
        fields_form.addRow("Album:", self.album_field)
        fields_form.addRow("Album Artist:", self.album_artist_field)

        top_layout = QHBoxLayout()
        top_layout.addLayout(cover_layout, stretch=1)
        top_layout.addLayout(fields_form, stretch=2)

        # ======================
        # MIDDLE SECTION (2x2)
        # ======================
        mid_form_left = QFormLayout()
        mid_form_left.addRow("Year:", self.year_field)
        mid_form_left.addRow("Genre:", self.genre_field)

        mid_form_right = QFormLayout()
        mid_form_right.addRow("Track #:", self.track_field)
        mid_form_right.addRow("Filename:", self.output_filename)

        middle_layout = QHBoxLayout()
        middle_layout.addLayout(mid_form_left)
        middle_layout.addLayout(mid_form_right)

        # ============
        # LYRICS BOX
        # ============
        lyrics_layout = QFormLayout()
        lyrics_layout.addRow("Lyrics:", self.lyrics_field)

        # =======================
        # BOTTOM (path + download)
        # =======================
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Save To:"))
        bottom_layout.addWidget(self.output_path)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_output_path)
        bottom_layout.addWidget(browse_btn)

        self.download_btn = QPushButton("Convert and Download")
        self.download_btn.setFixedHeight(40)
        self.download_btn.clicked.connect(self.process)
        bottom_layout.addWidget(self.download_btn)

        # =========
        # MAIN LAYOUT
        # =========
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_url_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(lyrics_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    # ============================
    # COVER ART (dialog + preview)
    # ============================
    def select_cover_art(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cover Art",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )
        if path:
            self.cover_art_path = path
            pixmap = QPixmap(path)
            scaled_pixmap = pixmap.scaled(
                self.cover_art_label.width(),
                self.cover_art_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.cover_art_label.setPixmap(scaled_pixmap)

    # ==========================
    # OUTPUT FOLDER DIALOG
    # ==========================
    def select_output_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if path:
            self.output_path.setText(path)

    # ==========================
    # MAIN PROCESSING LOGIC
    # ==========================
    def process(self):
        try:
            yt_url = self.url_field.text().strip()
            if not yt_url:
                raise ValueError("Please enter a YouTube URL")

            metadata = {
                "title": self.title_field.text(),
                "artist": self.artist_field.text(),
                "album": self.album_field.text(),
                "album_artist": self.album_artist_field.text(),
                "year": self.year_field.text(),
                "genre": self.genre_field.text(),
                "track_number": self.track_field.text(),
                "lyrics": self.lyrics_field.toPlainText().strip(),
                "cover_art_path": self.cover_art_path,
            }

            output_path = self.output_path.text()
            if not output_path:
                raise ValueError("Please select a destination folder")

            filename = self.output_filename.text().strip()
            if not filename:
                raise ValueError("Please enter an output filename")

            output_mp3_path = os.path.join(output_path, f"{filename}.mp3")

            # Processing
            QMessageBox.information(self, "Processing", "Downloading audio from YouTube...")
            download_youtube_audio(yt_url)
            to_mp3("temp.m4a", output_mp3_path)
            add_metadata(output_mp3_path, metadata)

            if os.path.exists("temp.m4a"):
                os.remove("temp.m4a")

            QMessageBox.information(self, "Success", f"MP3 file saved to:\n{output_mp3_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ============
# ENTRY POINT
# ============
if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = YoutubeMp3Window()

    window.download_btn.setObjectName("DownloadBtn")
    
    window.show()
    sys.exit(app.exec())
