from django.conf import settings

from oauth2client.service_account import ServiceAccountCredentials


_credentials = ServiceAccountCredentials.from_json_keyfile_name(
    settings.CLIENT_SECRET_FILE,
    scopes=['https://www.googleapis.com/auth/analytics.readonly'],
)


# Defines a method to get an access token from the credentials object.
# The access token is automatically refreshed if it has expired.
def get_access_token():
    return _credentials.get_access_token().access_token
