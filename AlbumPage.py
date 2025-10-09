from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel
from PySide6.QtCore import Qt

class AlbumPage(QWidget):
   def __init__(self, go_back, show_manual_entry, show_playlist_import):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(32, 24, 32, 24)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Title
        label = QLabel("How would you like to add songs to your album?")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        # Horizontal layout for options
        h_layout = QHBoxLayout()

        # Manual Entry option
        manual_layout = QVBoxLayout()
        btn_manual = QPushButton("📝")
        btn_manual.setFixedSize(80, 80)
        btn_manual.setStyleSheet("font-size: 36px;")
        btn_manual.clicked.connect(show_manual_entry)
        manual_label = QLabel(
            "Enter songs manually\n\n"
            "Add each song's YouTube URL, name, artist, and track number individually. "
            "Best for custom albums or when you want full control."
        )
        manual_label.setWordWrap(True)
        manual_label.setAlignment(Qt.AlignCenter)
        manual_layout.addWidget(btn_manual, alignment=Qt.AlignCenter)
        manual_layout.addWidget(manual_label)

        # Playlist Import option
        playlist_layout = QVBoxLayout()
        btn_playlist = QPushButton("📋")
        btn_playlist.setFixedSize(80, 80)
        btn_playlist.setStyleSheet("font-size: 36px;")
        btn_playlist.clicked.connect(show_playlist_import)
        playlist_label = QLabel(
            "Import from YouTube Playlist\n\n"
            "Paste a YouTube playlist link and automatically add all songs from that playlist. "
            "Best for quickly importing many songs."
        )
        playlist_label.setWordWrap(True)
        playlist_label.setAlignment(Qt.AlignCenter)
        playlist_layout.addWidget(btn_playlist, alignment=Qt.AlignCenter)
        playlist_layout.addWidget(playlist_label)

        # Add layouts to horizontal layout
        h_layout.addLayout(manual_layout)
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        h_layout.addWidget(vline)
        h_layout.addLayout(playlist_layout)

        layout.addSpacing(20)
        layout.addLayout(h_layout)
        layout.addSpacing(20)

        self.setLayout(layout)