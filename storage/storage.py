
import os

from .helpers import get_temp_filename, get_extension
from .blob import save_blob, read_blob
from .csv import save_csv, read_csv
from .json import dump_json, load_json, read_json, save_json
from .gcs import is_gcs_bucket, list_files, get_file, put_file, delete_blob

def listdir(directory: str):
    if is_gcs_bucket(directory):
        return list_files(directory)
    elif os.path.exists(directory):
        return os.listdir(directory)
    else:
        return []

def delete(filename: str):
    if is_gcs_bucket(filename):
        delete_blob(filename)
    else:
        os.remove(filename)

# Get an object from a file that is local or in gcs
def get(filename: str, **kwargs):
    extension = get_extension(filename)
    fname = filename
    if is_gcs_bucket(filename):
        fname = get_temp_filename(filename)
        get_file(filename, fname)

    if extension == '.json':
        result = read_json(fname)
    elif extension == '.tsv' or extension == '.csv':
        result = read_csv(fname, **kwargs)
    else:
        result = read_blob(fname)

    if is_gcs_bucket(filename):
        delete(fname)

    return result

# Save an object to a file that is local or in gcs
def save(data: list, filename: str, **kwargs):
    extension = get_extension(filename)
    fname = get_temp_filename(filename) if is_gcs_bucket(filename) else filename

    if extension == '.json':
        save_json(data, fname)
    elif extension == '.tsv' or extension == '.csv':
        save_csv(data, fname, **kwargs)
    else:
        save_blob(data, fname)

    if is_gcs_bucket(filename):
        put_file(fname, filename)
        delete(fname)
