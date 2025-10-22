# Imports
import os
import subprocess # To run ffmpeg
from yt_dlp import YoutubeDL # To download YouTube Audio
from mutagen.mp3 import MP3 # To edit MP3 metadata
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, TDRC, TCON, APIC, TRCK, USLT # ID3 tag types

# Downloading a Youtube video from a link
def download_youtube_audio(youtube_url, output_folder):
    output_template = os.path.join(output_folder, "%(title)s.%(ext)s")
    print(f'Output template: {output_template}')
    ydl_opts = {
        'format': 'bestaudio/best', # Downloading the best audio quality available
        'outtmpl': output_template, # Setting the output filename
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
        info = ydl.extract_info(youtube_url)
        # This will return the actual file path of the downloaded file
        downloaded_file = ydl.prepare_filename(info)
    print("[+] Download complete.")
    print(f'Downloaded file: {downloaded_file}')
    return downloaded_file

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
    print(f'Output file: {output_file}')
    print("[+] Conversion complete.")
    return output_file

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

        audio.save(v2_version=3) # Save the updated mp3 file
        print("[+] Metadata added.")