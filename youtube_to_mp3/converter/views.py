"""
Handles HTTP requests for the converter app.
Renders the home page, song edit form, and YouTube download form.
"""
from django.shortcuts import render, redirect
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from .forms import EditMP3Form, YouTubeForm, UploadMP3Form
from .utils import process_mp3_with_metadata, get_mp3_metadata
from .filename_utils import safe_filename
import os
from django.conf import settings



def home(request):
    # Main landing page with Song and Album sections
    return render(request, 'converter/home.html')

# Function to edit metadata of existing audio files (will convert to mp3 if not already an mp3)
def song_edit(request):
    # Handle back button or direct GET to step 1: always clear session
    if (request.method == 'GET' and not request.session.get('uploaded_mp3')) or (request.method == 'GET' and request.GET.get('back')):
        if request.session.get('uploaded_mp3'):
            try:
                os.remove(request.session['uploaded_mp3'])
            except Exception:
                pass
            del request.session['uploaded_mp3']
        form = UploadMP3Form()
        return render(request, 'converter/song_upload.html', {'form': form})

    # Step 1 POST: Save file and redirect to edit
    if request.method == 'POST' and not request.session.get('uploaded_mp3'):
        form = UploadMP3Form(request.POST, request.FILES)
        if form.is_valid():
            mp3_file = form.cleaned_data['mp3_file']
            temp_path = os.path.join(settings.MEDIA_ROOT, mp3_file.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in mp3_file.chunks():
                    destination.write(chunk)
            request.session['uploaded_mp3'] = temp_path
            return redirect('song_edit')
        else:
            return render(request, 'converter/song_upload.html', {'form': form})

    # Step 2: Edit metadata
    temp_path = request.session.get('uploaded_mp3')

    if temp_path and not os.path.exists(temp_path):
        # File is missing, clear session and go to step 1
        del request.session['uploaded_mp3']
        form = UploadMP3Form()
        return render(request, 'converter/song_upload.html', {'form': form})
    
    if temp_path:
        if request.method == 'GET':
            initial_data = get_mp3_metadata(temp_path)
            initial_data['output_filename'] = os.path.splitext(os.path.basename(temp_path))[0]
            cover_art_url = initial_data.get('cover_art_url')
            form = EditMP3Form(initial=initial_data)
            return render(request, 'converter/song_edit.html', {
                'form': form,
                'uploaded_file': os.path.basename(temp_path),
                'cover_art_url': cover_art_url,
            })
        
        elif request.method == 'POST':
            form = EditMP3Form(request.POST, request.FILES)
            if form.is_valid():
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
                cover_file = request.FILES.get('cover_art')
                mp3_path, temp_files = process_mp3_with_metadata(
                    temp_path,
                    output_filename,
                    metadata,
                    cover_file=cover_file
                )

                request.session['temp_files'] = list(temp_files)

                
                old_file = temp_path
                new_file = os.path.join(settings.MEDIA_ROOT, output_filename + ".mp3")
                if os.path.abspath(old_file) != os.path.abspath(new_file) and os.path.exists(old_file):
                    try:
                        os.remove(old_file)
                    except Exception:
                        pass

                del request.session['uploaded_mp3']

                initial_data = get_mp3_metadata(mp3_path)
                cover_art_url = initial_data.get('cover_art_url')

                return render(request, 'converter/song_edit.html', {
                    'form': form,
                    'success': True,
                    'output_file': os.path.basename(mp3_path),
                    'uploaded_file': os.path.basename(mp3_path),
                    'cover_art_url': cover_art_url, 
                })
            else:
                return render(request, 'converter/song_edit.html', {
                    'form': form, 
                    'success': True,
                    'output_file': os.path.basename(mp3_path),
                    'uploaded_file': os.path.basename(mp3_path),
                    })

    # Fallback
    form = UploadMP3Form()
    return render(request, 'converter/song_upload.html', {'form': form})

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