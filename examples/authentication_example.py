from api_base import APIBase
from datetime import datetime, timedelta
import jwt


class AppleMusic(APIBase):
    """
    This class inherits from API Base. This is an authenticated API that needs a token.
    """

    def __init__(self, proxies=None):
        """
        Initialize the class. Calls the init method of APIBase and passes through root URL and proxy info.

        :param proxies: Dictionary of proxy information, if needed
        """
        super().__init__(root='https://api.music.apple.com/v1/', proxies=proxies)

    def generate_token(self, secret_key, key_id, team_id, session_length=12):
        """
        Generate encrypted token to be used by in API requests and sets the class token variable.
        APIBase will use the token if the token_str variable is not None or empty string.

        :param secret_key: Secret Key provided by Apple
        :param key_id: Key ID provided by Apple
        :param team_id: Team ID provided by Apple
        :param session_length: Length Apple Music token is valid, in hours
        """
        alg = 'ES256'  # encryption algo that Apple requires
        headers = {
            'alg': alg,
            'kid': key_id
        }
        payload = {
            'iss': team_id,  # issuer
            'iat': int(datetime.now().timestamp()),  # issued at
            'exp': int((datetime.now() + timedelta(hours=session_length)).timestamp())  # expiration time
        }
        token = jwt.encode(payload, secret_key, algorithm=alg, headers=headers)
        self.token_str = token.decode()

    def charts(self, storefront='us', chart=None, types=None, l=None, genre=None, limit=None, offset=None):
        """
        Get Apple Music Chart data

        :param storefront: Apple Music store front
        :param chart: Chart ID
        :param types: List of resource types (e.g. songs, albums, etc.)
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param genre: The genre of the chart
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A list of chart data in JSON format
        """
        url = self.root + 'catalog/{}/charts'.format(storefront)
        if types:
            type_str = ','.join(types)
        else:
            type_str = None
        return self._get(url, types=type_str, chart=chart, l=l, genre=genre, limit=limit, offset=offset)


# Instantiate class
am = AppleMusic()

# Get key info for authentication, stored in private files
keys = {}

with open('private_key.p8', 'r') as f:
    keys['secret'] = f.read()

with open('keys.txt') as f:
    for line in f:
        name, val = line.partition('=')[::2]
        keys[name.strip()] = val.strip()

# Generate the token. Sets am.token_str
am.generate_token(secret_key=keys['secret'], key_id=keys['keyID'], team_id=keys['teamID'])

# Make calls to the API
results = am.charts(types=['songs'], genre=14)
chart = results['results']['songs'][0]
print(chart['name'] + ':')
for i, item in enumerate(chart['data']):
    print('{0}) {1} - {2}'.format(str(i+1), item['attributes']['name'], item['attributes']['artistName']))

