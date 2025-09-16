# Imports
import os
import subprocess # To run ffmpeg
from yt_dlp import YoutubeDl as Ytdl # To download YouTube Audio
from mutagen.mp3 import MP3 # To edit MP3 metadata
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC # ID3 tag types

# Downloading a Youtube video from a link
