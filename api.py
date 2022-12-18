import requests
import time
import yaml
import pandas as pd

with open("secrets.yml", "r") as secrets_file:
    secrets = yaml.safe_load(secrets_file)

BASE_URL = "https://ws.audioscrobbler.com/2.0/"
LASTFM_API_KEY = secrets["lastfm-api-key"]
USER = "mahathu"

next_page = 1
n_pages_total = 2


def extract_track_info(track):
    return {
        "artist": track["artist"]["#text"],
        "album": track["album"]["#text"],
        "title": track["name"],
        "ts": track["date"]["uts"] if "date" in track else int(time.time()),
    }

all_tracks = []

while next_page <= n_pages_total:
    response = requests.get(
        BASE_URL,
        params={
            "api_key": LASTFM_API_KEY,
            "method": "User.getrecenttracks",
            "user": USER,
            "format": "json",
            "limit": 1000,
            "page": next_page,
        },
    ).json()["recenttracks"]

    n_pages_total = int(response["@attr"]["totalPages"])
    next_page = int(response["@attr"]["page"]) + 1

    tracks = [
        extract_track_info(track)
        for track in response["track"]
        if "date" in track  # currently playing track doesn't have date key
    ]

    if (
        next_page == 2 and "@attr" in response["track"][0]
    ):  # first page, so check if a track is currently playing
        print("user is currently scrobbling")
        tracks.insert(0, extract_track_info(response["track"][0]))

    all_tracks.extend(tracks)
    total_tracks = response["@attr"]["total"]
    print(f"{len(all_tracks)}/{total_tracks}")

df = pd.DataFrame(all_tracks)
df.to_csv(f'{USER}.csv', index=False)