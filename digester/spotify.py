import json
import os
import pathlib
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import dateutil.parser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_SCOPE = 'user-read-recently-played'


@dataclass
class SongPlayedRecord:

    artist: str
    name: str
    track_id: str
    played_at: datetime

    @classmethod
    def from_spotify_result(cls, result):
        artist = result['track']['artists'][0]['name']
        name = result['track']['name']
        track_id = result['track']['id']
        played_at = dateutil.parser.isoparse(result['played_at'])
        return SongPlayedRecord(artist, name, track_id, played_at)

    def __repr__(self):
        return f'{self.artist}: {self.name} ({self.played_at})'


class SpotifyClient:  # pragma: no cover

    def __init__(self):
        create_oath_cache()
        self._spotify = Spotify(client_credentials_manager=SpotifyOAuth(
            scope=SPOTIFY_SCOPE))

    def current_user_recently_played(self):
        return self._spotify.current_user_recently_played()


class RecentlyPlayedMode(Enum):

    ALL = 1
    YESTERDAY = 2
    TODAY = 3


def get_recently_played(mode=RecentlyPlayedMode.ALL,
                        client: SpotifyClient = None):
    if not client:
        client = SpotifyClient()  # pragma: no cover
    results = client.current_user_recently_played()
    results = [
        SongPlayedRecord.from_spotify_result(result)
        for result in results['items']
    ]
    day = None
    if mode == RecentlyPlayedMode.TODAY:
        day = datetime.now(tz=timezone.utc)
    if mode == RecentlyPlayedMode.YESTERDAY:
        day = datetime.now(tz=timezone.utc) - timedelta(days=1)
    if day:
        begin = day.replace(hour=0, minute=0, second=0)
        end = day.replace(hour=23, minute=59, second=59)
        results = [
            result for result in results if begin <= result.played_at <= end
        ]
    return results


def create_oath_cache(target_path='.cache'):
    cache_path = pathlib.Path(target_path)
    if cache_path.exists():
        return
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    if not refresh_token:
        raise ValueError('SPOTIFY_REFRESH_TOKEN env var not set.')
    oauth_cache = {
        'refresh_token': refresh_token,
        'scope': SPOTIFY_SCOPE,
        'expires_at': 0,
    }
    cache_path.write_text(json.dumps(oauth_cache), encoding='utf-8')


def main():
    results = get_recently_played(RecentlyPlayedMode.ALL)
    for result in results:
        print(result)


if __name__ == '__main__':
    main()
