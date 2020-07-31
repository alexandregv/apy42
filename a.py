from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from pygments import highlight, lexers, formatters

import sys
import json
import os
import readline

client_id = os.environ['API42_ID']
client_secret = os.environ['API42_SECRET']

client = BackendApplicationClient(client_id=client_id)
api = OAuth2Session(client=client)
token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id, client_secret=client_secret)

tty = sys.stdout.isatty()

if len(sys.argv) <= 1:
    try:
        input = raw_input
    except NameError:
        pass
    endpoint = input("> https://api.intra.42.fr/v2/" if tty else "")
else:
    endpoint = sys.argv[1]

response = api.get('https://api.intra.42.fr/v2/' + endpoint)
raw_json = response.content

if tty:
    colored_json = highlight(json.dumps(json.loads(raw_json), indent=2, ensure_ascii=False), lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colored_json)
else:
    print(raw_json.decode())
