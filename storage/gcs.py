
import os
from urllib.parse import urlparse
from google.cloud import storage

get_bucket_name = lambda f: urlparse(f).netloc
get_filename = lambda f: urlparse(f).path[1:]
get_prefix = lambda f: get_filename(f).rsplit('/', 1)[0] if f.count('/') > 1 else None
is_gcs_bucket = lambda f: urlparse(f).scheme == 'gs'

# GCS functions
get_bucket = lambda b: storage.Client().get_bucket(b)
list_blobs = lambda d: storage.Client().list_blobs(get_bucket_name(d), prefix=get_prefix(d))
put_object = lambda d, f: get_bucket(get_bucket_name(f)).blob(get_filename(f)).upload_from_string(d)
get_object = lambda f: get_bucket(get_bucket_name(f)).blob(get_filename(f)).download_as_string()
list_files = lambda d: [os.path.basename(blob.name) for blob in list_blobs(d) if not blob.name[-1] == '/']
put_file = lambda i, o: get_bucket(get_bucket_name(o)).blob(get_filename(o)).upload_from_filename(i)
get_file = lambda i, o: get_bucket(get_bucket_name(i)).blob(get_filename(i)).download_to_filename(o)
