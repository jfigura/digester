# digester

Checks my activity on Spotify and sends
me a daily email with the songs I played yesterday.

## Installation

Uses [Poetry](https://python-poetry.org) for dependency management.

```bash
poetry install
make check
```

## Usage

Requires Spotify OAuth token and [Mailgun](https://www.mailgun.com) apikey.

```bash
export SPOTIPY_CLIENT_ID=<spotipy-client-id>
export SPOTIPY_CLIENT_SECRET=<spotipy-client-secret>
export SPOTIPY_REDIRECT_URI=<spotipy-redirect-uri>
export SPOTIFY_REFRESH_TOKEN=<spotify-refresh-token>
export MAILGUN_APIKEY=<mailgun-apikey>
export MAILGUN_URL=<mailgun-url>
export EMAIL_RECIPIENT=<email-recipient>
export EMAIL_SENDER=<email-sender>

make job
```

To run without email (prints Spotify results to stdout):
```bash
poetry run python digester/spotify.py
```

See [Spotipy instructions](https://spotipy.readthedocs.io/en/2.19.0/#quick-start)
to get the secrets. Scope `user-read-recently-played` is needed.
Spotipy can open a browser, where you need to sign in to Spotify, 
and it stores the tokens in `.cache` file. 
Then use the relevant values as env vars.

## Automation

To automate daily runs, GitHub Actions may be used as in 
[nightly.yaml](https://github.com/jfigura/digester/blob/main/.github/workflows/nightly.yaml).
Note the GitHub project secrets must be properly set.
