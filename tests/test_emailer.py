import os

import pytest
import responses

from digester.emailer import send_email


@pytest.fixture
def email_url():
    value = 'https://api.mailgun.net/v3/test.mailgun.org/messages'
    os.environ['MAILGUN_URL'] = value
    yield value
    del os.environ['MAILGUN_URL']


@responses.activate
def test_emailer(email_url):
    responses.add(responses.POST, email_url, status=200)
    send_email('hello')


@responses.activate
def test_emailer_failed(email_url):
    responses.add(responses.POST, email_url, status=401)
    with pytest.raises(Exception):
        send_email('hello')
