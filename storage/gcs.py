
import os
from urllib.parse import urlparse
from google.cloud import storage

# Parsers
get_bucket_name = lambda f: urlparse(f).netloc
get_filename = lambda f: urlparse(f).path[1:]
get_prefix = lambda f: get_filename(f).rsplit('/', 1)[0] if f.count('/') > 1 else None

# Helpers
is_gcs_bucket = lambda f: urlparse(f).scheme == 'gs'

# GCS functions
get_bucket = lambda b: storage.Client().get_bucket(b)

list_blobs = lambda d: storage.Client().list_blobs(get_bucket_name(d), prefix=get_prefix(d))
list_files = lambda d: [os.path.basename(blob.name) for blob in list_blobs(d) if not blob.name[-1] == '/']

get_blob = lambda f: get_bucket(get_bucket_name(f)).blob(get_filename(f))
delete_blob = lambda f: get_blob(f).delete()

put_object = lambda d, f: get_blob(f).upload_from_string(d)
get_object = lambda f: get_blob(f).download_as_string()

put_file = lambda i, o: get_blob(o).upload_from_filename(i)
get_file = lambda i, o: get_blob(i).download_to_filename(o)

file_exists = lambda f: get_blob(f).exists()

def copy_file(source_filename: str, dest_filename: str):
    source_bucket = get_bucket(get_bucket_name(source_filename))
    source_blob = get_blob(source_filename)
    destination_bucket = get_bucket(get_bucket_name(dest_filename))
    #copy file to destination bucket
    source_bucket.copy_blob(source_blob, destination_bucket, get_filename(dest_filename))

    return
