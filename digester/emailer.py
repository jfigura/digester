import logging
import os

import requests

logger = logging.getLogger(__name__)


def send_email(text):
    logger.info('Sending mail: %s', text)
    response = requests.post(os.getenv('MAILGUN_URL'),
                             auth=("api", os.getenv('MAILGUN_APIKEY', '')),
                             data={
                                 "from": os.getenv('EMAIL_SENDER'),
                                 "to": [os.getenv('EMAIL_RECIPIENT')],
                                 "subject": "Digest",
                                 "text": text
                             })
    if response.status_code != 200:
        raise Exception(f'Could not send email. Reason: {response.content}')
