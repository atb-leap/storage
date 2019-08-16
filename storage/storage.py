
import os
import numpy as np
from itertools import chain
from urllib.parse import urlparse
from google.cloud import storage

from .csv import save_csv
from .json import dump_json, load_json, read_json, save_json

get_bucket_name = lambda f: urlparse(f).netloc
get_filename = lambda f: urlparse(f).path[1:]
get_prefix = lambda f: get_filename(f).rsplit('/', 1)[0] if f.count('/') > 1 else None
is_gcs_bucket = lambda f: urlparse(f).scheme == 'gs'

# GCS functions
get_bucket = lambda b: storage.Client().get_bucket(b)
list_blobs = lambda d: storage.Client().list_blobs(get_bucket_name(d), prefix=get_prefix(d))
put_object = lambda d, f: get_bucket(get_bucket_name(f)).blob(get_filename(f)).upload_from_string(d)
get_object = lambda f: get_bucket(get_bucket_name(f)).blob(get_filename(f)).download_as_string()
list_files = lambda d: [blob.name for blob in list_blobs(d)]

# Helpers
is_supported_file_format = lambda f: True if os.path.splitext(f)[-1] in ['.json', '.tsv', '.csv'] else False

def listdir(directory: str):
    if is_gcs_bucket(directory):
        return list_files(d)
    elif os.path.exists(directory):
        return os.listdir(directory)
    else:
        return []

# Get an object from a file that is local or in gcs
def get(filename: str):
    if is_gcs_bucket(filename):
        return load_json(get_object(filename))
    else:
        return read_json(filename)

# Save an object to a file that is local or in gcs
def save(data, filename):
    if not is_supported_file_format(filename):
        raise Exception('Unsupported file format requested')

    _, extension = os.path.splitext(filename)
    if is_gcs_bucket(filename):
        if extension == '.json':
            data_string = dump_json(data)
        elif extension == '.tsv' or extension == '.csv':
            # TODO map the data to a string
            data_string = data

        return put_object(data_string, filename)
    else:
        if extension == '.json':
            return save_json(data, filename)
        else:
            return save_csv(data, filename)
