from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel
from PySide6.QtCore import Qt
from ManualEntry import ManualEntry

class AlbumPage(QWidget):
   def __init__(self, go_back, show_manual_entry):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(32)
        layout.setContentsMargins(32, 32, 32, 32)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Title
        label = QLabel("How would you like to add songs to your album?")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)

        # Horizontal layout for options
        h_layout = QHBoxLayout()
        h_layout.setSpacing(60)

        # Manual Entry option
        manual_layout = QVBoxLayout()
        btn_manual = QPushButton("📝")
        btn_manual.setFixedSize(140, 140)
        btn_manual.setStyleSheet("font-size: 64px;")
        btn_manual.clicked.connect(show_manual_entry)
        manual_label = QLabel(
            "Enter songs manually\n\n"
            "Add each song's YouTube URL, name, artist, and track number individually.\n"
            "Best for custom albums or when you want full control."
        )
        manual_label.setWordWrap(True)
        manual_label.setAlignment(Qt.AlignCenter)
        manual_layout.addWidget(btn_manual, alignment=Qt.AlignCenter)
        manual_layout.addWidget(manual_label, alignment=Qt.AlignCenter)

        # Add layouts to horizontal layout
        h_layout.addStretch(1)
        h_layout.addLayout(manual_layout)
        h_layout.addStretch(1)
        h_layout.addStretch(1)

        layout.addSpacing(20)
        layout.addLayout(h_layout)
        layout.addSpacing(20)

        self.setLayout(layout)