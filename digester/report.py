from typing import List
from datetime import datetime

from digester.spotify import SongPlayedRecord


def make_report(date: datetime, recently_played: List[SongPlayedRecord]):
    date_string = date.strftime("%A, %d. %B %Y")
    report = f'You played {len(recently_played)} songs on {date_string}.\n\n'
    lines = [f'{song.artist}: {song.name}' for song in recently_played]
    report += '\n'.join(lines)
    return report
