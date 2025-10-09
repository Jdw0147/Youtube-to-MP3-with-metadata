from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QScrollArea, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class AlbumPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn, alignment=0)
        label = QLabel("Convert an Album/Playlist")
        label.setAlignment(0x84)  # Qt.AlignCenter
        btn_playlist = QPushButton("Export from Youtube Playlist")
        btn_manual = QPushButton("Enter songs manually")
        layout.addWidget(label)
        layout.addWidget(btn_playlist)
        layout.addWidget(btn_manual)
        self.setLayout(layout)