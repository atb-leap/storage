
import os

from .helpers import is_supported_file_format, get_temp_filename, get_extension
from .csv import save_csv, read_csv
from .json import dump_json, load_json, read_json, save_json
from .gcs import is_gcs_bucket, list_files, get_file, put_file, get_prefix

def listdir(directory: str):
    if is_gcs_bucket(directory):
        print(get_prefix(directory))
        return list_files(directory)
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
    assert is_supported_file_format(filename),'Unsupported file format! Cannot get {}'.format(filename)
    extension = get_extension(filename)
    fname = filename
    if is_gcs_bucket(filename):
        fname = get_temp_filename(filename)
        get_file(filename, fname)

    if extension == '.json':
        return read_json(fname)
    else:
        return read_csv(fname)

    if is_gcs_bucket(filename):
        delete(fname)

# Save an object to a file that is local or in gcs
def save(data: dict, filename: str):
    assert is_supported_file_format(filename),'Unsupported file format! Cannot save {}'.format(filename)

    extension = get_extension(filename)
    fname = get_temp_filename(filename) if is_gcs_bucket(filename) else filename

    if extension == '.json':
        save_json(data, fname)
    else:
        save_csv(data, fname)

    if is_gcs_bucket(filename):
        put_file(fname, filename)
        delete(fname)
