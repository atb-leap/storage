
import json
import os
from urllib import request
from urllib.error import HTTPError

def load_json(json_string: str):
    return json.loads(json_string)

def dump_json(data, outfile = None):
    indent = None
    if outfile is None:
        return json.dumps(data, indent=indent)
    else:
        return json.dump(data, outfile, indent=indent)

def save_json(data, filename, append = False):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a' if append else 'w') as outfile:
        dump_json(data, outfile)

def read_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def fetch_json(url, path = None, options = {}):
    if path is not None:
        url = '{}/{}'.format(url, path)
    if len(options) > 0:
        url += '?' + '&'.join([str(name) + '=' + (','.join(option) if isinstance(option, list) else str(option)) for name, option in options.items()])
    print('Fetching "{}"'.format(url))
    with request.urlopen(url) as response:
        return json.loads(response.read())['data']
