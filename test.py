from datetime import datetime, timedelta

N_RECENT_TRACKS = 500  # how many recent tracks should be considered to determine favourite artist/album/song
DATE_FORMAT_STR = '%d %b %Y %H:%M'

with open("server/mahathu.csv", "r") as f:
    # lines = [l.strip() for l in f.readlines()][:500]
    lines = [l.strip() for l in f.readlines()]

colnames = ['artist', 'album', 'title', 'time']
tracks = [
    dict(zip(colnames, line.split(','))) 
    for line in lines[::-1]
]

most_played_artists = {}

for i, track in enumerate(tracks):
    artist = track['artist']
    most_played_artists[artist] = most_played_artists.get(artist, 0) + 1

    if i >= N_RECENT_TRACKS:
        remove_artist = tracks[i-N_RECENT_TRACKS]['artist']
        most_played_artists[remove_artist] = most_played_artists[remove_artist] - 1

    tracks[i]['favorite_artist'] = max(most_played_artists, key=most_played_artists.get)
    tracks[i]['favorite_artist_n'] = most_played_artists[tracks[i]['favorite_artist']]
    try:
        tracks[i]['timestamp'] = datetime.strptime(tracks[i]['time'], DATE_FORMAT_STR)
    except ValueError:
        print(track)

n_changes = -1
prev_fav_artist = ''
last_change = tracks[0]['timestamp']
total_delta = timedelta()
for track in tracks:
    if track['favorite_artist'] != prev_fav_artist:
        delta = track['timestamp'] - last_change
        total_delta += delta
        print(f"{prev_fav_artist} was fav artist for {delta}")
        last_change = track['timestamp']
        prev_fav_artist = track['favorite_artist']
        n_changes += 1
    
    
print(f"{n_changes} changes when considering last {N_RECENT_TRACKS} tracks. average: {total_delta/n_changes}")