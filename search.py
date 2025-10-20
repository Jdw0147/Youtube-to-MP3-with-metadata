import requests

DISCOGS_TOKEN = 'EurItYjbxmcFweNWLKVPinAygglnADxrWDDkxFfc'
url = 'https://api.discogs.com/database/search'
def search_song(song_name, artist_name = None, album_name = None):
    params = {
        'track': song_name,
        'type': 'release',
        'format': 'File',
        'token': DISCOGS_TOKEN,
        "per_page": 5,
        "country": "US"
    }

    if artist_name:
        params['artist'] = artist_name
    if album_name:
        params['release_title'] = album_name

    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    return results

def search_album(album_name, artist_name = None):
    params = {
        'q': album_name,
        'type': 'release',
        'format': 'File',
        'token': DISCOGS_TOKEN,
        "per_page": 5,
        "country": "US"
    }
    if artist_name:
        params['artist'] = artist_name
    
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    return results


# IDEAS FOR REST OF SITE:
# Users can search for album and clicking an album will do the following:
# 1. Get album info, Generate however many songs there are and fill out the song info (NOT URL)
# So if you also have a youtube playlist with that album, you can paste it in and make it to where the URL
# fields of the songs get filled by matching the track numbers.
