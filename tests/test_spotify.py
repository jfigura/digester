import json
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from digester.spotify import (get_recently_played, RecentlyPlayedMode,
                              SpotifyClient, create_oath_cache)


@pytest.fixture
def spotify_client():
    mock = MagicMock(SpotifyClient)
    mock.current_user_recently_played.return_value = {
        'items': [
            _item('Hans Zimmer', 'Time', '1', datetime.now()),
            _item('Oasis', 'Supersonic', '2', datetime.now()),
            _item('ABC', 'Overtime', '3',
                  datetime.now() - timedelta(days=1)),
            _item('DEF', 'Whatever', '4',
                  datetime.now() - timedelta(days=2)),
        ]
    }
    return mock


@pytest.fixture
def oauth_env():
    value = 'dummy-refresh'
    os.environ['SPOTIFY_REFRESH_TOKEN'] = 'dummy-refresh'
    yield value
    del os.environ['SPOTIFY_REFRESH_TOKEN']


def test_get_recently_played_all(spotify_client):
    results = get_recently_played(RecentlyPlayedMode.ALL, spotify_client)
    _check_ids(results, ['1', '2', '3', '4'])
    assert results[0].artist == 'Hans Zimmer'
    assert results[0].name == 'Time'
    assert results[0].track_id == '1'
    assert datetime.now(tz=timezone.utc) - results[0].played_at < timedelta(
        seconds=1)


def test_get_recently_played_today(spotify_client):
    results = get_recently_played(RecentlyPlayedMode.TODAY, spotify_client)
    _check_ids(results, ['1', '2'])


def test_get_recently_played_yesterday(spotify_client):
    results = get_recently_played(RecentlyPlayedMode.YESTERDAY, spotify_client)
    _check_ids(results, ['3'])


def test_create_oath_cache(oauth_env, tmp_path):
    cache_path = tmp_path / '.cache'
    create_oath_cache(cache_path)
    cache = json.loads(cache_path.read_text())
    assert cache == {
        'refresh_token': oauth_env,
        'scope': 'user-read-recently-played',
        'expires_at': 0
    }


def test_create_oath_cache_missing_env(tmp_path):
    cache_path = tmp_path / '.cache'
    with pytest.raises(ValueError):
        create_oath_cache(cache_path)


def test_create_oath_cache_existing(tmp_path):
    cache_path = tmp_path / '.cache'
    cache_path.write_text('test')
    create_oath_cache(cache_path)
    assert cache_path.read_text() == 'test'


def _item(artist, track_name, track_id, played_at):
    return {
        'track': {
            'artists': [{
                'name': artist,
            }],
            'id': track_id,
            'name': track_name,
        },
        'played_at': played_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    }


def _check_ids(results, expected_ids):
    assert [result.track_id for result in results] == expected_ids
