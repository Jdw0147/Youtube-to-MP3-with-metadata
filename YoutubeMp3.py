# Imports
import os
import subprocess # To run ffmpeg
from yt_dlp import YoutubeDl # To download YouTube Audio
from mutagen.mp3 import MP3 # To edit MP3 metadata
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC # ID3 tag types

# Downloading a Youtube video from a link
def download_youtube_audio(youtube_url, output_filename="temp.m4a"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }]
    }

    # Downloading process
    print("[*] Downloading audio from Youtube...")
    with YoutubeDl(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print("[+] Download complete.")

    