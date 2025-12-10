"""
Defines forms for editing MP3 metadata and downloading from YouTube.
"""
from django import forms

class EditMP3Form(forms.Form):
    mp3_file = forms.FileField(label="Upload MP3 file")
    title = forms.CharField(max_length=255, required=False)
    artist = forms.CharField(max_length=255, required=False)
    album = forms.CharField(max_length=255, required=False)
    album_artist = forms.CharField(max_length=255, required=False)
    year = forms.CharField(max_length=4, required=False)
    genre = forms.CharField(max_length=255, required=False)
    track_number = forms.CharField(max_length=10, required=False)
    lyrics = forms.CharField(widget=forms.Textarea, required=False)
    cover_art = forms.ImageField(label="Cover Art", required=False)
    output_filename = forms.CharField(max_length=255, required=False)

class YouTubeForm(forms.Form):
    youtube_url = forms.URLField(label="YouTube URL")
    title = forms.CharField(max_length=255, required=False)
    artist = forms.CharField(max_length=255, required=False)
    album = forms.CharField(max_length=255, required=False)
    album_artist = forms.CharField(max_length=255, required=False)
    year = forms.CharField(max_length=4, required=False)
    genre = forms.CharField(max_length=255, required=False)
    track_number = forms.CharField(max_length=10, required=False)
    lyrics = forms.CharField(widget=forms.Textarea, required=False)
    cover_art = forms.ImageField(label="Cover Art", required=False)
    output_filename = forms.CharField(max_length=255, required=False)