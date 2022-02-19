import logging
import os

import requests

logger = logging.getLogger(__name__)


def send_email(text):
    logger.info('Sending mail: %s', text)
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox0ec66a6594f147c48dfac000ce780ea9.mailgun.org/messages",
        auth=("api", os.getenv('MAILGUN_APIKEY', '')),
        data={
            "from":
            "Digester <postmaster@sandbox0ec66a6594f147c48dfac000ce780ea9.mailgun.org>",
            "to": [os.getenv('EMAIL_RECIPIENT')],
            "subject": "Digest",
            "text": text
        })
    if response.status_code != 200:
        raise Exception(f'Could not send email. Reason: {response.content}')
