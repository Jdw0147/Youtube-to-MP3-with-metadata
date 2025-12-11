"""
URL configuration for app.
Defines routes for home, song edit, and song YouTube download.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('song/edit/', views.song_edit, name='song_edit'),
    path('song/youtube/', views.song_youtube, name='song_youtube'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]