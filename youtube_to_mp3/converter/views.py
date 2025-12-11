"""
Handles HTTP requests for the converter app.
Renders the home page, song edit form, and YouTube download form.
"""
from django.shortcuts import render
from .forms import EditMP3Form, YouTubeForm
from .utils import process_mp3_with_metadata
from .filename_utils import safe_filename
import os
from django.conf import settings



def home(request):
    # Main landing page with Song and Album sections
    return render(request, 'converter/home.html')

# Function to edit metadata of existing audio files (will convert to mp3 if not already an mp3)
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

            output_filename = form.cleaned_data['output_filename'] or safe_filename(
                f"{form.cleaned_data['title']} - {form.cleaned_data['artist']}"
            )

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
            }
            
            mp3_path, temp_files = process_mp3_with_metadata(
                temp_path,
                output_filename,
                metadata,
                cover_file=form.cleaned_data.get('cover_art')
            )
            request.session['temp_files'] = list(temp_files)

            return render(request, 'converter/song_edit.html', {
                'form': form,
                'success': True,
                'output_file': os.path.basename(mp3_path)
            })
    else:
        form = EditMP3Form()
    return render(request, 'converter/song_edit.html', {'form': form})

# Function to handle converting youtube links to mp3 files
def song_youtube(request):
    if request.method == 'POST':
        form = YouTubeForm(request.POST, request.FILES)
        if form.is_valid():
            from .YoutubeMp3 import download_youtube_audio
            youtube_url = form.cleaned_data['youtube_url']
            audio_path = download_youtube_audio(youtube_url, settings.MEDIA_ROOT)

            output_filename = form.cleaned_data['output_filename'] or safe_filename(
                f"{form.cleaned_data['title']} - {form.cleaned_data['artist']}"
            )

            metadata = {
                "title": form.cleaned_data['title'],
                "artist": form.cleaned_data['artist'],
                "album": form.cleaned_data['album'],
                "album_artist": form.cleaned_data['album_artist'],
                "year": form.cleaned_data['year'],
                "genre": form.cleaned_data['genre'],
                "track_number": form.cleaned_data['track_number'],
                "lyrics": form.cleaned_data['lyrics'],
            }

            mp3_path, temp_files = process_mp3_with_metadata(
                audio_path,
                output_filename,
                metadata,
                cover_file=form.cleaned_data.get('cover_art')
            )
            request.session['temp_files'] = list(temp_files)

            return render(request, 'converter/song_youtube.html', {
                'form': form,
                'success': True,
                'output_file': os.path.basename(mp3_path)
            })
    else:
        form = YouTubeForm()
    return render(request, 'converter/song_youtube.html', {'form': form})