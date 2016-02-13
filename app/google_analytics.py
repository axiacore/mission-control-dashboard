import json

from django.conf import settings

from oauth2client.client import SignedJwtAssertionCredentials


# Load the key file's private data.
with open(settings.CLIENT_SECRET_FILE) as key_file:
    _key_data = json.load(key_file)


# Construct a credentials objects from the key data and OAuth2 scope.
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
_credentials = SignedJwtAssertionCredentials(
    _key_data['client_email'],
    _key_data['private_key'],
    SCOPE,
)


# Defines a method to get an access token from the credentials object.
# The access token is automatically refreshed if it has expired.
def get_access_token():
    return _credentials.get_access_token().access_token
