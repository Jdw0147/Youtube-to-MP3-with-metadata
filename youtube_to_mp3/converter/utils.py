
import os
import shutil
import threading
from django.conf import settings
from django.http import FileResponse, Http404
from .YoutubeMp3 import to_mp3, add_metadata
from .filename_utils import safe_filename


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
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)

        def delete_temp_files():
            import time
            time.sleep(1)
            temp_files = request.session.pop('temp_files', [])
            for f in temp_files:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception:
                        pass

        threading.Thread(target=delete_temp_files).start()
        return response
    else:
        raise Http404("File does not exist")