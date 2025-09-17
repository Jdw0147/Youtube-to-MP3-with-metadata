# Imports
import os
import subprocess # To run ffmpeg
from yt_dlp import YoutubeDL # To download YouTube Audio
from mutagen.mp3 import MP3 # To edit MP3 metadata
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, TDRC, TCON, APIC, TRCK, USLT # ID3 tag types
import tkinter as tk
from tkinter import filedialog, messagebox

# Downloading a Youtube video from a link
def download_youtube_audio(youtube_url, output_filename="temp"):
    ydl_opts = {
        'format': 'bestaudio/best', # Downloading the best audio quality available
        'outtmpl': output_filename, # Setting the output filename
        'quiet': False, # Not showing download process
        'postprocessors': [{    # Done after downloading
            'key': 'FFmpegExtractAudio', # Extract just audio using ffmpeg
            'preferredcodec': 'm4a',    # Specify to convert to m4a
            'preferredquality': '192',  # 192kbps quality
        }]
    }

    # Downloading process
    print("[*] Downloading audio from Youtube...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url]) # Downloading the video (youtube_url) and applying the options (ydl_opts)
    print("[+] Download complete.")

# Function that converts the m4a file into an mp3 file
def to_mp3(input_file, output_file="download.mp3"):
    print("[*] Converting to mp3...")
    subprocess.run([
        "ffmpeg", "-y", # Overwrite output file if one exists
        "-i", input_file, # Input file
        "-vn", # No video
        "-ar", "44100", # Set audio sampling rate
        "-ac", "2", # Set number of audio channels
        "-b:a", "192k", # Set audio bitrate
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL # Hides ffmpeg output
    )
    

    print("[+] Conversion complete.")

    # Function to add metadata to the mp3 file
def add_metadata(mp3_file, metadata):
    print("[*] Adding metadata...")
    audio = MP3(mp3_file, ID3=ID3) #Loading mp3 file
    try:
        audio.add_tags() # Trying to add ID3 tage if they dont already exist
    except Exception:
        pass # If tags already exist, do nothing

    # Adding metadata (standard ID3 tags)
    audio.tags.add(TIT2(encoding=3, text=metadata["title"])) # Song title
    audio.tags.add(TPE1(encoding=3, text=metadata["artist"])) # Artist name
    if metadata["album_artist"].strip():    # Only add album artist if provided
        audio.tags.add(TPE2(encoding=3, text=metadata["album_artist"])) # Album artist
    audio.tags.add(TALB(encoding=3, text=metadata["album"])) # Album name
    audio.tags.add(TDRC(encoding=3, text=metadata["year"])) # Year of release
    audio.tags.add(TCON(encoding=3, text=metadata["genre"])) # Genre
    audio.tags.add(TRCK(encoding=3, text=metadata["track_number"])) # Track number

    # Lyrics
    audio.tags.add(USLT(encoding=3, lang='eng', desc='Lyrics', text=metadata["lyrics"]))

    # Album Art
    with open(metadata["cover_art_path"], 'rb') as albumart:
        audio.tags.add(APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=albumart.read()
        ))

        audio.save() # Save the updated mp3 file
        print("[+] Metadata added.")


# GUI Interface
class YoutubeMp3GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube to MP3 with customizable metadata")

        # Input fields for GUI stored in a dictionary
        self.fields = {
            "Youtube URL": tk.Entry(root, width=50),
            "Title": tk.Entry(root, width=50),
            "Artist": tk.Entry(root, width=50),
            "Album": tk.Entry(root, width=50),
            "Album Artist": tk.Entry(root, width=50),
            "Year": tk.Entry(root, width=50),
            "Genre": tk.Entry(root, width=50),
            "Track Number": tk.Entry(root, width=50),
            "Lyrics": tk.Text(root, width=50, height=10),
        }

        # Layout input fields on the GUI
        row = 0
        for label, widget in self.fields.items():
            tk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=2)
            widget.grid(row=row, column=1, padx=10, pady=2)
            row += 1

        # Cover Art file selection (file dialog)
        self.cover_art_path = tk.StringVar()
        tk.Label(root, text="Cover Art:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        tk.Entry(root, textvariable=self.cover_art_path, width=40).grid(row=row, column=1, sticky="w", padx=10)
        tk.Button(root, text="Browse", command=self.select_cover_art).grid(row=row, column=2)
        row += 1

        # Output Directory selection (folder dialog)
        self.output_dir = tk.StringVar()
        tk.Label(root, text="Save To Folder:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        tk.Entry(root, textvariable=self.output_dir, width=40).grid(row=row, column=1)
        tk.Button(root, text="Browse", command=self.select_output_directory).grid(row=row, column=2)
        row += 1

        # Output filename entry
        self.output_filename = tk.Entry(root, width=50)
        tk.Label(root, text="Output Filename (no extension):").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.output_filename.grid(row=row, column=1, padx=10, pady=2)
        row += 1

        # Download Button
        tk.Button(root, text="Download and Convert", command=self.process).grid(row=row, column=1, pady=10)


    # Cover Art File Selection Dialog
    def select_cover_art(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if path:
            self.cover_art_path.set(path)

    # Output Directory Selection Dialog
    def select_output_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    # Main process logic
    def process(self):
        try:
            youtube_url = self.fields["YouTube URL"].get().strip()
            if not youtube_url:
                raise ValueError("YouTube URL is required.")
            print("YouTube URL:", youtube_url)  # Debug line

            # Metadata
            metadata = {
                "title": self.fields["Title"].get(),
                "artist": self.fields["Artist"].get(),
                "album": self.fields["Album"].get(),
                "album_artist": self.fields["Album Artist"].get(),
                "year": self.fields["Year"].get(),
                "genre": self.fields["Genre"].get(),
                "track_number": self.fields["Track Number"].get(),
                "lyrics": self.fields["Lyrics"].get("1.0", tk.END).strip(),
                "cover_art_path": self.cover_art_path.get()
            }

            # Validate save folder and filename
            output_dir = self.output_dir.get()
            if not output_dir:
                raise ValueError("Please select a save folder.")

            filename = self.output_filename.get().strip()
            if not filename:
                raise ValueError("Please enter an output filename.")

            output_mp3_path = os.path.join(output_dir, f"{filename}.mp3")

            # Download & convert
            messagebox.showinfo("Processing", "Downloading audio from YouTube...")
            download_youtube_audio(youtube_url)
            to_mp3("temp.m4a", output_mp3_path)

            # Add metadata
            add_metadata(output_mp3_path, metadata)

            # Cleanup
            if os.path.exists("temp.m4a"):
                os.remove("temp.m4a")

            # Success message
            messagebox.showinfo("Success", f"MP3 file saved to:\n{output_mp3_path}")
        # Error message
        except Exception as e:
            messagebox.showerror("Error", str(e))

# python entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeMp3GUI(root)
    root.mainloop()