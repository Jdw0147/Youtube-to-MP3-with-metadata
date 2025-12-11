
import os
import shutil
import threading
from django.conf import settings
from django.http import FileResponse, Http404
from .YoutubeMp3 import to_mp3, add_metadata
from .filename_utils import safe_filename
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, APIC, TPE2, TALB, TDRC, TCON, TRCK, USLT


##################################
# Helper functions are stored here
##################################


#
# Function that uses shared logic between song_edit and song_youtube views to eliminate redundancy
#
def process_mp3_with_metadata(
    input_path,
    output_filename,
    metadata,
    cover_file=None,
    convert_if_needed=True
):
    ext = os.path.splitext(input_path)[1].lower()
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename + ".mp3")

    # Track all temp files for cleanup
    temp_files = set([input_path, output_path]) 

    # If input and output are the same file, don't copy—just update metadata in place
    if os.path.abspath(input_path) == os.path.abspath(output_path):
        mp3_path = input_path
    else:
        if convert_if_needed and ext != ".mp3":
            mp3_path = to_mp3(input_path, output_path)
            temp_files.add(mp3_path)
        else:
            shutil.copy(input_path, output_path)
            mp3_path = output_path

    if cover_file:
        cover_path = os.path.join(settings.MEDIA_ROOT, cover_file.name)
        with open(cover_path, 'wb+') as dest:
            for chunk in cover_file.chunks():
                dest.write(chunk)
        metadata['cover_art_path'] = cover_path
        temp_files.add(cover_path)
    else:
        # Try to extract existing cover art from input_path
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC
        audio = MP3(input_path, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                cover_path = os.path.join(settings.MEDIA_ROOT, "current_cover.jpg")
                with open(cover_path, "wb") as img_out:
                    img_out.write(tag.data)
                metadata['cover_art_path'] = cover_path
                temp_files.add(cover_path)
                break
        else:
            metadata['cover_art_path'] = None

    add_metadata(mp3_path, metadata)

    if metadata['cover_art_path'] and os.path.exists(metadata['cover_art_path']):
        try:
            os.remove(metadata['cover_art_path'])
            temp_files.discard(metadata['cover_art_path'])
        except Exception:
            pass

    return mp3_path, temp_files


#
# Function to handle download and cleanup of files
#
def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    cover_path = os.path.join(settings.MEDIA_ROOT, "current_cover.jpg")

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)

        def delete_temp_files():
            import time
            time.sleep(1)
            try:
                os.remove(file_path)
            except Exception:
                pass
            # Delete the cover art preview file
            if os.path.exists(cover_path):
                try:
                    os.remove(cover_path)
                except Exception:
                    pass

        threading.Thread(target=delete_temp_files).start()
        return response
    else:
        raise Http404("File does not exist")
    

#
# Function to getmp3 file data when reading a file to edit
#
def get_mp3_metadata(mp3_path):
    """
    Extracts metadata from an MP3 file and returns a dict suitable for initializing the form.
    """
    data = {}
    try:
        audio = MP3(mp3_path, ID3=ID3)
        data['title'] = audio.tags.get('TIT2', [''])[0] if audio.tags.get('TIT2') else ''
        data['artist'] = audio.tags.get('TPE1', [''])[0] if audio.tags.get('TPE1') else ''
        data['album'] = audio.tags.get('TALB', [''])[0] if audio.tags.get('TALB') else ''
        data['album_artist'] = audio.tags.get('TPE2', [''])[0] if audio.tags.get('TPE2') else ''
        data['year'] = str(audio.tags.get('TDRC', [''])[0]) if audio.tags.get('TDRC') else ''
        data['genre'] = audio.tags.get('TCON', [''])[0] if audio.tags.get('TCON') else ''
        data['track_number'] = audio.tags.get('TRCK', [''])[0] if audio.tags.get('TRCK') else ''
        data['lyrics'] = audio.tags.get('USLT::eng', USLT(encoding=3, text='')).text if audio.tags.get('USLT::eng') else ''
        # Extract cover art
        cover_art_path = None
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                cover_art_path = os.path.join(settings.MEDIA_ROOT, "current_cover.jpg")
                with open(cover_art_path, "wb") as img_out:
                    img_out.write(tag.data)
                # Save relative path for template
                data['cover_art_url'] = "current_cover.jpg"
                break
        if not 'cover_art_url' in data:
            data['cover_art_url'] = None
    except Exception:
        # If file is not a valid MP3 or has no tags, leave fields blank
        pass
    return data