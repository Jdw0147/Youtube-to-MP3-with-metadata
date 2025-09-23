import os
import sys
from PySide6.QtWidgets import (
    QApplication,   # Application object (this manages the event loop)
    QWidget,  # Base class for all UI objects
    QLineEdit,  # Single line text inputs ex.) Title & Artist
    QTextEdit,  # Multi line text input ex.) Lyrics
    QPushButton,    # Clickable button
    QLabel, # Text display label
    QFileDialog,    #File/folder selection windows (for output path and album art path)
    QVBoxLayout,    # Vertical stacking layout manager
    QHBoxLayout,    # Horizontal stacking layout manager
    QFormLayout,    # Layout manager for forms (label + input field)
    QMessageBox    # Popup boxes (errors, success messages, etc)
)
from PySide6.QtCore import Qt
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata

class YoutubeMp3Window(QWidget):
    """
    Main window for the YouTube → MP3 converter app using PySide6 (Qt).
    In Qt, every visible window is a QWidget (or subclass of QWidget).
    """

    def __init__(self):
        super().__init__()  # Initializing the base (parent) QWidget class
        self.setWindowTitle("Convert Youtube to MP3")   # Setting window title

        #=============
        # INPUT FIELDS
        #=============
        # Remember QLineEdit is single line input, QTextEdit is multi-line input
        # Defining as a dictionary so we can loop over it, creating the form easily
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

        # QFormLayout creates a neat two columned layout with labels and fields on the left and right respectively
        # Right side of top section
        top_right_form = QFormLayout()
        top_right_form.addRow("YouTube URL:", self.fields["YouTube URL"])
        top_right_form.addRow("Title:", self.fields["Title"])
        top_right_form.addRow("Artist:", self.fields["Artist"])
        top_right_form.addRow("Album:", self.fields["Album"])

        #Top Section Layout
        top_layout = QHBoxLayout()
        top_layout.addLayout(cover_layout, stretch=1)
        top_layout.addLayout(top_right_form, stretch=2)

        # Middle section under album art
        year_genre_layout = QFormLayout()
        year_genre_layout.addRow("Year:", self.fields["Year"])
        year_genre_layout.addRow("Genre:", self.fields["Genre"])

        album_track_layout = QFormLayout()
        album_track_layout.addRow("Album Artist:", self.fields["Album Artist"])
        album_track_layout.addRow("Track #:", self.fields["Track Number"])

        middle_layout = QHBoxLayout()
        middle_layout.addLayout(year_genre_layout)
        middle_layout.addLayout(album_track_layout)

        # Lyrics section
        lyrics_layout = QFormLayout()
        lyrics_layout.addRow("Lyrics:", self.fields["Lyrics"])

        # Main Layout
        main_layout = QVBoxLayout()
        # album art + basic fields
        main_layout.addLayout(top_layout)
        # Year/Genre + Album Artist/Track
        main_layout.addLayout(middle_layout)
        # Lyrics box
        main_layout.addLayout(lyrics_layout)
        main_layout.addWidget(self.download_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        
        #====================
        # COVER ART SELECTION
        #====================
        # Visual setup
        self.cover_art_label = QLabel("No Image")
        self.cover_art_label.setFixedSize(150, 150) 
        self.cover_art_label.setAlignment(Qt.AlignCenter)
        # Setting object name for styling in style.qss
        self.cover_art_label.setObjectName("CoverArtLabel")
        
        # Logic Setup
        cover_btn = QPushButton("Choose")
        cover_btn.clicked.connect(self.select_cover_art) # The Signal/Slot mechanism in Qt

        # Arranging the forms in the layout
        cover_layout = QVBoxLayout() #'QVBoxLayout' for vertical layout
        cover_layout.addWidget(self.cover_art_label, alignment=Qt.AlignCenter)
        cover_layout.addWidget(cover_btn, alignment=Qt.AlignCenter)
        form_layout.addRow(QLabel("Cover Art: "), cover_layout)

        #======================
        # OUTPUT PATH SELECTION
        #======================
        self.output_path = QLineEdit()
        output_btn=QPushButton("Browse")
        output_btn.clicked.connect(self.select_output_path) 

        output_layout =QHBoxLayout()
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_btn)
        form_layout.addRow(QLabel("File Destination: "), output_layout)

        #================
        # OUTPUT FILENAME
        #================
        self.output_filename = QLineEdit()
        form_layout.addRow(QLabel("Filename (No Extension):"), self.output_filename)
        
        #================
        # DOWNLOAD BUTTON
        #================
        self.download_btn = QPushButton("Convert and Download")
        self.download_btn.clicked.connect(self.process) # Process is our main method

        #====================
        # MAIN LAYOUT OF PAGE
        #====================
        layout = QVBoxLayout() #'QV' for vertical layout    
        layout.addLayout(form_layout) # Adding the form layout we created above
        layout.addWidget(self.download_btn, alignment=Qt.AlignCenter) # Centering the button
        self.setLayout(layout) # Setting the main layout of the window

        
    #=======
    #DIALOGS
    #=======

    # Album Art
    def select_cover_art(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cover Art",
            "",
            "Images (*.jpg *.jpeg)"
        )
        if path:
            self.cover_art_path.setText(path)

    # Output Path
    def select_output_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if path:
            self.output_path.setText(path)

    #============
    # MAIN METHOD
    #============
    def process(self):
        try:
            # Validating youtube url
            yt_url = self.fields["YouTube URL"].text().strip()
            if not yt_url:
                raise ValueError("Please Enter a YouTube URL")
                
            # Collecting fields
            metadata = {
            "title": self.fields["Title"].text(),
            "artist": self.fields["Artist"].text(),
            "album": self.fields["Album"].text(),
            "album_artist": self.fields["Album Artist"].text(),
            "year": self.fields["Year"].text(),
            "genre": self.fields["Genre"].text(),
            "track_number": self.fields["Track Number"].text(),
            "lyrics": self.fields["Lyrics"].toPlainText().strip(),
            "cover_art_path": self.cover_art_path.text(),
            }

            # Validating output folder and filename
            output_path = self.output_path.text()
            if not output_path:
                raise ValueError("Please select a destination folder")
                
            filename = self.output_filename.text().strip()
            if not filename:
                raise ValueError("Please enter a file")
                
            output_mp3_path = os.path.join(output_path, f"{filename}.mp3")

            # Backend stuff
            QMessageBox.information(self, "Processing", "Downloading audio from YouTube...")
                                        
            # Downloading youtube audio
            download_youtube_audio(yt_url)

            # Convert to mp3
            to_mp3("temp.m4a", output_mp3_path)

            # Adding metadata
            add_metadata(output_mp3_path, metadata)

            # Cleanup
            if os.path.exists("temp.m4a"):
                os.remove("temp.m4a")

            # Success message
            QMessageBox.information(self, "Success", f"MP3 file saved to:\n{output_mp3_path}")

        except Exception as e:
            # If anything fails, show error popup
            QMessageBox.critical(self, "Error", str(e))


#============
# ENTRY POINT
#============

# QApplication is required for any Qt app. It manages the event loop.
# sys.argv passes command-line arguments to Qt (not usually needed here).
if __name__ == "__main__":
    app = QApplication(sys.argv)   # Create app object
    window = YoutubeMp3Window()    # Create main window
    window.show()                  # Show the window
    sys.exit(app.exec())           # Start event loop (blocks until window closes)
