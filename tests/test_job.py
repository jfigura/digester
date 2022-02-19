from unittest.mock import patch

from digester.job import run


@patch('digester.job.get_recently_played')
@patch('digester.job.send_email')
def test_run(send_email, get_recently_played):
    run()
    get_recently_played.assert_called()
    send_email.assert_called()
