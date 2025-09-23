import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton,
    QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata


class YoutubeMp3Window(QWidget):
    """
    Main window for the YouTube → MP3 converter app using PySide6 (Qt).
    Layout:
    - URL input at top (full width)
    - Album art on left, first 4 inputs (Title, Artist, Album, Album Artist) on right
    - Next row (Year + Genre, Track # + Output Filename)
    - Bottom row: Output Folder (left) + Convert Button (right)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convert YouTube to MP3")

        # =========================
        #  FIELD DEFINITIONS
        # =========================
        self.fields = {
            "YouTube URL": QLineEdit(),
            "Title": QLineEdit(),
            "Artist": QLineEdit(),
            "Album": QLineEdit(),
            "Album Artist": QLineEdit(),
            "Year": QLineEdit(),
            "Genre": QLineEdit(),
            "Track Number": QLineEdit(),
            "Lyrics": QTextEdit(),
        }

        # Output filename (special field)
        self.output_filename = QLineEdit()

        # Output path (special field)
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Choose save folder...")

        # =========================
        #  TOP: URL INPUT
        # =========================
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("YouTube URL:"))
        url_layout.addWidget(self.fields["YouTube URL"])

        # =========================
        #  ALBUM ART (LEFT SIDE)
        # =========================
        self.cover_art_label = QLabel("No Image")
        self.cover_art_label.setFixedSize(150, 150)
        self.cover_art_label.setAlignment(Qt.AlignCenter)
        self.cover_art_label.setObjectName("CoverArtLabel")

        cover_btn = QPushButton("Choose")
        cover_btn.clicked.connect(self.select_cover_art)

        cover_layout = QVBoxLayout()
        cover_layout.addWidget(self.cover_art_label, alignment=Qt.AlignCenter)
        cover_layout.addWidget(cover_btn, alignment=Qt.AlignCenter)

        # =========================
        #  FIRST 4 INPUTS (RIGHT OF ART)
        # =========================
        right_top_form = QFormLayout()
        right_top_form.addRow("Title:", self.fields["Title"])
        right_top_form.addRow("Artist:", self.fields["Artist"])
        right_top_form.addRow("Album:", self.fields["Album"])
        right_top_form.addRow("Album Artist:", self.fields["Album Artist"])

        # Combine cover art + first 4 inputs
        top_layout = QHBoxLayout()
        top_layout.addLayout(cover_layout, stretch=1)
        top_layout.addLayout(right_top_form, stretch=2)

        # =========================
        #  NEXT ROW (Year/Genre + Track#/Filename)
        # =========================
        middle_layout = QHBoxLayout()

        left_form = QFormLayout()
        left_form.addRow("Year:", self.fields["Year"])
        left_form.addRow("Genre:", self.fields["Genre"])

        right_form = QFormLayout()
        right_form.addRow("Track #:", self.fields["Track Number"])
        right_form.addRow("Filename:", self.output_filename)

        middle_layout.addLayout(left_form)
        middle_layout.addLayout(right_form)

        # =========================
        #  LYRICS BOX (FULL WIDTH)
        # =========================
        lyrics_layout = QFormLayout()
        lyrics_layout.addRow("Lyrics:", self.fields["Lyrics"])

        # =========================
        #  BOTTOM ROW (Output path + Convert button)
        # =========================
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.output_path)

        output_btn = QPushButton("Browse")
        output_btn.clicked.connect(self.select_output_path)
        bottom_layout.addWidget(output_btn)

        self.download_btn = QPushButton("Convert and Download")
        self.download_btn.clicked.connect(self.process)
        bottom_layout.addWidget(self.download_btn)

        # =========================
        #  MAIN LAYOUT
        # =========================
        main_layout = QVBoxLayout()
        main_layout.addLayout(url_layout)      # Top URL row
        main_layout.addLayout(top_layout)      # Album art + first 4 inputs
        main_layout.addLayout(middle_layout)   # Year/Genre + Track#/Filename
        main_layout.addLayout(lyrics_layout)   # Lyrics field
        main_layout.addLayout(bottom_layout)   # Output path + convert button

        self.setLayout(main_layout)

    # =========================
    #  FILE DIALOGS
    # =========================
    def select_cover_art(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Cover Art", "", "Images (*.jpg *.jpeg *.png)"
        )
        if path:
            # Display the image
            pixmap = QPixmap(path)
            scaled_pixmap = pixmap.scaled(
                self.cover_art_label.width(),
                self.cover_art_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.cover_art_label.setPixmap(scaled_pixmap)
            self.cover_art_label.setText("")  # clear placeholder text
            # Save for metadata use
            self.cover_art_path = path

    def select_output_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if path:
            self.output_path.setText(path)

    # =========================
    #  MAIN PROCESS
    # =========================
    def process(self):
        try:
            yt_url = self.fields["YouTube URL"].text().strip()
            if not yt_url:
                raise ValueError("Please enter a YouTube URL")

            metadata = {
                "title": self.fields["Title"].text(),
                "artist": self.fields["Artist"].text(),
                "album": self.fields["Album"].text(),
                "album_artist": self.fields["Album Artist"].text(),
                "year": self.fields["Year"].text(),
                "genre": self.fields["Genre"].text(),
                "track_number": self.fields["Track Number"].text(),
                "lyrics": self.fields["Lyrics"].toPlainText().strip(),
                "cover_art_path": getattr(self, "cover_art_path", ""),  # safe
            }

            output_path = self.output_path.text()
            if not output_path:
                raise ValueError("Please select a destination folder")

            filename = self.output_filename.text().strip()
            if not filename:
                raise ValueError("Please enter a filename")

            output_mp3_path = os.path.join(output_path, f"{filename}.mp3")

            # Backend process
            QMessageBox.information(self, "Processing", "Downloading audio from YouTube...")
            download_youtube_audio(yt_url)
            to_mp3("temp.m4a", output_mp3_path)
            add_metadata(output_mp3_path, metadata)

            if os.path.exists("temp.m4a"):
                os.remove("temp.m4a")

            QMessageBox.information(self, "Success", f"MP3 file saved to:\n{output_mp3_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# =========================
#  ENTRY POINT
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YoutubeMp3Window()
    window.show()
    sys.exit(app.exec())
