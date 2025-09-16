# Imports
import os
import subprocess # To run ffmpeg
from yt_dlp import YoutubeDl # To download YouTube Audio
from mutagen.mp3 import MP3 # To edit MP3 metadata
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC # ID3 tag types

# Downloading a Youtube video from a link
def download_youtube_audio(youtube_url, output_filename="temp.m4a"):
    ydl_opts = {
        'format': 'bestaudio/best', # Downloading the best audio quality available
        'outtmpl': output_filename, # Setting the output filename
        'quiet': False, # To show download progress
        'postprocessors': [{    # Done after downloading
            'key': 'FFmpegExtractAudio', # Extract just audio using ffmpeg
            'preferredcodec': 'm4a',    # Specify to convert to m4a
            'preferredquality': '192',  # 192kbps quality
        }]
    }

    # Downloading process
    print("[*] Downloading audio from Youtube...")
    with YoutubeDl(ydl_opts) as ydl:
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
        ])

        print("[+] Conversion complete.")