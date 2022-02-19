import logging
from datetime import datetime, timedelta

import fire

from digester.emailer import send_email
from digester.report import make_report
from digester.spotify import get_recently_played, RecentlyPlayedMode


def run():
    recently_played = get_recently_played(RecentlyPlayedMode.YESTERDAY)
    date = datetime.now() - timedelta(days=1)
    report = make_report(date, recently_played)
    send_email(report)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    fire.Fire(run)
