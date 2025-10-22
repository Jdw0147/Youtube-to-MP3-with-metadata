from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QMessageBox, QScrollArea, QGridLayout, QGroupBox, QListWidget
)
import os
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata
import re
import yt_dlp
from search import search_album

def safe_filename(name):
    # Remove invalid filename characters for Windows
    return re.sub(r'[\\/*?:"<>|]', "", name).strip() or "untitled"

class SongEntry(QGroupBox):
    def __init__(self, song_number, remove_callback):
        super().__init__(f"Song {song_number}")
        self.setProperty("songEntry", True)
        self.setStyleSheet("QGroupBox { margin-top: 0px; font-size: 9pt; padding: 0px 0px 0px 0px; border: none; } ")
        self.remove_callback = remove_callback
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(4, 2, 4, 2)

        self.song_url = QLineEdit()
        self.song_url.setPlaceholderText("URL")
        self.song_url.setMinimumWidth(160)
        self.song_url.setMaximumWidth(260)
        url_label = QLabel("URL:")
        url_label.setStyleSheet("font-size: 9pt; color: #888; margin-right: 0px;")
        layout.addWidget(url_label)
        layout.addWidget(self.song_url, stretch=2)

        self.song_name = QLineEdit()
        self.song_name.setPlaceholderText("Name")
        self.song_name.setMinimumWidth(120)
        self.song_name.setMaximumWidth(180)
        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-size: 9pt; color: #888; margin-right: 0px;")
        layout.addWidget(name_label)
        layout.addWidget(self.song_name, stretch=2)

        self.track_number = QLineEdit()
        self.track_number.setPlaceholderText("#")
        self.track_number.setFixedWidth(32)
        track_label = QLabel("#")
        track_label.setStyleSheet("font-size: 9pt; color: #888; margin-right: 0px;")
        layout.addWidget(track_label)
        layout.addWidget(self.track_number)

        # Remove button
        remove_btn = QPushButton("✕")
        remove_btn.setFixedWidth(28)
        remove_btn.setStyleSheet("padding:0px 0px;font-size:10pt;background:#eee;color:#888;border-radius:4px;")
        remove_btn.clicked.connect(self.remove_self)
        layout.addWidget(remove_btn)

        self.setLayout(layout)

    def remove_self(self):
        self.remove_callback(self)

    def set_number(self, n):
        self.setTitle(f"Song {n}")

