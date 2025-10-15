from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from yt_dlp import YoutubeDL

class ImportPlaylist(QWidget):
    def __init__(self, go_back, on_import):
        super().__init__()
        self.go_back = go_back
        self.on_import = on_import  # Callback to pass video list to main album page
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 16, 24, 16)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Playlist URL input
        url_layout = QHBoxLayout()
        self.url_field = QLineEdit()
        self.url_field.setPlaceholderText("Paste YouTube playlist URL here...")
        url_layout.addWidget(QLabel("Playlist URL:"))
        url_layout.addWidget(self.url_field)
        layout.addLayout(url_layout)

        # Fetch button
        fetch_btn = QPushButton("Fetch Playlist")
        fetch_btn.clicked.connect(self.fetch_playlist)
        layout.addWidget(fetch_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def fetch_playlist(self):
        url = self.url_field.text().strip()
        if not url:
            QMessageBox.warning(self, "No URL", "Please enter a playlist URL.")
            return
        try:
            ydl_opts = {'extract_flat': True, 'quiet': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                entries = info.get('entries', [])
                if not entries:
                    raise Exception("No videos found in playlist.")
                videos = [
                    {
                        'title': entry.get('title', f"Track {i+1}"),
                        'url': f"https://www.youtube.com/watch?v={entry['id']}"
                    }
                    for i, entry in enumerate(entries) if 'id' in entry
                ]
            self.on_import(videos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch playlist:\n{e}")