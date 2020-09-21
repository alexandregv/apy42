#!/usr/bin/env python3

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from pygments import highlight, lexers, formatters

import sys
import json
import os
import time
import readline
from builtins import input


def call(api, endpoint):
    response = api.get('https://api.intra.42.fr/v2/' + endpoint)
    raw_json = response.content
    return raw_json


def print_results(raw_json):
    if sys.stdout.isatty():
        colored_json = highlight(json.dumps(json.loads(raw_json), indent=2, ensure_ascii=False), lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colored_json)
    else:
        if isinstance(raw_json, str):
            print(raw_json)
        else:
            print(raw_json.decode('utf-8'))


def prompt(api):
    if len(sys.argv) <= 1:
        if sys.stdout.isatty():
            sys.stderr.write(str("\033[91m> https://api.intra.42.fr/v2/\033[0m"))
        endpoint = input()
        print_results(call(api, endpoint))
        prompt(api)
    else:
        endpoint = sys.argv[1]
        print_results(call(api, endpoint))


def init_api():
    client_id = os.environ['API42_ID']
    client_secret = os.environ['API42_SECRET']

    client = BackendApplicationClient(client_id=client_id)
    api = OAuth2Session(client=client)
    token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id, client_secret=client_secret)

    return(api)


if __name__ == "__main__":
    try:
        api = init_api()
        prompt(api)
    except KeyboardInterrupt:
        sys.exit()