class ManualEntry(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.song_entries = []
        self.output_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 16, 24, 16)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # --- Album Search Bar ---
        self.album_search_bar = QLineEdit()
        self.album_search_bar.setPlaceholderText("Search for album...")
        self.album_search_results = QListWidget()
        self.album_search_results.setMaximumHeight(120)
        self.album_search_results.hide()
        self.album_search_map = {}

        # Add search bar and results below album info fields
        main_layout.addWidget(self.album_search_bar)
        main_layout.addWidget(self.album_search_results)

        self.album_search_bar.textChanged.connect(self.update_album_search)
        self.album_search_results.itemClicked.connect(self.fill_album_fields_from_search)

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
        info_label = QLabel("Tip: You can paste the link to a youtube playlist to fill out all of the song fields instantly!.")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        main_layout.addWidget(info_label)

        # Playlist URL
        playlist_layout = QHBoxLayout()
        self.playlist_url = QLineEdit()
        self.playlist_url.setPlaceholderText("Playlist URL (If applicable)")
        playlist_layout.addWidget(QLabel("Playlist URL (If applicable):"))
        playlist_layout.addWidget(self.playlist_url)
        load_playlist_btn = QPushButton("Load Playlist")
        load_playlist_btn.clicked.connect(self.load_playlist)
        playlist_layout.addWidget(load_playlist_btn)
        main_layout.addLayout(playlist_layout)

        # Songs section (scrollable)
        songs_box = QGroupBox("Songs")
        songs_box_layout = QVBoxLayout()
        self.songs_area = QScrollArea()
        self.songs_area.setWidgetResizable(True)
        # Removed setMinimumHeight to allow compactness
        self.songs_widget = QWidget()
        self.songs_widget.setStyleSheet("background: white;")
        self.songs_layout = QVBoxLayout()
        self.songs_widget.setLayout(self.songs_layout)
        self.songs_area.setWidget(self.songs_widget)
        songs_box_layout.addWidget(self.songs_area)
        songs_box.setLayout(songs_box_layout)
        main_layout.addWidget(songs_box)

        # Add Song button
        add_song_btn = QPushButton("Add Song")
        add_song_btn.clicked.connect(self.add_song_entry)
        main_layout.addWidget(add_song_btn, alignment=Qt.AlignRight)

        # Download Destination
        dest_layout = QHBoxLayout()
        self.dest_label = QLabel(f"Download Destination: {self.output_folder}")
        select_dest_btn = QPushButton("Choose Folder")
        select_dest_btn.clicked.connect(self.select_output_folder)
        dest_layout.addWidget(self.dest_label)
        dest_layout.addWidget(select_dest_btn)
        main_layout.addLayout(dest_layout)


        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_album)
        main_layout.addWidget(submit_btn, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

        # Add the first song entry by default
        self.add_song_entry()

    def update_album_search(self, text):
        self.album_search_results.clear()
        self.album_search_map.clear()
        if not text.strip():
            self.album_search_results.hide()
            return
        try:
            results = search_album(text)
            if not results:
                self.album_search_results.addItem("No results found")
            else:
                for result in results:
                    display = f"{result['title']} ({result.get('year', '')})"
                    self.album_search_results.addItem(display)
                    self.album_search_map[display] = result
            self.album_search_results.show()
        except Exception:
            self.album_search_results.addItem("No results found")
            self.album_search_results.show()

    def fill_album_fields_from_search(self, item):
        text = item.text()
        if text == "No results found":
            return
        result = self.album_search_map.get(text)
        if not result:
            return

        # Set album name and artist from result
        self.album_name.setText(result.get('title', ''))
        self.album_artist.setText(result.get('artist', ''))

        # Fetch full release data for tracklist, year, genre
        resource_url = result.get('resource_url')
        if resource_url:
            try:
                import requests
                release_data = requests.get(resource_url, params={'token': 'EurItYjbxmcFweNWLKVPinAygglnADxrWDDkxFfc'}).json()
                # Year and genre
                self.album_year.setText(str(release_data.get('year', '')))
                genres = release_data.get('genres', []) or release_data.get('genre', [])
                self.album_genre.setText(', '.join(genres) if genres else '')

                # Remove existing song entries
                for entry in self.song_entries[:]:
                    self.remove_song_entry(entry)

                # Fill song entries from tracklist
                tracklist = release_data.get('tracklist', [])
                for idx, track in enumerate(tracklist, 1):
                    entry = SongEntry(idx, self.remove_song_entry)
                    entry.song_name.setText(track.get('title', ''))
                    entry.track_number.setText(str(idx))
                    self.song_entries.append(entry)
                    self.songs_layout.addWidget(entry)
            except Exception as e:
                print(f"Error fetching release data: {e}")

        # Set album art if available
        cover_url = result.get('cover_image')
        if cover_url:
            self.set_album_art_from_url(cover_url)
        self.album_search_results.hide()

    def set_album_art_from_url(self, url):
        try:
            import requests
            from PySide6.QtGui import QImage
            response = requests.get(url)
            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                self.album_art_label.width(),
                self.album_art_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.album_art_label.setPixmap(scaled_pixmap)
            self.album_art_path = url
        except Exception:
            pass

    def is_youtube_playlist(self, url):
        # Checks to see if URL leads to a youtube playlist
        return "youtube.com/playlist?list=" in url or "youtube.com/watch?v=" in url and "list=" in url
    
    def load_playlist(self):
        url = self.playlist_url.text().strip()
        if not url or not self.is_youtube_playlist(url):
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube playlist URL.")
            return
        
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'skip_download': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' not in info:
                    raise Exception("No videos found in playlist.")
                videos = info['entries']
        except Exception as e:
            QMessageBox.critical(self, "Playlist Error", f"Could not load playlist:\n{e}")
            return
        
        # Remove existing song entries
        for entry in self.song_entries[:]:
            self.remove_song_entry(entry)
        
        # Add entries from playlist
        for idk, video in enumerate(videos, 1):
            entry = SongEntry(idk, self.remove_song_entry)
            entry.song_url.setText(f"https://www.youtube.com/watch?v={video['id']}")
            entry.song_name.setText(video.get('title', ''))
            entry.track_number.setText(str(idk))
            self.song_entries.append(entry)
            self.songs_layout.addWidget(entry)

        QMessageBox.information(self, "Playlist Loaded", f"Loaded {len(videos)} songs from playlist.")


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
            song_artist = album_artist
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
                print("Downloaded file path:", audio_path)
                print("File exists?", os.path.exists(audio_path))
                # If file does not exist, try .m4a extension
                if not os.path.exists(audio_path):
                    alt_path = os.path.splitext(audio_path)[0] + ".m4a"
                    print("Trying alternate path:", alt_path)
                    if os.path.exists(alt_path):
                        audio_path = alt_path
                    else:
                        raise FileNotFoundError(f"Neither {audio_path} nor {alt_path} exist!")

                filename = safe_filename(song.get("filename", "") or song["song_name"])
                mp3_path = os.path.join(self.output_folder, f"{filename}.mp3")

                # 2. Convert to mp3 (only once, with both input and output)
                to_mp3(audio_path, mp3_path)

                # 3. Cleanup
                if os.path.exists(audio_path):
                    try:
                        os.remove(audio_path)
                    except Exception as cleanup_err:
                        print(f"Could not remove temp file {audio_path}: {cleanup_err}")
                        

                # 4. Add metadata (make lyrics optional)
                metadata = {
                    "title": song["song_name"],
                    "artist": song["song_artist"],
                    "album": album_data["album_name"],
                    "album_artist": album_data["album_artist"],
                    "year": album_data["album_year"],
                    "genre": album_data["album_genre"],
                    "track_number": song["track_number"],
                    "cover_art_path": album_data["album_art"],
                    "lyrics": song.get("lyrics", "")
                }
                add_metadata(mp3_path, metadata)
            except Exception as e:
                errors.append(f"{song['song_name']}: {e}")

        if errors:
            QMessageBox.warning(self, "Some Errors Occurred", "\n".join(errors))
        else:
            QMessageBox.information(self, "Success", "All songs downloaded and tagged!")