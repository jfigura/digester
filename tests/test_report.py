from datetime import datetime

from digester.report import make_report
from digester.spotify import SongPlayedRecord


def test_make_report():
    date = datetime.fromisoformat("2022-02-09T21:48:00-05:30")
    songs = [
        SongPlayedRecord('Nirvana', 'Polly', '1', datetime.now()),
        SongPlayedRecord('Oasis', 'Whatever', '2', datetime.now()),
    ]
    report = make_report(date, songs)
    assert report == '\n'.join([
        'You played 2 songs on Wednesday, February 09, 2022.\n',
        'Nirvana: Polly',
        'Oasis: Whatever',
    ])
