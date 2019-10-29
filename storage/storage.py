
import os
import warnings

from .helpers import get_temp_filename, get_extension, is_fully_supported_filetype, is_blob
from .blob import save_blob, read_blob
from .csv import save_csv, read_csv
from .json import dump_json, load_json, read_json, save_json
from .gcs import is_gcs_bucket, list_files, get_file, put_file, copy_file, delete_blob, file_exists

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

def exists(filename: str):
    if is_gcs_bucket(filename):
        return file_exists(filename)
    else:
        return os.path.exists(filename)

# Get an object from a file that is local or in gcs
def get(filename: str, asBlob=False, **kwargs):
    extension = get_extension(filename)
    fname = filename
    if is_gcs_bucket(filename):
        fname = get_temp_filename(filename)
        get_file(filename, fname)

    if not asBlob and is_fully_supported_filetype(filename):
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
def save(data: list, filename: str, asBlob=False, **kwargs):
    extension = get_extension(filename)
    fname = get_temp_filename(filename) if is_gcs_bucket(filename) else filename

    if not asBlob and is_fully_supported_filetype(filename):
        if extension == '.json':
            save_json(data, fname)
        elif extension == '.tsv' or extension == '.csv':
            save_csv(data, fname, **kwargs)
    else:
        save_blob(data, fname)

    if is_gcs_bucket(filename):
        put_file(fname, filename)
        delete(fname)

# Copy a file that is local or in gcs to a local or remote location
def copy(source_filename: str, dest_filename: str):
    if is_gcs_bucket(source_filename) and is_gcs_bucket(dest_filename) and (get_extension(source_filename) == get_extension(dest_filename) or is_blob(dest_filename)):
        copy_file(source_filename, dest_filename)
    else:
        asBlob = is_blob(source_filename) or is_blob(dest_filename)
        if is_blob(source_filename) and not is_blob(dest_filename):
            warnings.warn("The source file given ({}) is a blob but the destination ({}) is a structured file. This may result in the destination file being malformed as it will be a direct copy of the source file. Please ensure that the source file is properly formatted.".format(source_filename, dest_filename))
        save(get(source_filename, asBlob=asBlob), dest_filename, asBlob=asBlob)

# Move a file that is local or in gcs to a local or remote location
def move(source_filename: str, dest_filename: str):
    copy(source_filename, dest_filename)
    delete(source_filename)
