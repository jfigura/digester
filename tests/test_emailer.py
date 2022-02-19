import pytest
import responses

from digester.emailer import send_email


@responses.activate
def test_emailer():
    responses.add(
        responses.POST,
        'https://api.mailgun.net/v3/sandbox0ec66a6594f147c48dfac000ce780ea9.mailgun.org/messages',
        status=200)
    send_email('hello')


@responses.activate
def test_emailer_failed():
    responses.add(
        responses.POST,
        'https://api.mailgun.net/v3/sandbox0ec66a6594f147c48dfac000ce780ea9.mailgun.org/messages',
        status=401)
    with pytest.raises(Exception):
        send_email('hello')
