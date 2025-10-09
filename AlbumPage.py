from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class AlbumPage(QWidget):
    def __init__(self, go_back, show_manual_entry, show_playlist_import):
        super().__init__()
        layout = QVBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        label = QLabel("Convert an Album/Playlist")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn_playlist = QPushButton("Export from Youtube Playlist")
        btn_playlist.clicked.connect(show_playlist_import)
        btn_manual = QPushButton("Enter songs manually")
        btn_manual.clicked.connect(show_manual_entry)
        layout.addWidget(btn_playlist)
        layout.addWidget(btn_manual)

        self.setLayout(layout)