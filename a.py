#!/usr/bin/env python3

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from pygments import highlight, lexers, formatters
import urllib.parse

import sys
import json
import os
import time
import readline
from builtins import input



def recursive_urlencode(d):
    def recursion(d, base=[]):
        pairs = []
        for key, value in d.items():
            new_base = base + [key]
            if hasattr(value, 'values'):
                pairs += recursion(value, new_base)
            else:
                new_pair = None
                if len(new_base) > 1:
                    first = new_base.pop(0)
                    rest = map(lambda x: x, new_base)
                    new_pair = "%s[%s]=%s" % (first, ']['.join(rest), str(value))
                else:
                    new_pair = "%s=%s" % (str(key), str(value))
                pairs.append(new_pair)
        return pairs
    return '&'.join(recursion(d))

def recursive_urlencode_quote(d):
    def recursion(d, base=[]):
        pairs = []
        for key, value in d.items():
            new_base = base + [key]
            if hasattr(value, 'values'):
                pairs += recursion(value, new_base)
            else:
                new_pair = None
                if len(new_base) > 1:
                    first = urllib.parse.quote(new_base.pop(0))
                    rest = map(lambda x: urllib.parse.quote(x), new_base)
                    new_pair = "%s[%s]=%s" % (first, ']['.join(rest), urllib.parse.quote(str(value)))
                else:
                    new_pair = "%s=%s" % (urllib.parse.quote(str(key)), urllib.parse.quote(str(value)))
                pairs.append(new_pair)
        return pairs
    return '&'.join(recursion(d))



def call(api, endpoint, params = {}):
    response = api.get(f'https://api.intra.42.fr/v2/{endpoint}', params=recursive_urlencode(params))
    return response


def call_rec(api, endpoint, params = {}, page = 1):
    params = {
        **params,
        "page": {
            "size": 100,
            "number": page,
        },
    }
    response = api.get(f'https://api.intra.42.fr/v2/{endpoint}', params=recursive_urlencode(params))
    #print(response.request.url)
    #print(response)
    raw_json = response.json()
    if raw_json:
        return raw_json + call_rec(api, endpoint, params, page + 1)
    else:
        return []


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
        print_results(call(api, endpoint).content)
        prompt(api)
    else:
        endpoint = sys.argv[1]
        print_results(call(api, endpoint).content)


def init_api():
    client_id = os.environ['API42_ID']
    client_secret = os.environ['API42_SECRET']

    client = BackendApplicationClient(client_id=client_id)
    api = OAuth2Session(client=client)
    token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id, client_secret=client_secret, scope=["public", "projects", "profile", "tig", "forum", "elearning"])
    return(api)


if __name__ == "__main__":
    try:
        api = init_api()
        prompt(api)
    except KeyboardInterrupt:
        sys.exit()
