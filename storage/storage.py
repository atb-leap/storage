
import os
from urllib.parse import urlparse
from google.cloud import storage

from .csv import save_csv, read_csv
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
put_file = lambda i, o: get_bucket(get_bucket_name(o)).blob(get_filename(o)).upload_from_file(i)
get_file = lambda i, o: get_bucket(get_bucket_name(i)).blob(get_filename(i)).download_to_file(o)

# Helpers
is_supported_file_format = lambda f: True if os.path.splitext(f)[-1] in ['.json', '.tsv', '.csv'] else False

def listdir(directory: str):
    if is_gcs_bucket(directory):
        return list_files(d)
    elif os.path.exists(directory):
        return os.listdir(directory)
    else:
        return []

def delete(filename: str):
    if is_gcs_bucket(filename):
        raise Exception('Unimplemented feature!')
    else:
        os.remove(filename)

# Get an object from a file that is local or in gcs
def get(filename: str):
    _, extension = os.path.split(filename)
    fname = filename
    if is_gcs_bucket(filename):
        fname = os.path.join(tempfile.mkdtemp(), os.path.basename(filename))
        get_file(filename, fname)

    if extension == '.json':
        return read_json(fname)
    else:
        return read_csv(fname)

    if is_gcs_bucket(filename):
        delete(fname)

# Save an object to a file that is local or in gcs
def save(data: dict, filename: str):
    if not is_supported_file_format(filename):
        raise Exception('Unsupported file format requested')

    _, extension = os.path.splitext(filename)
    fname = filename
    if is_gcs_bucket(filename):
        fname = os.path.join(tempfile.mkdtemp(), os.path.basename(filename))

    if extension == '.json':
        save_json(data, fname)
    else:
        save_csv(data, fname)

    if is_gcs_bucket(filename):
        put_file(fname, filename)
        delete(fname)
