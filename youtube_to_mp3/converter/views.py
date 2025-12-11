"""
Handles HTTP requests for the converter app.
Renders the home page, song edit form, and YouTube download form.
"""
from django.shortcuts import render
from .forms import EditMP3Form, YouTubeForm
from .utils import safe_filename
import os
from django.conf import settings
from django.http import FileResponse
import threading
from django.http import Http404
import shutil

def home(request):
    # Main landing page with Song and Album sections
    return render(request, 'converter/home.html')

def song_edit(request):
    # Edit existing MP3 metadata
    if request.method == 'POST':
        form = EditMP3Form(request.POST, request.FILES)
        if form.is_valid():
            mp3_file = request.FILES['mp3_file']
            # Save uploaded file to temp location
            temp_path = os.path.join(settings.MEDIA_ROOT, mp3_file.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in mp3_file.chunks():
                    destination.write(chunk)

            # Check extension
            ext = os.path.splitext(temp_path)[1].lower()
            output_filename = form.cleaned_data['output_filename'] or safe_filename(
                f"{form.cleaned_data['title']} - {form.cleaned_data['artist']}"
            )
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename + ".mp3")

            if ext != ".mp3":
                # Convert to mp3
                from .YoutubeMp3 import to_mp3
                mp3_path = to_mp3(temp_path, output_path)
            else:
                shutil.copy(temp_path, output_path)
                mp3_path = output_path

            # Call your add_metadata function here
            from .YoutubeMp3 import add_metadata
            metadata = {
                "title": form.cleaned_data['title'],
                "artist": form.cleaned_data['artist'],
                "album": form.cleaned_data['album'],
                "album_artist": form.cleaned_data['album_artist'],
                "year": form.cleaned_data['year'],
                "genre": form.cleaned_data['genre'],
                "track_number": form.cleaned_data['track_number'],
                "lyrics": form.cleaned_data['lyrics'],
                "cover_art_path": None,
            }
            if form.cleaned_data['cover_art']:
                cover = form.cleaned_data['cover_art']
                cover_path = os.path.join(settings.MEDIA_ROOT, cover.name)
                with open(cover_path, 'wb+') as dest:
                    for chunk in cover.chunks():
                        dest.write(chunk)
                metadata['cover_art_path'] = cover_path

            add_metadata(mp3_path, metadata)
            return render(request, 'converter/song_edit.html', {
                'form': form,
                'success': True,
                'output_file': os.path.basename(mp3_path)
            })
    else:
        form = EditMP3Form()
    return render(request, 'converter/song_edit.html', {'form': form})

def download_file(request, filename):
    # Serve the file for download
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        # Schedule file deletion after response is sent
        def delete_file(path):
            import time
            time.sleep(1)  # Wait for the response to finish
            try:
                os.remove(path)
            except Exception:
                pass

        threading.Thread(target=delete_file, args=(file_path,)).start()
        return response
    else:
        raise Http404("File does not exist")

def song_youtube(request):
    # Download from YouTube and edit metadata
    if request.method == 'POST':
        form = YouTubeForm(request.POST, request.FILES)
        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            from .YoutubeMp3 import download_youtube_audio, to_mp3, add_metadata
            # Download audio
            audio_path = download_youtube_audio(youtube_url, settings.MEDIA_ROOT)
            # Convert to mp3 if needed
            ext = os.path.splitext(audio_path)[1].lower()
            filename = form.cleaned_data['output_filename'] or safe_filename(
                f"{form.cleaned_data['title']} - {form.cleaned_data['artist']}"
            )
            output_path = os.path.join(settings.MEDIA_ROOT, filename + ".mp3")
            if ext != ".mp3":
                mp3_path = to_mp3(audio_path, output_path)
            else:
                import shutil
                shutil.copy(audio_path, output_path)
                mp3_path = output_path
            # Prepare metadata
            metadata = {
                "title": form.cleaned_data['title'],
                "artist": form.cleaned_data['artist'],
                "album": form.cleaned_data['album'],
                "album_artist": form.cleaned_data['album_artist'],
                "year": form.cleaned_data['year'],
                "genre": form.cleaned_data['genre'],
                "track_number": form.cleaned_data['track_number'],
                "lyrics": form.cleaned_data['lyrics'],
                "cover_art_path": None,
            }
            if form.cleaned_data['cover_art']:
                cover = form.cleaned_data['cover_art']
                cover_path = os.path.join(settings.MEDIA_ROOT, cover.name)
                with open(cover_path, 'wb+') as dest:
                    for chunk in cover.chunks():
                        dest.write(chunk)
                metadata['cover_art_path'] = cover_path
            add_metadata(mp3_path, metadata)
            # Clean up temp files if needed
            return render(request, 'converter/song_youtube.html', {'form': form, 'success': True, 'output_file': filename + ".mp3"})
    else:
        form = YouTubeForm()
    return render(request, 'converter/song_youtube.html', {'form': form})